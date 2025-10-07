import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import axios from 'axios';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner';
import { Capacitor } from '@capacitor/core';
import { StatusBar, Style } from '@capacitor/status-bar';
import { SplashScreen } from '@capacitor/splash-screen';
import { mobileService } from './services/MobileService';
import { SpeedInsights } from "@vercel/speed-insights/react";
import { runApiTests } from './utils/apiTest';
import './App.css';

// Components
import AuthPage from './components/AuthPage';
import Dashboard from './components/Dashboard';
import BabyProfile from './components/BabyProfile';
import TrackingPage from './components/TrackingPage';
import FoodResearch from './components/FoodResearch';
import FormulaComparison from './components/FormulaComparison';
import EmergencyTraining from './components/EmergencyTraining';
import MealPlanner from './components/MealPlanner';
import Research from './components/Research';
import EmailVerification from './components/EmailVerification';
import PasswordReset from './components/PasswordReset';
import PrivacyPolicy from './components/PrivacyPolicy';
import Layout from './components/Layout';
import BottomBannerAd from './components/ads/BottomBannerAd';

// Backend URL Configuration - Use relative paths for Vercel API routes
const API = '/api';

// Debug logging
console.log('Environment configuration:', {
  API,
  usingRelativePaths: true
});

// Set up axios defaults
axios.defaults.baseURL = API;

