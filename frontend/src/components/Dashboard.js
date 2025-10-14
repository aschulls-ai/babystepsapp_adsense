import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Plus, Baby, Activity, Apple, BookOpen, Calendar, Heart, TrendingUp, Clock } from 'lucide-react';
import InContentAd from './ads/InContentAd';
import PageAd from './ads/PageAd';
import FeedReminder from './FeedReminder';

const getMilestonesForAge = (ageMonths) => {
  const milestones = {
    0: [
      "Follows objects with eyes",
      "Lifts head briefly when on tummy", 
      "Responds to loud sounds",
      "Focuses on faces 8-12 inches away"
    ],
    1: [
      "Smiles responsively",
      "Follows objects past midline",
      "Holds head up 45 degrees",
      "Makes cooing sounds"
    ],
    2: [
      "Holds head steady when upright",
      "Pushes up on arms during tummy time",
      "Begins to laugh and squeal",
      "Tracks objects with eyes smoothly"
    ],
    3: [
      "Reaches for and grabs objects",
      "Holds head up 90 degrees",
      "Bears weight on legs when supported",
      "Babbles with expression"
    ],
    4: [
      "Rolls from tummy to back",
      "Brings hands together",
      "Laughs out loud",
      "Shows excitement when seeing food"
    ],
    5: [
      "Rolls from back to tummy",
      "Sits with support",
      "Shows curiosity about objects",
      "Recognizes familiar people"
    ],
    6: [
      "Sits without support briefly",
      "Transfers objects hand to hand",
      "Starts eating solid foods",
      "Responds to own name"
    ],
    9: [
      "Crawls or scoots",
      "Pulls to standing position",
      "Says 'mama' and 'dada'",
      "Plays peek-a-boo"
    ],
    12: [
      "Takes first steps",
      "Says first words",
      "Drinks from a cup",
      "Waves goodbye"
    ],
    15: [
      "Walks independently",
      "Uses 10-20 words",
      "Stacks 2 blocks",
      "Points to body parts"
    ],
    18: [
      "Runs and climbs stairs",
      "Uses 20-50 words",
      "Feeds self with utensils",
      "Shows affection to familiar people"
    ]
  };

  // Find the appropriate milestone set for the age
  const ageKeys = Object.keys(milestones).map(Number).sort((a, b) => a - b);
  let appropriateAge = 0;
  
  for (let i = 0; i < ageKeys.length; i++) {
    if (ageMonths >= ageKeys[i]) {
      appropriateAge = ageKeys[i];
    } else {
      break;
    }
  }
  
  return milestones[appropriateAge] || [];
};

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
              <Button onClick={() => window.location.href = '/baby-profile'} className="w-full">
                <Plus className="h-4 w-4 mr-2" />
                Add Baby Profile
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const currentAge = currentBaby?.birth_date 
    ? Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44))
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
      title: 'Formula Comparison',
      description: 'Compare baby formulas',
      icon: Heart,
      link: '/formula-comparison',
      color: 'bg-pink-500 hover:bg-pink-600',
      iconColor: 'text-pink-500'
    },
    {
      title: 'Baby Profile',
      description: 'Update info & milestones',
      icon: Baby,
      link: '/baby-profile',
      color: 'bg-purple-500 hover:bg-purple-600',
      iconColor: 'text-purple-500'
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
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Hello! Welcome back to Baby Steps
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          Caring for {currentBaby?.name || 'your little one'} • {currentAge} months old
        </p>
      </div>

      {/* Baby Info Card */}
      <Card className="mb-8 bg-gradient-to-r from-green-50 to-blue-50 dark:from-gray-800 dark:to-gray-700 border-green-200 dark:border-gray-600">
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-green-100 dark:bg-green-800 rounded-full flex items-center justify-center">
                <Baby className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">{currentBaby?.name}</h2>
                <p className="text-gray-600 dark:text-gray-300">
                  Born {currentBaby?.birth_date ? new Date(currentBaby.birth_date).toLocaleDateString() : 'Date not set'}
                </p>
              </div>
            </div>
            <Link to="/baby-profile">
              <Button variant="outline" size="sm">
                View Profile
              </Button>
            </Link>
          </div>
          
          {/* Current Milestones */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-green-100 dark:border-gray-700 mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 flex items-center">
              <Calendar className="h-5 w-5 mr-2 text-green-600 dark:text-green-400" />
              Current Milestones ({currentAge} months)
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {getMilestonesForAge(currentAge).map((milestone, index) => (
                <div key={index} className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-green-500 dark:bg-green-400 rounded-full mt-2 flex-shrink-0"></div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">{milestone}</p>
                </div>
              ))}
            </div>
            {getMilestonesForAge(currentAge).length === 0 && (
              <p className="text-sm text-gray-500 dark:text-gray-400 italic">
                Keep tracking! Milestones will appear as your baby grows.
              </p>
            )}
          </div>

          {/* Feed Reminder */}
          <FeedReminder currentBaby={currentBaby} />
        </CardContent>
      </Card>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {stats.map((stat, index) => (
          <Card key={index} className="hover:shadow-md transition-shadow bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-600">
            <CardContent className="p-4 text-center">
              <stat.icon className={`h-6 w-6 mx-auto mb-2 ${stat.color}`} />
              <p className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">{stat.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <Link key={index} to={action.link} className="block">
              <Card className="hover:shadow-lg transition-all duration-200 hover:scale-105 cursor-pointer group bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-600">
                <CardContent className="p-6 text-center">
                  <div className={`w-12 h-12 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center group-hover:bg-white dark:group-hover:bg-gray-600 transition-colors`}>
                    <action.icon className={`h-6 w-6 ${action.iconColor}`} />
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-2">{action.title}</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{action.description}</p>
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
            <div className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                  <Activity className="h-4 w-4 text-blue-600 dark:text-blue-300" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">Ready to start tracking!</p>
                  <p className="text-xs text-gray-600 dark:text-gray-400">Log your first activity to see it here</p>
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

      {/* Page Ad */}
      <PageAd position="bottom" />
    </div>
  );
};

export default Dashboard;