import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Plus, Baby, Activity, Apple, BookOpen, Calendar, Heart, TrendingUp, Clock } from 'lucide-react';
import InContentAd from './ads/InContentAd';

const Dashboard = ({ currentBaby, onAddBaby }) => {
  if (!currentBaby) {
    return (
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <div className="flex items-center justify-center min-h-[400px]">
          <Card className="w-full max-w-md text-center">
            <CardHeader>
              <Baby className="h-12 w-12 mx-auto text-green-600 mb-4" />
              <CardTitle>Create Your First Baby Profile</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-6">
                Get started by adding your baby's information to begin tracking their journey.
              </p>
              <Button onClick={onAddBaby} className="w-full">
                <Plus className="h-4 w-4 mr-2" />
                Add Baby Profile
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const currentAge = currentBaby?.birthDate 
    ? Math.floor((new Date() - new Date(currentBaby.birthDate)) / (1000 * 60 * 60 * 24 * 30))
    : 0;

  const quickActions = [
    {
      title: 'Track Activity',
      description: 'Log feeding, sleep, diapers',
      icon: Activity,
      link: '/tracking',
      color: 'bg-blue-500 hover:bg-blue-600',
      iconColor: 'text-blue-500'
    },
    {
      title: 'Food Research',
      description: 'Check food safety & meal ideas',
      icon: Apple,
      link: '/food-research',
      color: 'bg-green-500 hover:bg-green-600',
      iconColor: 'text-green-500'
    },
    {
      title: 'Baby Profile',
      description: 'Update info & milestones',
      icon: Baby,
      link: '/baby-profile',
      color: 'bg-purple-500 hover:bg-purple-600',
      iconColor: 'text-purple-500'
    },
    {
      title: 'Research Hub',
      description: 'Get parenting guidance',
      icon: BookOpen,
      link: '/research',
      color: 'bg-orange-500 hover:bg-orange-600',
      iconColor: 'text-orange-500'
    }
  ];

  const stats = [
    {
      label: 'Baby\'s Age',
      value: `${currentAge} months`,
      icon: Calendar,
      color: 'text-blue-600'
    },
    {
      label: 'Growth',
      value: currentBaby?.weight ? `${currentBaby.weight} lbs` : 'Not tracked',
      icon: TrendingUp,
      color: 'text-green-600'
    },
    {
      label: 'Health',
      value: 'Good',
      icon: Heart,
      color: 'text-red-500'
    },
    {
      label: 'Last Activity',
      value: 'Today',
      icon: Clock,
      color: 'text-purple-600'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-6 max-w-6xl">
      {/* Welcome Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Hello! Welcome back to Baby Steps
        </h1>
        <p className="text-lg text-gray-600">
          Caring for {currentBaby?.name || 'your little one'} • {currentAge} months old
        </p>
      </div>

      {/* Baby Info Card */}
      <Card className="mb-8 bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                <Baby className="h-8 w-8 text-green-600" />
              </div>
              <div>
                <h2 className="text-2xl font-semibold text-gray-900">{currentBaby?.name}</h2>
                <p className="text-gray-600">
                  Born {currentBaby?.birthDate ? new Date(currentBaby.birthDate).toLocaleDateString() : 'Date not set'}
                </p>
              </div>
            </div>
            <Link to="/baby-profile">
              <Button variant="outline" size="sm">
                View Profile
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {stats.map((stat, index) => (
          <Card key={index} className="hover:shadow-md transition-shadow">
            <CardContent className="p-4 text-center">
              <stat.icon className={`h-6 w-6 mx-auto mb-2 ${stat.color}`} />
              <p className="text-sm text-gray-600">{stat.label}</p>
              <p className="text-lg font-semibold text-gray-900">{stat.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <Link key={index} to={action.link} className="block">
              <Card className="hover:shadow-lg transition-all duration-200 hover:scale-105 cursor-pointer group">
                <CardContent className="p-6 text-center">
                  <div className={`w-12 h-12 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center group-hover:bg-white transition-colors`}>
                    <action.icon className={`h-6 w-6 ${action.iconColor}`} />
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">{action.title}</h4>
                  <p className="text-sm text-gray-600">{action.description}</p>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* In-content Ad */}
      <InContentAd />

      {/* Recent Activity Preview */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center">
            <Activity className="h-5 w-5 mr-2 text-blue-600" />
            Recent Activity
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Activity className="h-4 w-4 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">Ready to start tracking!</p>
                  <p className="text-xs text-gray-600">Log your first activity to see it here</p>
                </div>
              </div>
              <Link to="/tracking">
                <Button variant="outline" size="sm">
                  Start Tracking
                </Button>
              </Link>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tips & Guidance */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BookOpen className="h-5 w-5 mr-2 text-green-600" />
            Today's Parenting Tip
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <h4 className="font-semibold text-green-900 mb-2">
              {currentAge < 6 ? '🍼 Feeding Time' : '🥄 Solid Foods'}
            </h4>
            <p className="text-green-800 text-sm">
              {currentAge < 6 
                ? 'Newborns typically feed every 2-3 hours. Look for hunger cues like rooting or fussiness.'
                : 'At this age, you can start introducing more textured foods. Always check our food research for safety!'
              }
            </p>
            <Link to="/food-research" className="inline-block mt-2">
              <Button variant="outline" size="sm" className="border-green-300 text-green-700 hover:bg-green-100">
                Learn More
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Helper Components
const WelcomeCard = ({ onAddBaby }) => (
  <Card className="glass-strong border-0 max-w-md mx-auto text-center">
    <CardContent className="p-8">
      <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
        <Baby className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-2xl font-bold font-display text-gray-900 mb-4">
        Welcome to Baby Steps!
      </h2>
      <p className="text-gray-600 mb-6">
        Let's start by adding your baby's profile to get personalized nutrition guidance and safety information.
      </p>
      <Button
        onClick={() => window.location.href = '/baby-profile'}
        className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="add-first-baby-btn"
      >
        <Plus className="w-5 h-5 mr-2" />
        Add Your Baby
      </Button>
    </CardContent>
  </Card>
);

export default Dashboard;