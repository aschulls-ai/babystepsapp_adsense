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
import FormulaComparison from './components/FormulaComparison';
import EmergencyTraining from './components/EmergencyTraining';
import AIAssistant from './components/AIAssistant';
import Settings from './components/Settings';
import EmailVerification from './components/EmailVerification';
import PasswordReset from './components/PasswordReset';
import PrivacyPolicy from './components/PrivacyPolicy';
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
const initializeBackendMode = () => {
  localStorage.setItem('babysteps_app_mode', 'backend');
  console.log('🌐 Baby Steps running with backend connectivity - full API features available');
};

// Backend-enabled App - Full functionality with API connectivity
const API = process.env.REACT_APP_BACKEND_URL;

// Debug logging for connection issues
console.log('🔧 App Configuration:', {
  backendUrl: process.env.REACT_APP_BACKEND_URL,
  apiBase: API,
  environment: process.env.NODE_ENV
});

// Debug logging
console.log('Environment configuration:', {
  API,
  environment: process.env.REACT_APP_ENVIRONMENT || 'development',
  usingProductionAPI: !!process.env.REACT_APP_BACKEND_URL
});

// Alternative HTTP client for Android compatibility
export const androidFetch = async (url, options = {}) => {
  console.log('📱 Android-specific fetch:', { url, options });
  
  // Add a timeout wrapper to prevent hanging
  const timeout = options.timeout || 10000; // Default 10 second timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    // Method 1: Native fetch with Android-specific headers
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        ...options.headers
      },
      mode: 'cors',
      credentials: 'omit'
    });
    
    clearTimeout(timeoutId);
    console.log('📱 Android fetch success:', response.status);
    return response;
  } catch (fetchError) {
    clearTimeout(timeoutId);
    
    // Check if it was a timeout
    if (fetchError.name === 'AbortError') {
      console.log('📱 Request timeout after', timeout, 'ms');
      throw new Error('Request timeout');
    }
    
    console.log('📱 Android fetch failed, trying XMLHttpRequest:', fetchError);
    
    // Method 2: XMLHttpRequest with Promise wrapper
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const method = options.method || 'GET';
      
      xhr.open(method, url, true);
      xhr.timeout = timeout;
      
      // Set headers
      xhr.setRequestHeader('Accept', 'application/json');
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.setRequestHeader('User-Agent', 'BabyStepsApp/1.0 Android');
      xhr.setRequestHeader('Cache-Control', 'no-cache');
      
      xhr.onload = function() {
        console.log('📱 XHR success:', xhr.status, xhr.statusText);
        resolve({
          ok: xhr.status >= 200 && xhr.status < 300,
          status: xhr.status,
          statusText: xhr.statusText,
          json: () => Promise.resolve(JSON.parse(xhr.responseText || '{}')),
          text: () => Promise.resolve(xhr.responseText)
        });
      };
      
      xhr.onerror = function() {
        console.log('📱 XHR error:', xhr.statusText);
        reject(new Error(`XHR Error: ${xhr.statusText || 'Network Error'}`));
      };
      
      xhr.ontimeout = function() {
        console.log('📱 XHR timeout');
        reject(new Error('Request timeout'));
      };
      
      if (options.body) {
        xhr.send(options.body);
      } else {
        xhr.send();
      }
    });
  }
};

