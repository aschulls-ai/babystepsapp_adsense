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
import billingService from './services/BillingService';
import './App.css';

// Components
import AuthPage from './components/AuthPage';
import Dashboard from './components/Dashboard';
import BabyProfile from './components/BabyProfile';
import TrackingPage from './components/TrackingPage';
import Analysis from './components/Analysis';
import FormulaComparison from './components/FormulaComparison';
import EmergencyTraining from './components/EmergencyTraining';
import AIAssistant from './components/AIAssistant';
import Settings from './components/Settings';
import EmailVerification from './components/EmailVerification';
import PasswordReset from './components/PasswordReset';
import PrivacyPolicy from './components/PrivacyPolicy';
import TermsOfService from './components/TermsOfService';
import FAQ from './components/FAQ';
import Layout from './components/Layout';
import BottomBannerAd from './components/ads/BottomBannerAd';

// Import standalone app mode (primary mode)
import { 
  shouldUseOfflineMode, 
  enableOfflineMode, 
  initializeOfflineMode, 
  offlineAPI,
  isOfflineMode 
} from './offlineMode';

// Initialize backend mode on app start
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Demo credentials for auto-login
const DEMO_EMAIL = 'demo@babysteps.com';
const DEMO_PASSWORD = 'demo123';

// Android fetch wrapper for native app compatibility
export const androidFetch = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    return response;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
};

function App() {
  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAutoLoggingIn, setIsAutoLoggingIn] = useState(true);
  
  // Baby management state
  const [babies, setBabies] = useState([]);
  const [currentBaby, setCurrentBaby] = useState(null);
  
  // Theme state
  const [darkMode, setDarkMode] = useState(false);

  // Auto-login on mount
  useEffect(() => {
    autoLogin();
  }, []);

  const autoLogin = async () => {
    try {
      // Try to get existing token first
      const existingToken = localStorage.getItem('token');
      if (existingToken) {
        // Verify token is still valid
        try {
          const api = isOfflineMode() ? offlineAPI : axios.create({
            baseURL: BACKEND_URL,
            timeout: 10000
          });
          
          const response = await api.get('/api/user/profile', {
            headers: { Authorization: `Bearer ${existingToken}` }
          });
          
          if (response.data) {
            setIsAuthenticated(true);
            await loadUserData();
            setIsAutoLoggingIn(false);
            return;
          }
        } catch (error) {
          // Token invalid, proceed with demo login
          localStorage.removeItem('token');
        }
      }

      // Perform demo account login
      const api = isOfflineMode() ? offlineAPI : axios.create({
        baseURL: BACKEND_URL,
        timeout: 10000
      });

      const response = await api.post('/api/auth/login', {
        email: DEMO_EMAIL,
        password: DEMO_PASSWORD
      });

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        setIsAuthenticated(true);
        await loadUserData();
      }
    } catch (error) {
      console.error('Auto-login failed:', error);
      // If auto-login fails, still set authenticated to show the app
      // This ensures AdSense reviewers can see the content
      setIsAuthenticated(true);
    } finally {
      setIsAutoLoggingIn(false);
    }
  };

  const loadUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const api = isOfflineMode() ? offlineAPI : axios.create({
        baseURL: BACKEND_URL,
        timeout: 10000
      });

      // Load babies
      const babiesResponse = await api.get('/api/babies', {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (babiesResponse.data) {
        setBabies(babiesResponse.data);
        if (babiesResponse.data.length > 0) {
          const savedBabyId = localStorage.getItem('currentBabyId');
          const baby = savedBabyId 
            ? babiesResponse.data.find(b => b.id === savedBabyId) 
            : babiesResponse.data[0];
          setCurrentBaby(baby || babiesResponse.data[0]);
        }
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  // Initialize mobile services
  useEffect(() => {
    const initMobile = async () => {
      if (Capacitor.isNativePlatform()) {
        try {
          await SplashScreen.hide();
          await StatusBar.setStyle({ style: Style.Default });
          
          // Initialize mobile service with backend URL
          mobileService.setBackendUrl(BACKEND_URL);
          
          // Handle deep links
          mobileService.handleDeepLink((url) => {
            console.log('Deep link received:', url);
          });
        } catch (error) {
          console.error('Mobile initialization error:', error);
        }
      }
    };

    initMobile();
  }, []);

  // Dark mode management
  useEffect(() => {
    const savedMode = localStorage.getItem('darkMode') === 'true';
    setDarkMode(savedMode);
    document.documentElement.classList.toggle('dark', savedMode);
  }, []);

  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('darkMode', newMode.toString());
    document.documentElement.classList.toggle('dark', newMode);
  };

  const handleBabySwitch = (babyId) => {
    const baby = babies.find(b => b.id === babyId);
    if (baby) {
      setCurrentBaby(baby);
      localStorage.setItem('currentBabyId', babyId);
    }
  };

  const handleLogout = () => {
    // For demo, just reload to auto-login again
    localStorage.removeItem('token');
    window.location.reload();
  };

  // Show loading while auto-logging in
  if (isAutoLoggingIn) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-700 dark:text-gray-300">Loading Baby Steps Demo...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Toaster position="top-center" />
        <SpeedInsights />
        <Routes>
          {/* Public routes */}
          <Route path="/privacy-policy" element={<PrivacyPolicy />} />
          <Route path="/terms-of-service" element={<TermsOfService />} />
          <Route path="/faq" element={<FAQ />} />
          
          {/* All other routes go to dashboard/app */}
          <Route 
            path="/*" 
            element={
              <Layout 
                currentBaby={currentBaby}
                babies={babies}
                onBabySwitch={handleBabySwitch}
                darkMode={darkMode}
                onToggleDarkMode={toggleDarkMode}
                onLogout={handleLogout}
              >
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<Dashboard currentBaby={currentBaby} />} />
                  <Route path="/profile" element={<BabyProfile currentBaby={currentBaby} onBabyUpdate={loadUserData} />} />
                  <Route path="/track" element={<TrackingPage currentBaby={currentBaby} />} />
                  <Route path="/analysis" element={<Analysis currentBaby={currentBaby} />} />
                  <Route path="/formula" element={<FormulaComparison />} />
                  <Route path="/emergency" element={<EmergencyTraining />} />
                  <Route path="/ai-assistant" element={<AIAssistant />} />
                  <Route path="/settings" element={<Settings onLogout={handleLogout} darkMode={darkMode} onToggleDarkMode={toggleDarkMode} />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Layout>
            }
          />
        </Routes>
        
        {/* Bottom banner ad */}
        <BottomBannerAd />
      </div>
    </Router>
  );
}

export default App;
