import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Home, 
  Baby, 
  Activity, 
  BookOpen, 
  LogOut, 
  Menu,
  X,
  Heart
} from 'lucide-react';
import { useState } from 'react';

const Layout = ({ children, currentBaby, babies, onSwitchBaby, onLogout }) => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Baby Profile', href: '/baby-profile', icon: Baby },
    { name: 'Track Activities', href: '/tracking', icon: Activity },
    { name: 'Research & Tips', href: '/research', icon: BookOpen },
  ];

  const isActive = (href) => location.pathname === href;

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-white to-blue-50">
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          variant="outline"
          size="sm"
          className="bg-white/90 backdrop-blur-sm border-rose-200"
          data-testid="mobile-menu-toggle"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </Button>
      </div>

      {/* Mobile menu overlay */}
      {mobileMenuOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-72 bg-white/95 backdrop-blur-xl border-r border-rose-100 transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${
        mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-center h-16 px-6 border-b border-rose-100 bg-gradient-to-r from-rose-500 to-pink-500 text-white">
            <Heart className="w-6 h-6 mr-2" />
            <h1 className="text-xl font-bold font-display">Baby Tracker</h1>
          </div>

          {/* Baby Selector */}
          {babies.length > 0 && (
            <div className="p-4 border-b border-rose-100 bg-rose-50/50">
              <label className="text-sm font-medium text-gray-700 mb-2 block">
                Select Baby
              </label>
              <Select
                value={currentBaby?.id || ''}
                onValueChange={(value) => {
                  const baby = babies.find(b => b.id === value);
                  if (baby) onSwitchBaby(baby);
                }}
              >
                <SelectTrigger 
                  className="w-full bg-white border-rose-200"
                  data-testid="baby-selector"
                >
                  <SelectValue placeholder="Select a baby" />
                </SelectTrigger>
                <SelectContent>
                  {babies.map((baby) => (
                    <SelectItem key={baby.id} value={baby.id}>
                      <div className="flex items-center gap-2">
                        <Baby className="w-4 h-4 text-rose-500" />
                        {baby.name}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`nav-link ${isActive(item.href) ? 'active' : ''}`}
                  data-testid={`nav-${item.name.toLowerCase().replace(/\s+/g, '-')}`}
                >
                  <Icon className="w-5 h-5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-rose-100">
            <Button
              onClick={onLogout}
              variant="outline"
              className="w-full justify-start text-red-600 border-red-200 hover:bg-red-50"
              data-testid="logout-btn"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-72">
        <main className="min-h-screen p-4 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;