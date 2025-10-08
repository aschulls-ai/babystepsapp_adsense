import React, { useState, useEffect } from 'react';
import { 
  Settings as SettingsIcon, 
  Sun, 
  Moon, 
  User, 
  Lock, 
  LogOut,
  Eye,
  EyeOff,
  Save,
  Edit
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Switch } from './ui/switch';
import { toast } from 'sonner';

const Settings = ({ onLogout, darkMode, onToggleDarkMode }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [editingAccount, setEditingAccount] = useState(false);
  const [editingProfile, setEditingProfile] = useState(false);
  
  // Account information
  const [accountData, setAccountData] = useState({
    email: '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  
  // User profile information
  const [userProfile, setUserProfile] = useState({
    firstName: '',
    lastName: '',
    phone: '',
    timezone: 'America/New_York'
  });

  useEffect(() => {
    // Load user data
    loadUserData();
  }, []);

  const loadUserData = () => {
    // Load from localStorage or API
    const savedEmail = localStorage.getItem('rememberedEmail');
    if (savedEmail) {
      setAccountData(prev => ({ ...prev, email: savedEmail }));
    }
    
    // Load user profile from localStorage
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
      try {
        setUserProfile(JSON.parse(savedProfile));
      } catch (error) {
        console.error('Failed to parse saved profile:', error);
      }
    }
  };

  const handleToggleDarkMode = () => {
    onToggleDarkMode();
    toast.success(`Switched to ${!darkMode ? 'dark' : 'light'} mode`);
  };

  const handleAccountUpdate = async (e) => {
    e.preventDefault();
    
    if (accountData.newPassword && accountData.newPassword !== accountData.confirmPassword) {
      toast.error('New passwords do not match');
      return;
    }
    
    try {
      // Here you would typically make an API call to update account info
      // For demo purposes, we'll just show success
      toast.success('Account information updated successfully');
      setEditingAccount(false);
      setAccountData(prev => ({ 
        ...prev, 
        currentPassword: '', 
        newPassword: '', 
        confirmPassword: '' 
      }));
    } catch (error) {
      toast.error('Failed to update account information');
    }
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    
    try {
      // Save to localStorage for demo
      localStorage.setItem('userProfile', JSON.stringify(userProfile));
      toast.success('Profile information updated successfully');
      setEditingProfile(false);
    } catch (error) {
      toast.error('Failed to update profile information');
    }
  };

  return (
    <div className="container mx-auto px-4 py-6 max-w-4xl">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
          <SettingsIcon className="w-8 h-8 text-blue-600" />
          Settings
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Manage your account preferences and application settings
        </p>
      </div>

      <div className="grid gap-6">
        {/* Appearance Settings */}
        <Card className="glass border-0">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {darkMode ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
              Appearance
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label className="text-base font-medium">Dark Mode</Label>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Switch between light and dark themes
                </p>
              </div>
              <Switch 
                checked={darkMode} 
                onCheckedChange={toggleDarkMode}
              />
            </div>
          </CardContent>
        </Card>

        {/* Account Information */}
        <Card className="glass border-0">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <Lock className="w-5 h-5" />
                Account Information
              </CardTitle>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setEditingAccount(!editingAccount)}
              >
                <Edit className="w-4 h-4 mr-1" />
                {editingAccount ? 'Cancel' : 'Edit'}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAccountUpdate} className="space-y-4">
              <div>
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  value={accountData.email}
                  onChange={(e) => setAccountData(prev => ({ ...prev, email: e.target.value }))}
                  disabled={!editingAccount}
                  className="bg-gray-50 dark:bg-gray-800"
                />
              </div>
              
              {editingAccount && (
                <>
                  <div>
                    <Label htmlFor="currentPassword">Current Password</Label>
                    <div className="relative">
                      <Input
                        id="currentPassword"
                        type={showPassword ? 'text' : 'password'}
                        value={accountData.currentPassword}
                        onChange={(e) => setAccountData(prev => ({ ...prev, currentPassword: e.target.value }))}
                        placeholder="Enter current password"
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3"
                        onClick={() => setShowPassword(!showPassword)}
                      >
                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </Button>
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="newPassword">New Password (Optional)</Label>
                    <Input
                      id="newPassword"
                      type={showPassword ? 'text' : 'password'}
                      value={accountData.newPassword}
                      onChange={(e) => setAccountData(prev => ({ ...prev, newPassword: e.target.value }))}
                      placeholder="Enter new password"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="confirmPassword">Confirm New Password</Label>
                    <Input
                      id="confirmPassword"
                      type={showPassword ? 'text' : 'password'}
                      value={accountData.confirmPassword}
                      onChange={(e) => setAccountData(prev => ({ ...prev, confirmPassword: e.target.value }))}
                      placeholder="Confirm new password"
                    />
                  </div>
                  
                  <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                    <Save className="w-4 h-4 mr-2" />
                    Update Account
                  </Button>
                </>
              )}
            </form>
          </CardContent>
        </Card>

        {/* User Profile */}
        <Card className="glass border-0">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <User className="w-5 h-5" />
                User Information
              </CardTitle>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setEditingProfile(!editingProfile)}
              >
                <Edit className="w-4 h-4 mr-1" />
                {editingProfile ? 'Cancel' : 'Edit'}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleProfileUpdate} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    value={userProfile.firstName}
                    onChange={(e) => setUserProfile(prev => ({ ...prev, firstName: e.target.value }))}
                    disabled={!editingProfile}
                    className="bg-gray-50 dark:bg-gray-800"
                    placeholder="Enter first name"
                  />
                </div>
                <div>
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    value={userProfile.lastName}
                    onChange={(e) => setUserProfile(prev => ({ ...prev, lastName: e.target.value }))}
                    disabled={!editingProfile}
                    className="bg-gray-50 dark:bg-gray-800"
                    placeholder="Enter last name"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="phone">Phone Number</Label>
                <Input
                  id="phone"
                  type="tel"
                  value={userProfile.phone}
                  onChange={(e) => setUserProfile(prev => ({ ...prev, phone: e.target.value }))}
                  disabled={!editingProfile}
                  className="bg-gray-50 dark:bg-gray-800"
                  placeholder="Enter phone number"
                />
              </div>
              
              {editingProfile && (
                <Button type="submit" className="bg-blue-600 hover:bg-blue-700">
                  <Save className="w-4 h-4 mr-2" />
                  Update Profile
                </Button>
              )}
            </form>
          </CardContent>
        </Card>

        {/* Logout Section */}
        <Card className="glass border-0">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium text-gray-900 dark:text-white">Sign Out</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Sign out of your Baby Steps account
                </p>
              </div>
              <Button 
                variant="destructive" 
                onClick={onLogout}
                className="bg-red-600 hover:bg-red-700"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Settings;