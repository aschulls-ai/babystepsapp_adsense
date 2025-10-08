import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Home, 
  Baby, 
  Activity,
  Search, 
  ShieldAlert, 
  ChefHat,
  BookOpen,
  LogOut, 
  Menu,
  X,
  Utensils,
  Settings
} from 'lucide-react';
import { useState } from 'react';

const Layout = ({ children, currentBaby, babies, onSwitchBaby, onLogout }) => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Baby Profile', href: '/baby-profile', icon: Baby },
    { name: 'Track Activities', href: '/tracking', icon: Activity },
    { name: 'Food Research', href: '/food-research', icon: Search },
    { name: 'Formula Comparison', href: '/formula-comparison', icon: Utensils },
    { name: 'Emergency Training', href: '/emergency-training', icon: ShieldAlert },
    { name: 'Meal Planner', href: '/meal-planner', icon: ChefHat },
    { name: 'Research & Tips', href: '/research', icon: BookOpen },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  const isActive = (href) => location.pathname === href;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors">
      {/* Mobile menu button - Made bigger for better usability */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          variant="outline"
          size="lg"
          className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm border-green-200 dark:border-gray-600 w-14 h-14 p-0 shadow-lg dark:text-white"
          data-testid="mobile-menu-toggle"
        >
          {mobileMenuOpen ? <X className="w-8 h-8" /> : <Menu className="w-8 h-8" />}
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
      <div className={`fixed inset-y-0 left-0 z-50 w-72 bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl border-r border-green-100 dark:border-gray-700 transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${
        mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-center h-16 px-6 border-b border-green-100 dark:border-gray-700 bg-gradient-to-r from-green-500 to-emerald-500 dark:from-green-600 dark:to-emerald-600 text-white">
            <Utensils className="w-6 h-6 mr-2" />
            <h1 className="text-xl font-bold font-display">Baby Steps</h1>
          </div>

          {/* Baby Selector */}
          {babies.length > 0 && (
            <div className="p-4 border-b border-green-100 dark:border-gray-700 bg-green-50/50 dark:bg-gray-800/50">
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
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
                  className="w-full bg-white dark:bg-gray-800 border-green-200 dark:border-gray-600 dark:text-white"
                  data-testid="baby-selector"
                >
                  <SelectValue placeholder="Select a baby">
                    {currentBaby ? (
                      <div className="flex items-center gap-2">
                        <Baby className="w-4 h-4 text-green-500" />
                        {currentBaby.name}
                      </div>
                    ) : null}
                  </SelectValue>
                </SelectTrigger>
                <SelectContent>
                  {babies.map((baby) => (
                    <SelectItem key={baby.id} value={baby.id}>
                      <div className="flex items-center gap-2">
                        <Baby className="w-4 h-4 text-green-500" />
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
              const isEmergency = item.href === '/emergency-training';
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`nav-link ${isActive(item.href) ? 'active' : ''} ${
                    isEmergency ? 'emergency-nav-link' : ''
                  }`}
                  data-testid={`nav-${item.name.toLowerCase().replace(/\s+/g, '-')}`}
                >
                  <Icon className="w-5 h-5" />
                  {item.name}
                  {isEmergency && (
                    <span className="ml-auto text-xs bg-red-100 text-red-600 px-2 py-1 rounded-full">
                      Emergency
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>

          {/* Disclaimer */}
          <div className="p-4 border-t border-green-100 dark:border-gray-700 bg-yellow-50 dark:bg-yellow-900/30">
            <div className="text-xs text-gray-600 dark:text-gray-300">
              <p className="font-medium text-gray-800 dark:text-yellow-200 mb-1">⚠️ Important Notice</p>
              <p>This app provides educational content only. Always consult your pediatrician for medical advice.</p>
            </div>
          </div>

        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-72">
        <main className="min-h-screen p-4 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
          
          {/* Footer */}
          <footer className="max-w-7xl mx-auto px-4 lg:px-8 py-6 border-t border-gray-200 dark:border-gray-700 mt-12">
            <div className="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
              <div>
                <p>&copy; 2025 Baby Steps. All rights reserved.</p>
              </div>
              <div className="flex items-center gap-4">
                <Link 
                  to="/privacy-policy" 
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 underline"
                >
                  Privacy Policy
                </Link>
                <span>•</span>
                <a 
                  href="mailto:support@babysteps.app" 
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 underline"
                >
                  Contact Support
                </a>
              </div>
            </div>
          </footer>
        </main>
      </div>

      <style jsx>{`
        .nav-link {
          @apply flex items-center gap-3 px-3 py-2 text-sm font-medium text-gray-700 rounded-lg transition-all duration-200 hover:bg-green-100 hover:text-green-700;
        }
        
        .dark .nav-link {
          @apply text-gray-300 hover:bg-gray-700 hover:text-white;
        }
        
        .nav-link.active {
          @apply bg-green-500 text-white shadow-md;
        }
        
        .dark .nav-link.active {
          @apply bg-green-600 text-white;
        }
        
        .emergency-nav-link {
          @apply flex items-center gap-3 px-3 py-2 text-sm font-medium text-red-700 rounded-lg transition-all duration-200 hover:bg-red-100 hover:text-red-800 animate-pulse;
        }
        
        .dark .emergency-nav-link {
          @apply text-red-400 hover:bg-red-900/30 hover:text-red-300;
        }
        
        .emergency-nav-link:hover {
          background: rgba(239, 68, 68, 0.1) !important;
          color: #ef4444 !important;
        }
        
        .dark .emergency-nav-link:hover {
          background: rgba(239, 68, 68, 0.2) !important;
          color: #fca5a5 !important;
        }
      `}</style>
    </div>
  );
};

export default Layout;