function App() {
  const [user, setUser] = useState(null);
  const [currentBaby, setCurrentBaby] = useState(null);
  const [babies, setBabies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeApp = async () => {
      // Initialize mobile features if running on native platform
      if (Capacitor.isNativePlatform()) {
        await initializeMobileApp();
      }
      
      await checkAuthState();
      
      // Run API tests in development/debugging mode
      if (process.env.NODE_ENV === 'development' || window.location.hostname.includes('vercel')) {
        runApiTests().then(results => {
          console.log('API Test Results:', results);
          if (!results.overall) {
            console.warn('⚠️ API connection issues detected. Check deployment configuration.');
          }
        });
      }
    };
    
    initializeApp();
  }, []);

  const initializeMobileApp = async () => {
    try {
      // Set status bar style
      await StatusBar.setStyle({ style: Style.Light });
      await StatusBar.setBackgroundColor({ color: '#10b981' });
      
      // Hide splash screen after app is ready
      await SplashScreen.hide();
      
      // Initialize mobile service
      await mobileService.initializeServices();
      
      console.log('Mobile app initialized successfully');
    } catch (error) {
      console.error('Mobile app initialization failed:', error);
    }
  };

  const checkAuthState = async () => {
    // Auto-login as sample user for AdSense verification
    try {
      console.log('🎭 Auto-logging in as sample user for AdSense verification...');
      
      const sampleUserLogin = await axios.post('/auth/login', {
        email: 'demo@babysteps.com',
        password: 'DemoPassword123'
      });

      if (sampleUserLogin.data.access_token) {
        const token = sampleUserLogin.data.access_token;
        localStorage.setItem('token', token);
        localStorage.setItem('rememberMe', 'true');
        localStorage.setItem('rememberedEmail', 'demo@babysteps.com');
        
        // Set up axios headers
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        // Fetch user data
        await fetchBabies();
        
        // Set user state
        setUser({ 
          authenticated: true, 
          email: 'demo@babysteps.com',
          rememberMe: true
        });
        
        console.log('✅ Auto-login successful as demo user');
      }
    } catch (error) {
      console.log('⚠️ Auto-login failed, trying fallback sample user...');
      
      // Fallback: try the existing test user
      try {
        const fallbackLogin = await axios.post('/auth/login', {
          email: 'test@babysteps.com',
          password: 'TestPassword123'
        });

        if (fallbackLogin.data.access_token) {
          const token = fallbackLogin.data.access_token;
          localStorage.setItem('token', token);
          localStorage.setItem('rememberMe', 'true');
          localStorage.setItem('rememberedEmail', 'test@babysteps.com');
          
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          await fetchBabies();
          
          setUser({ 
            authenticated: true, 
            email: 'test@babysteps.com',
            rememberMe: true
          });
          
          console.log('✅ Fallback auto-login successful');
        }
      } catch (fallbackError) {
        console.error('❌ Both auto-login attempts failed:', fallbackError);
        // Create mock user state for AdSense verification even if backend fails
        setUser({ 
          authenticated: true, 
          email: 'demo@babysteps.com',
          rememberMe: true
        });
        
        // Create mock baby data for display
        setCurrentBaby({
          id: 'demo-baby-001',
          name: 'Emma Johnson',
          birth_date: '2023-04-15',
          gender: 'girl'
        });
        
        setBabies([{
          id: 'demo-baby-001',
          name: 'Emma Johnson', 
          birth_date: '2023-04-15',
          gender: 'girl'
        }]);
        
        console.log('🎭 Using mock data for AdSense verification');
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

  const login = async (email, password, rememberMe = false) => {
    try {
      const response = await axios.post('/auth/login', { email, password });
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Handle remember me functionality
      if (rememberMe) {
        localStorage.setItem('rememberMe', 'true');
        localStorage.setItem('rememberedEmail', email);
        // Set longer expiration for remembered sessions (30 days)
        const expirationTime = new Date().getTime() + (30 * 24 * 60 * 60 * 1000);
        localStorage.setItem('tokenExpiration', expirationTime.toString());
        toast.success('Welcome back! You will stay signed in on this device.');
      } else {
        localStorage.removeItem('rememberMe');
        localStorage.removeItem('rememberedEmail');
        localStorage.removeItem('tokenExpiration');
        toast.success('Welcome to Baby Steps!');
      }
      
      // Set user state to trigger re-render
      setUser({ email });
      await fetchBabies();
      return true;
    } catch (error) {
      console.error('Login error:', error);
      if (error.code === 'ERR_NETWORK') {
        toast.error('Unable to connect to server. Please check your internet connection.');
      } else if (error.response?.status === 404) {
        toast.error('Login service not available. Please try again later.');
      } else {
        toast.error(error.response?.data?.detail || 'Login failed');
      }
      return false;
    }
  };

  const register = async (name, email, password) => {
    try {
      const response = await axios.post('/auth/register', { name, email, password });
      
      // Registration successful - user can login immediately
      toast.success('Account created successfully! You can now log in.');
      return { success: true, requiresVerification: false, email };
    } catch (error) {
      console.error('Registration error:', error);
      if (error.code === 'ERR_NETWORK') {
        toast.error('Unable to connect to server. Please check your internet connection.');
      } else if (error.response?.status === 404) {
        toast.error('Registration service not available. Please try again later.');
      } else {
        toast.error(error.response?.data?.detail || 'Registration failed');
      }
      return { success: false };
    }
  };

  const resendVerification = async (email) => {
    try {
      await axios.post('/auth/resend-verification', { email });
      toast.success('Verification email sent! Please check your inbox.');
      return true;
    } catch (error) {
      toast.error('Failed to send verification email');
      return false;
    }
  };

  const requestPasswordReset = async (email) => {
    try {
      await axios.post('/auth/request-password-reset', { email });
      toast.success('Password reset link sent! Please check your email.');
      return true;
    } catch (error) {
      toast.error('Failed to send password reset email');
      return false;
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      await axios.post('/auth/reset-password', { token, new_password: newPassword });
      toast.success('Password reset successful! You can now log in.');
      return true;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Password reset failed');
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('rememberMe');
    localStorage.removeItem('rememberedEmail');
    localStorage.removeItem('tokenExpiration');
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

  const updateBaby = async (babyData) => {
    try {
      const response = await axios.put(`/babies/${currentBaby.id}`, babyData);
      const updatedBaby = response.data;
      
      // Update babies array
      setBabies(babies.map(baby => 
        baby.id === updatedBaby.id ? updatedBaby : baby
      ));
      
      // Update current baby if it's the one being updated
      if (currentBaby.id === updatedBaby.id) {
        setCurrentBaby(updatedBaby);
      }
      
      toast.success(`${updatedBaby.name}'s profile updated successfully!`);
      return updatedBaby;
    } catch (error) {
      toast.error('Failed to update baby profile');
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

  // Always show as authenticated for AdSense verification
  const isAuthenticated = true;

  return (
    <div className="App min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
      <Router>
        <Routes>
          {/* Redirect /auth to dashboard for AdSense verification */}
          <Route 
            path="/auth" 
            element={<Navigate to="/dashboard" replace />} 
          />
          
          {/* Email verification and password reset routes - redirect to dashboard */}
          <Route path="/verify-email/:token" element={<Navigate to="/dashboard" replace />} />
          <Route path="/reset-password/:token" element={<Navigate to="/dashboard" replace />} />
          
          {/* Privacy policy - accessible without authentication */}
          <Route path="/privacy-policy" element={<PrivacyPolicy />} />
          
          {/* Main app routes - no authentication required for AdSense verification */}
          <Route 
            path="/*" 
            element={
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
                        onUpdateBaby={updateBaby}
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
                    path="/formula-comparison" 
                    element={
                      <FormulaComparison 
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
        
        {/* Bottom Banner Ad - Always show for AdSense verification */}
        <BottomBannerAd />
        
        {/* Add padding to prevent content overlap with bottom banner */}
        <div className="h-16 md:h-20" />
        
        {/* Vercel Speed Insights for performance monitoring */}
        <SpeedInsights />
      </Router>
    </div>
  );
}

export default App;