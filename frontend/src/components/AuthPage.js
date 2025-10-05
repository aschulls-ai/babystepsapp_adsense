import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Baby, ShieldCheck, Heart, Utensils, Activity, ChefHat } from 'lucide-react';

const AuthPage = ({ onLogin, onRegister, onRequestPasswordReset, onResendVerification }) => {
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [registerData, setRegisterData] = useState({ name: '', email: '', password: '' });
  const [resetEmail, setResetEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPasswordReset, setShowPasswordReset] = useState(false);
  const [registrationResult, setRegistrationResult] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    await onLogin(loginData.email, loginData.password);
    setLoading(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    const result = await onRegister(registerData.name, registerData.email, registerData.password);
    if (result && result.requiresVerification) {
      setRegistrationResult(result);
    }
    setLoading(false);
  };

  const handlePasswordReset = async (e) => {
    e.preventDefault();
    setLoading(true);
    await onRequestPasswordReset(resetEmail);
    setLoading(false);
    setShowPasswordReset(false);
    setResetEmail('');
  };

  const handleResendVerification = async () => {
    if (registrationResult && registrationResult.email) {
      await onResendVerification(registrationResult.email);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-green-50 via-white to-blue-50">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
        <div className="absolute top-1/2 right-1/4 w-64 h-64 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/2 w-64 h-64 bg-orange-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse delay-500"></div>
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Hero Section */}
        <div className="text-center mb-8 fade-in">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-white rounded-full shadow-lg border-2 border-green-100">
              <Baby className="w-12 h-12 text-green-600" />
            </div>
          </div>
          <h1 className="text-4xl font-bold font-display text-gray-900 mb-3">
            Baby Steps
          </h1>
          <p className="text-lg text-gray-600 leading-relaxed mb-4">
            Complete parenting companion for baby tracking, nutrition & safety
          </p>
          
          {/* Features preview */}
          <div className="grid grid-cols-3 gap-4 mt-6 text-xs text-gray-500">
            <div className="flex flex-col items-center gap-1">
              <Activity className="w-4 h-4 text-rose-500" />
              <span>Activity Tracking</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <Utensils className="w-4 h-4 text-green-500" />
              <span>Food Safety</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <ShieldCheck className="w-4 h-4 text-red-500" />
              <span>Emergency Training</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <ChefHat className="w-4 h-4 text-orange-500" />
              <span>Meal Planning</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <Heart className="w-4 h-4 text-purple-500" />
              <span>Growth Tracking</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <Baby className="w-4 h-4 text-blue-500" />
              <span>Multi-Baby Support</span>
            </div>
          </div>
        </div>

        {/* Auth Card */}
        <Card className="glass-strong shadow-2xl border-0 slide-up">
          <CardHeader>
            <CardTitle className="text-2xl font-semibold text-center text-gray-800">
              Join Baby Steps
            </CardTitle>
            <p className="text-center text-sm text-gray-600 mt-2">
              Parenting made easy
            </p>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6 bg-gray-100 p-1 rounded-xl">
                <TabsTrigger 
                  value="login" 
                  className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-md transition-all duration-200"
                  data-testid="login-tab"
                >
                  Sign In
                </TabsTrigger>
                <TabsTrigger 
                  value="register" 
                  className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-md transition-all duration-200"
                  data-testid="register-tab"
                >
                  Sign Up
                </TabsTrigger>
              </TabsList>

              <TabsContent value="login">
                <form onSubmit={handleLogin} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="login-email" className="text-sm font-medium text-gray-700">
                      Email Address
                    </Label>
                    <Input
                      id="login-email"
                      type="email"
                      placeholder="Enter your email"
                      value={loginData.email}
                      onChange={(e) => setLoginData({...loginData, email: e.target.value})}
                      required
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 transition-all duration-200"
                      data-testid="login-email-input"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="login-password" className="text-sm font-medium text-gray-700">
                      Password
                    </Label>
                    <Input
                      id="login-password"
                      type="password"
                      placeholder="Enter your password"
                      value={loginData.password}
                      onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                      required
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 transition-all duration-200"
                      data-testid="login-password-input"
                    />
                  </div>
                  <Button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
                    data-testid="login-submit-btn"
                  >
                    {loading ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Signing In...
                      </div>
                    ) : (
                      'Sign In'
                    )}
                  </Button>
                  
                  {/* Forgot Password Link */}
                  <div className="text-center mt-4">
                    <button
                      type="button"
                      onClick={() => setShowPasswordReset(true)}
                      className="text-sm text-blue-600 hover:text-blue-800 underline"
                    >
                      Forgot your password?
                    </button>
                  </div>
                </form>
              </TabsContent>

              <TabsContent value="register">
                <form onSubmit={handleRegister} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="register-name" className="text-sm font-medium text-gray-700">
                      Full Name
                    </Label>
                    <Input
                      id="register-name"
                      type="text"
                      placeholder="Enter your full name"
                      value={registerData.name}
                      onChange={(e) => setRegisterData({...registerData, name: e.target.value})}
                      required
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 transition-all duration-200"
                      data-testid="register-name-input"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="register-email" className="text-sm font-medium text-gray-700">
                      Email Address
                    </Label>
                    <Input
                      id="register-email"
                      type="email"
                      placeholder="Enter your email"
                      value={registerData.email}
                      onChange={(e) => setRegisterData({...registerData, email: e.target.value})}
                      required
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 transition-all duration-200"
                      data-testid="register-email-input"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="register-password" className="text-sm font-medium text-gray-700">
                      Password
                    </Label>
                    <Input
                      id="register-password"
                      type="password"
                      placeholder="Create a password"
                      value={registerData.password}
                      onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                      required
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 transition-all duration-200"
                      data-testid="register-password-input"
                    />
                  </div>
                  
                  {/* Multi-device note */}
                  <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                    <p className="text-xs text-green-700">
                      <strong>Multi-Device Access:</strong> Both parents can sign in with the same account on different devices to access all baby data together.
                    </p>
                  </div>
                  
                  {/* Disclaimer */}
                  <div className="disclaimer">
                    <p className="text-xs text-gray-600">
                      <span className="warning-text">⚠️ Important:</span> Baby Steps provides educational content only. 
                      Always consult your pediatrician for medical advice. Emergency training content is not a substitute for formal CPR/First Aid certification.
                    </p>
                  </div>
                  
                  <Button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
                    data-testid="register-submit-btn"
                  >
                    {loading ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        Creating Account...
                      </div>
                    ) : (
                      'Create Account'
                    )}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        {/* Email Verification Notice */}
        {registrationResult && registrationResult.requiresVerification && (
          <Card className="mt-6 border-blue-200 bg-blue-50">
            <CardContent className="p-6">
              <div className="text-center">
                <div className="text-blue-600 text-lg font-semibold mb-2">
                  📧 Check Your Email!
                </div>
                <p className="text-sm text-blue-700 mb-4">
                  We've sent a verification link to <strong>{registrationResult.email}</strong>
                </p>
                <p className="text-xs text-blue-600 mb-4">
                  Please click the link in your email to verify your account before logging in.
                </p>
                <Button
                  onClick={handleResendVerification}
                  variant="outline"
                  className="text-blue-600 border-blue-600 hover:bg-blue-100"
                >
                  Resend Verification Email
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Password Reset Modal */}
        {showPasswordReset && (
          <Card className="mt-6 border-orange-200 bg-orange-50">
            <CardHeader>
              <CardTitle className="text-center text-orange-800">Reset Password</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handlePasswordReset} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="reset-email" className="text-sm font-medium text-gray-700">
                    Email Address
                  </Label>
                  <Input
                    id="reset-email"
                    type="email"
                    placeholder="Enter your email address"
                    value={resetEmail}
                    onChange={(e) => setResetEmail(e.target.value)}
                    required
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all duration-200"
                  />
                </div>
                <div className="flex gap-3">
                  <Button
                    type="submit"
                    disabled={loading}
                    className="flex-1 bg-orange-600 hover:bg-orange-700 text-white"
                  >
                    {loading ? 'Sending...' : 'Send Reset Link'}
                  </Button>
                  <Button
                    type="button"
                    onClick={() => setShowPasswordReset(false)}
                    variant="outline"
                    className="flex-1"
                  >
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-gray-500 space-y-2">
          <p>Parenting made easy</p>
          <div className="flex justify-center items-center gap-4">
            <a 
              href="/privacy-policy" 
              className="text-blue-600 hover:text-blue-800 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Privacy Policy
            </a>
            <span>•</span>
            <a 
              href="mailto:support@babysteps.app" 
              className="text-blue-600 hover:text-blue-800 underline"
            >
              Contact Support
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;