// Enhanced connection test function
const testConnection = async () => {
  console.log('🧪 Testing server connection...', { API, navigator_online: navigator.onLine });
  
  // Test 1: Basic fetch
  try {
    console.log('Test 1: Basic fetch to health endpoint');
    const response = await fetch(`${API}/api/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'User-Agent': 'BabyStepsApp/1.0 Android',
      }
    });
    
    console.log('Fetch response:', {
      ok: response.ok,
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries())
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Connection test successful:', data);
      return { success: true, data };
    } else {
      console.log('❌ Connection test failed:', response.status, response.statusText);
      return { success: false, error: `HTTP ${response.status}` };
    }
  } catch (error) {
    console.log('❌ Fetch failed, trying XMLHttpRequest...', error);
    
    // Test 2: XMLHttpRequest fallback
    return new Promise((resolve) => {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', `${API}/api/health`);
      xhr.setRequestHeader('Accept', 'application/json');
      xhr.timeout = 10000;
      
      xhr.onload = function() {
        console.log('XHR Success:', {
          status: xhr.status,
          statusText: xhr.statusText,
          responseText: xhr.responseText.substring(0, 100)
        });
        resolve({ success: true, data: { xhr: true, status: xhr.status } });
      };
      
      xhr.onerror = function() {
        console.log('❌ XHR Error:', xhr.statusText);
        resolve({ success: false, error: `XHR Error: ${xhr.statusText}` });
      };
      
      xhr.ontimeout = function() {
        console.log('❌ XHR Timeout');
        resolve({ success: false, error: 'XHR Timeout' });
      };
      
      xhr.send();
    });
  }
};

// Use androidFetch instead of axios for better Android WebView compatibility
// Axios has adapter issues in Android WebView environment
console.log('🔧 Configured to use androidFetch for all network requests (bypassing Axios adapter issues)');
axios.defaults.validateStatus = function (status) {
  return status >= 200 && status < 500; // Accept 4xx errors as valid responses
};

function App() {
  const [user, setUser] = useState(null);
  const [currentBaby, setCurrentBaby] = useState(null);
  const [babies, setBabies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  // Initialize theme on app start
  useEffect(() => {
    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme');
    const isDark = savedTheme === 'dark';
    setDarkMode(isDark);
    
    // Apply theme to document
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  // Theme toggle function
  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    
    // Save preference
    localStorage.setItem('theme', newDarkMode ? 'dark' : 'light');
    
    // Apply theme
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  useEffect(() => {
    // Define network event handlers
    const handleOnline = () => {
      console.log('🌐 Network: ONLINE');
      toast.info('Back online! Reconnecting to server...');
    };
    
    const handleOffline = () => {
      console.log('🌐 Network: OFFLINE');
      toast.warning('Network connection lost. Using offline mode.');
      enableOfflineMode();
    };
    
    const initializeApp = async () => {
      console.log('🚀 Initializing Baby Steps standalone app...');
      
      // Initialize standalone mode as primary
      initializeBackendMode();
      
      // Initialize mobile features if running on native platform
      if (Capacitor.isNativePlatform()) {
        await initializeMobileApp();
      }
      
      // Initialize offline mode
      initializeOfflineMode();
      
      // Wait a moment for initialization to complete, then fetch babies
      setTimeout(() => {
        if (shouldUseOfflineMode()) {
          console.log('🔄 Post-initialization: checking for babies...');
          fetchBabies();
        }
      }, 500);
      
      // Check internet connectivity
      console.log('🌐 Network status:', {
        online: navigator.onLine,
        connection: navigator.connection?.effectiveType || 'unknown',
        userAgent: navigator.userAgent
      });
      
      // Add network state listeners
      window.addEventListener('online', handleOnline);
      window.addEventListener('offline', handleOffline);
      
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
      
      console.log('✅ Baby Steps standalone app initialized successfully');
    };
    
    initializeApp();
    
    // Cleanup function to remove event listeners
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Load babies when user is authenticated
  useEffect(() => {
    const isAuthenticated = user || localStorage.getItem('token');
    if (isAuthenticated && !currentBaby && babies.length === 0) {
      console.log('🔄 User authenticated but no babies loaded, fetching...');
      fetchBabies();
    }
  }, [user, currentBaby, babies.length]);

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
    const token = localStorage.getItem('token');
    const rememberMe = localStorage.getItem('rememberMe') === 'true';
    const tokenExpiration = localStorage.getItem('tokenExpiration');
    const rememberedEmail = localStorage.getItem('rememberedEmail');

    if (token) {
      // Check if token is expired for remembered sessions
      if (rememberMe && tokenExpiration) {
        const now = new Date().getTime();
        if (now > parseInt(tokenExpiration)) {
          // Token expired, clear remembered session
          logout();
          setLoading(false);
          return;
        }
      }

      // Note: Using androidFetch instead of axios for critical auth calls
      // axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      console.log('🔑 Authentication token stored, using androidFetch for API calls');
      
      // Set user object first to avoid redirect
      setUser({ 
        authenticated: true, 
        email: rememberedEmail,
        rememberMe: rememberMe
      });
      
      try {
        await fetchBabies();
        if (rememberMe && rememberedEmail) {
          console.log('Auto-logged in with remembered credentials');
        }
      } catch (error) {
        console.error('Failed to fetch babies on auth check:', error);
        // Don't crash the app - just continue without babies
        // User can add a baby or try again from the UI
        console.log('✅ App continuing despite babies fetch failure - user can add baby from UI');
      }
    }
    setLoading(false);
  };

  const fetchBabies = async () => {
    try {
      if (shouldUseOfflineMode()) {
        console.log('🏠 Fetching babies from offline storage');
        const response = await offlineAPI.getBabies();
        console.log('👶 Babies response:', response);
        setBabies(response.data);
        if (response.data && response.data.length > 0) {
          console.log('✅ Setting current baby:', response.data[0]);
          setCurrentBaby(response.data[0]);
        } else {
          console.log('⚠️ No babies found in response');
        }
        return;
      }

      // Try online fetch using androidFetch (bypassing Axios adapter issues)
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/babies`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      const responseData = { data }; // Match axios response format
      setBabies(responseData.data);
      if (responseData.data.length > 0 && !currentBaby) {
        setCurrentBaby(responseData.data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch babies:', error);
      console.log('⚠️ Backend fetch failed, app will continue without babies loaded');
      // DON'T throw during initialization - let the app start successfully
      // User can try to add a baby or login again
    }
  };

  const login = async (email, password, rememberMe = false) => {
    // In standalone mode, always use local authentication first
    console.log('🔐 Attempting login in standalone mode...');
    console.log('📧 Login credentials:', { email, password: password ? '***' : 'empty' });
    
    try {
      // Use backend authentication (online mode)
      console.log('🌐 Calling backend API for login...');
      const response = await androidFetch(`${API}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      
      console.log('📡 Response status:', response.status, response.statusText);
      
      if (!response.ok) {
        // Try to get error details from response body
        let errorMessage = `HTTP ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
          console.error('❌ Backend error response:', errorData);
        } catch (e) {
          console.error('❌ Could not parse error response');
        }
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      console.log('✅ Login response received:', data);
      console.log('🔍 Response type:', typeof data, 'Keys:', Object.keys(data));
      
      // Backend returns {access_token, token_type} directly
      const access_token = data.access_token || data.data?.access_token;
      const userData = data.user || data.data?.user;
      
      console.log('👤 User data from login:', userData);
      console.log('🔑 Access token:', access_token);
      
      if (!access_token) {
        throw new Error('No access token received from backend');
      }
      
      localStorage.setItem('token', access_token);
      console.log('💾 Token saved to localStorage');
      
      if (rememberMe) {
        localStorage.setItem('rememberMe', 'true');
        localStorage.setItem('rememberedEmail', email);
        toast.success('Welcome back to Baby Steps!');
      } else {
        localStorage.removeItem('rememberMe');
        localStorage.removeItem('rememberedEmail');
        toast.success('Welcome to Baby Steps!');
      }
      
      // Handle case where backend doesn't return user data
      const userToSet = {
        id: userData?.id || 'backend-user',
        email: userData?.email || email,  // Use login email if not provided
        name: userData?.name || email.split('@')[0], // Use email prefix as name fallback
        authenticated: true,
        offline: false
      };
      console.log('👤 Setting user state to:', userToSet);
      setUser(userToSet);
      
      console.log('👶 Fetching babies after successful login...');
      await fetchBabies();
      console.log('✅ Login process completed successfully');
      return true;
    } catch (error) {
      console.error('❌ Standalone login failed:', error);
      toast.error(error.message || 'Login failed');
      throw error;
    }
  };

  const register = async (name, email, password) => {
    console.log('📝 Creating new account in standalone mode...');
    
    try {
      const response = await offlineAPI.register(name, email, password);
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      
      toast.success('Welcome to Baby Steps! Account created successfully.');
      setUser({ email, authenticated: true, offline: false }); // All features work in standalone
      return true;
    } catch (error) {
      console.error('❌ Registration failed:', error);
      toast.error(error.message || 'Registration failed');
      throw error;
    }
  };

  const resendVerification = async (email) => {
    try {
      await axios.post('/api/auth/resend-verification', { email });
      toast.success('Verification email sent! Please check your inbox.');
      return true;
    } catch (error) {
      toast.error('Failed to send verification email');
      return false;
    }
  };

  const requestPasswordReset = async (email) => {
    try {
      await axios.post('/api/auth/request-password-reset', { email });
      toast.success('Password reset link sent! Please check your email.');
      return true;
    } catch (error) {
      toast.error('Failed to send password reset email');
      return false;
    }
  };

  const resetPassword = async (token, newPassword) => {
    try {
      await axios.post('/api/auth/reset-password', { token, new_password: newPassword });
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
      // Use offline API for standalone mode
      console.log('👶 Creating baby in standalone mode:', babyData);
      const response = await offlineAPI.createBaby(babyData);
      const newBaby = response.data;
      
      setBabies([...babies, newBaby]);
      if (!currentBaby) {
        setCurrentBaby(newBaby);
      }
      toast.success(`${newBaby.name}'s profile created successfully! (Saved to device)`);
      console.log('✅ Baby created and state updated:', newBaby.name);
      return newBaby;
    } catch (error) {
      console.error('❌ Failed to add baby profile:', error);
      toast.error('Failed to add baby profile: ' + (error.message || 'Unknown error'));
      throw error;
    }
  };

  const updateBaby = async (babyData) => {
    try {
      // Use offline API for standalone mode
      console.log('👶 Updating baby in standalone mode:', babyData);
      const response = await offlineAPI.updateBaby(currentBaby.id, babyData);
      const updatedBaby = response.data;
      
      // Update babies array
      setBabies(babies.map(baby => 
        baby.id === updatedBaby.id ? updatedBaby : baby
      ));
      
      // Update current baby if it's the one being updated
      if (currentBaby.id === updatedBaby.id) {
        setCurrentBaby(updatedBaby);
      }
      
      toast.success(`${updatedBaby.name}'s profile updated successfully! (Saved to device)`);
      console.log('✅ Baby updated and state updated:', updatedBaby.name);
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

  const isAuthenticated = user || localStorage.getItem('token');

  return (
    <div className="App min-h-screen page-gradient">
      <Router>
        <Routes>
          <Route 
            path="/auth" 
            element={
              isAuthenticated ? 
              <Navigate to="/dashboard" replace /> : 
              <AuthPage 
                onLogin={login} 
                onRegister={register}
                onRequestPasswordReset={requestPasswordReset}
                onResendVerification={resendVerification}
              />
            } 
          />
          
          {/* Email verification and password reset routes - accessible without authentication */}
          <Route path="/verify-email/:token" element={<EmailVerification />} />
          <Route path="/reset-password/:token" element={<PasswordReset onResetPassword={resetPassword} />} />
          
          {/* Privacy policy - accessible without authentication */}
          <Route path="/privacy-policy" element={<PrivacyPolicy />} />
          
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
                darkMode={darkMode}
                onToggleDarkMode={toggleDarkMode}
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
                      path="/formula-comparison" 
                      element={<FormulaComparison />} 
                    />
                    <Route 
                      path="/emergency-training" 
                      element={<EmergencyTraining />} 
                    />
                    <Route 
                      path="/ai-assistant" 
                      element={<AIAssistant currentBaby={currentBaby} />} 
                    />
                    <Route 
                      path="/settings" 
                      element={
                        <Settings 
                          onLogout={logout} 
                          darkMode={darkMode}
                          onToggleDarkMode={toggleDarkMode}
                        />
                      } 
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
        
        {/* Bottom Banner Ad - Only show when user is logged in */}
        {user && <BottomBannerAd />}
        
        {/* Add padding to prevent content overlap with bottom banner */}
        {user && <div className="h-16 md:h-20" />}
        
        {/* Vercel Speed Insights for performance monitoring */}
        <SpeedInsights />
      </Router>
    </div>
  );
}

export default App;