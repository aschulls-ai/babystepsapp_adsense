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
import AdRemovalSettings from './AdRemovalSettings';

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

  const loadUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No auth token found');
        toast.error('Please login again');
        return;
      }

      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/user/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const userData = await response.json();
        setAccountData(prev => ({ 
          ...prev, 
          email: userData.email 
        }));
        
        // Parse name into first and last name
        const nameParts = userData.name.split(' ');
        setUserProfile({
          firstName: nameParts[0] || '',
          lastName: nameParts.slice(1).join(' ') || '',
          phone: userProfile.phone,
          timezone: userProfile.timezone
        });
      } else {
        console.error('Failed to fetch user profile');
        toast.error('Failed to load profile data');
      }
    } catch (error) {
      console.error('Error loading user data:', error);
      toast.error('Failed to load profile data');
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
    
    if (!accountData.currentPassword) {
      toast.error('Current password is required');
      return;
    }
    
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        toast.error('Please login again');
        return;
      }

      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/user/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: accountData.email,
          current_password: accountData.currentPassword,
          new_password: accountData.newPassword || undefined
        })
      });

      if (response.ok) {
        const result = await response.json();
        
        // If email was changed, update token
        if (result.token) {
          localStorage.setItem('token', result.token);
          toast.success('Email updated! Please use your new email to login next time.');
        } else {
          toast.success(result.message || 'Account information updated successfully');
        }
        
        setEditingAccount(false);
        setAccountData(prev => ({ 
          ...prev, 
          currentPassword: '', 
          newPassword: '', 
          confirmPassword: '' 
        }));
        
        // Reload user data
        await loadUserData();
      } else {
        const error = await response.json();
        toast.error(error.detail || 'Failed to update account information');
      }
    } catch (error) {
      console.error('Account update error:', error);
      toast.error('Failed to update account information');
    }
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        toast.error('Please login again');
        return;
      }

      const fullName = `${userProfile.firstName} ${userProfile.lastName}`.trim();
      
      if (!fullName) {
        toast.error('Please enter your name');
        return;
      }
      
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/user/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: fullName
        })
      });

      if (response.ok) {
        const result = await response.json();
        toast.success(result.message || 'Profile information updated successfully');
        setEditingProfile(false);
        
        // Reload user data
        await loadUserData();
      } else {
        const error = await response.json();
        toast.error(error.detail || 'Failed to update profile information');
      }
    } catch (error) {
      console.error('Profile update error:', error);
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
                onCheckedChange={handleToggleDarkMode}
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