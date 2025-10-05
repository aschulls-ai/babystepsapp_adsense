import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';
import './App.css';

// Components
import AuthPage from './components/AuthPage';
import Dashboard from './components/Dashboard';
import BabyProfile from './components/BabyProfile';
import TrackingPage from './components/TrackingPage';
import FoodResearch from './components/FoodResearch';
import EmergencyTraining from './components/EmergencyTraining';
import MealPlanner from './components/MealPlanner';
import Research from './components/Research';
import Layout from './components/Layout';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Set up axios defaults
axios.defaults.baseURL = API;

function App() {
  const [user, setUser] = useState(null);
  const [currentBaby, setCurrentBaby] = useState(null);
  const [babies, setBabies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthState();
  }, []);

  const checkAuthState = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      try {
        await fetchBabies();
        // Set a basic user object to indicate authentication
        setUser({ authenticated: true });
      } catch (error) {
        console.error('Auth check failed:', error);
        logout();
      }
    }
    setLoading(false);
  };

  const fetchBabies = async () => {
    try {
      const response = await axios.get('/babies');
      setBabies(response.data);
      if (response.data.length > 0 && !currentBaby) {
        setCurrentBaby(response.data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch babies:', error);
      throw error;
    }
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post('/auth/login', { email, password });
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Set user state to trigger re-render
      setUser({ email });
      await fetchBabies();
      toast.success('Welcome to Baby Steps!');
      return true;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed');
      return false;
    }
  };

  const register = async (name, email, password) => {
    try {
      const response = await axios.post('/auth/register', { name, email, password });
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Set user state to trigger re-render
      setUser({ email, name });
      await fetchBabies();
      
      toast.success('Account created successfully! Welcome to Baby Steps!');
      return true;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed');
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setCurrentBaby(null);
    setBabies([]);
    toast.success('Logged out successfully');
  };

  const addBaby = async (babyData) => {
    try {
      const response = await axios.post('/babies', babyData);
      const newBaby = response.data;
      setBabies([...babies, newBaby]);
      if (!currentBaby) {
        setCurrentBaby(newBaby);
      }
      toast.success(`${newBaby.name}'s profile created successfully!`);
      return newBaby;
    } catch (error) {
      toast.error('Failed to add baby profile');
      throw error;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-white to-blue-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Baby Steps...</p>
        </div>
      </div>
    );
  }

  const isAuthenticated = user || localStorage.getItem('token');

  return (
    <div className="App min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
      <Router>
        <Routes>
          <Route 
            path="/auth" 
            element={
              isAuthenticated ? 
              <Navigate to="/dashboard" replace /> : 
              <AuthPage onLogin={login} onRegister={register} />
            } 
          />
          
          <Route 
            path="/*" 
            element={
              !isAuthenticated ? 
              <Navigate to="/auth" replace /> : 
              <Layout 
                currentBaby={currentBaby}
                babies={babies}
                onSwitchBaby={setCurrentBaby}
                onLogout={logout}
              >
                <Routes>
                  <Route 
                    path="/dashboard" 
                    element={
                      <Dashboard 
                        currentBaby={currentBaby}
                        onAddBaby={addBaby}
                      />
                    } 
                  />
                  <Route 
                    path="/baby-profile" 
                    element={
                      <BabyProfile 
                        currentBaby={currentBaby}
                        onAddBaby={addBaby}
                      />
                    } 
                  />
                  <Route 
                    path="/tracking" 
                    element={
                      <TrackingPage 
                        currentBaby={currentBaby}
                      />
                    } 
                  />
                  <Route 
                    path="/food-research" 
                    element={
                      <FoodResearch 
                        currentBaby={currentBaby}
                      />
                    } 
                  />
                  <Route 
                    path="/emergency-training" 
                    element={<EmergencyTraining currentBaby={currentBaby} />} 
                  />
                  <Route 
                    path="/meal-planner" 
                    element={
                      <MealPlanner 
                        currentBaby={currentBaby}
                      />
                    } 
                  />
                  <Route 
                    path="/research" 
                    element={<Research />} 
                  />
                  <Route 
                    path="/" 
                    element={<Navigate to="/dashboard" replace />} 
                  />
                </Routes>
              </Layout>
            } 
          />
        </Routes>
        <Toaster position="top-right" />
      </Router>
    </div>
  );
}

export default App;