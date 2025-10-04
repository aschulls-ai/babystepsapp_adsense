import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { 
  Baby, 
  Milk, 
  Clock, 
  Activity, 
  TrendingUp, 
  Heart, 
  Calendar,
  Droplet,
  Moon,
  Plus
} from 'lucide-react';
import { toast } from 'sonner';
import { format, formatDistanceToNow } from 'date-fns';

const Dashboard = ({ currentBaby, onAddBaby }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddBaby, setShowAddBaby] = useState(false);

  useEffect(() => {
    if (currentBaby) {
      fetchDashboardData();
    } else {
      setLoading(false);
    }
  }, [currentBaby]);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get(`/dashboard/${currentBaby.id}`);
      setDashboardData(response.data);
    } catch (error) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (!currentBaby) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <WelcomeCard onAddBaby={onAddBaby} setShowAddBaby={setShowAddBaby} />
      </div>
    );
  }

  if (loading) {
    return <LoadingDashboard />;
  }

  const { baby, recent_feedings, recent_diapers, recent_sleep, next_feeding_prediction, next_pumping_prediction, stats } = dashboardData || {};

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold font-display text-gray-900" data-testid="dashboard-title">
            Welcome back! 👶
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Here's how <span className="font-semibold text-rose-600">{baby.name}</span> is doing today
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-sm text-gray-500">Born</p>
            <p className="font-medium text-gray-900">
              {format(new Date(baby.birth_date), 'MMM dd, yyyy')}
            </p>
          </div>
          <div className="w-16 h-16 bg-gradient-to-br from-rose-400 to-pink-500 rounded-full flex items-center justify-center">
            <Baby className="w-8 h-8 text-white" />
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={<Milk className="w-6 h-6 text-blue-600" />}
          title="Feedings Today"
          value={stats?.total_feedings_today || 0}
          subtitle="Last feeding"
          time={recent_feedings?.[0] ? formatDistanceToNow(new Date(recent_feedings[0].timestamp), { addSuffix: true }) : 'No data'}
          bgColor="from-blue-500 to-cyan-500"
        />
        <StatCard
          icon={<Droplet className="w-6 h-6 text-orange-600" />}
          title="Diapers Today"
          value={stats?.total_diapers_today || 0}
          subtitle="Last change"
          time={recent_diapers?.[0] ? formatDistanceToNow(new Date(recent_diapers[0].timestamp), { addSuffix: true }) : 'No data'}
          bgColor="from-orange-500 to-amber-500"
        />
        <StatCard
          icon={<Moon className="w-6 h-6 text-purple-600" />}
          title="Sleep Sessions"
          value={recent_sleep?.length || 0}
          subtitle="Last sleep"
          time={recent_sleep?.[0] ? formatDistanceToNow(new Date(recent_sleep[0].start_time), { addSuffix: true }) : 'No data'}
          bgColor="from-purple-500 to-violet-500"
        />
        <StatCard
          icon={<Heart className="w-6 h-6 text-rose-600" />}
          title="Days Old"
          value={Math.floor((new Date() - new Date(baby.birth_date)) / (1000 * 60 * 60 * 24))}
          subtitle="Growing strong"
          time="Every day counts"
          bgColor="from-rose-500 to-pink-500"
        />
      </div>

      {/* Predictions & Reminders */}
      <div className="grid lg:grid-cols-2 gap-6">
        <Card className="glass-strong border-0" data-testid="predictions-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-800">
              <Clock className="w-5 h-5 text-rose-500" />
              Smart Predictions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {next_feeding_prediction && (
              <PredictionItem
                icon={<Milk className="w-5 h-5 text-blue-500" />}
                title="Next Feeding"
                time={format(new Date(next_feeding_prediction), 'h:mm a')}
                subtitle={formatDistanceToNow(new Date(next_feeding_prediction), { addSuffix: true })}
                color="blue"
              />
            )}
            {next_pumping_prediction && (
              <PredictionItem
                icon={<Activity className="w-5 h-5 text-purple-500" />}
                title="Next Pumping"
                time={format(new Date(next_pumping_prediction), 'h:mm a')}
                subtitle={formatDistanceToNow(new Date(next_pumping_prediction), { addSuffix: true })}
                color="purple"
              />
            )}
            {!next_feeding_prediction && !next_pumping_prediction && (
              <p className="text-gray-500 text-center py-8">
                Start tracking activities to see smart predictions
              </p>
            )}
          </CardContent>
        </Card>

        <Card className="glass-strong border-0">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-800">
              <TrendingUp className="w-5 h-5 text-green-500" />
              Quick Actions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <QuickActionButton
              icon={<Milk className="w-5 h-5" />}
              title="Log Feeding"
              subtitle="Track bottle or breast feeding"
              href="/tracking?tab=feeding"
              color="blue"
            />
            <QuickActionButton
              icon={<Droplet className="w-5 h-5" />}
              title="Log Diaper"
              subtitle="Record diaper change"
              href="/tracking?tab=diaper"
              color="orange"
            />
            <QuickActionButton
              icon={<Moon className="w-5 h-5" />}
              title="Log Sleep"
              subtitle="Track sleep session"
              href="/tracking?tab=sleep"
              color="purple"
            />
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <div className="grid lg:grid-cols-3 gap-6">
        <ActivityCard
          title="Recent Feedings"
          icon={<Milk className="w-5 h-5 text-blue-500" />}
          activities={recent_feedings?.slice(0, 3) || []}
          renderActivity={(activity) => (
            <ActivityItem
              key={activity.id}
              icon={<Milk className="w-4 h-4 text-blue-500" />}
              title={`${activity.type.charAt(0).toUpperCase() + activity.type.slice(1)} feeding`}
              subtitle={activity.amount ? `${activity.amount} oz` : `${activity.duration || 0} min`}
              time={formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })}
            />
          )}
        />

        <ActivityCard
          title="Recent Diapers"
          icon={<Droplet className="w-5 h-5 text-orange-500" />}
          activities={recent_diapers?.slice(0, 3) || []}
          renderActivity={(activity) => (
            <ActivityItem
              key={activity.id}
              icon={<Droplet className="w-4 h-4 text-orange-500" />}
              title={`${activity.type.charAt(0).toUpperCase() + activity.type.slice(1)} diaper`}
              subtitle="Changed"
              time={formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })}
            />
          )}
        />

        <ActivityCard
          title="Recent Sleep"
          icon={<Moon className="w-5 h-5 text-purple-500" />}
          activities={recent_sleep?.slice(0, 3) || []}
          renderActivity={(activity) => (
            <ActivityItem
              key={activity.id}
              icon={<Moon className="w-4 h-4 text-purple-500" />}
              title="Sleep session"
              subtitle={activity.duration ? `${Math.round(activity.duration / 60)} hours` : 'In progress'}
              time={formatDistanceToNow(new Date(activity.start_time), { addSuffix: true })}
            />
          )}
        />
      </div>
    </div>
  );
};

// Helper Components
const WelcomeCard = ({ onAddBaby }) => (
  <Card className="glass-strong border-0 max-w-md mx-auto text-center">
    <CardContent className="p-8">
      <div className="w-20 h-20 bg-gradient-to-br from-rose-400 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
        <Baby className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-2xl font-bold font-display text-gray-900 mb-4">
        Welcome to Baby Tracker!
      </h2>
      <p className="text-gray-600 mb-6">
        Let's start by adding your little one's profile to begin tracking their journey.
      </p>
      <Button
        onClick={() => window.location.href = '/baby-profile'}
        className="w-full bg-gradient-to-r from-rose-500 to-pink-500 hover:from-rose-600 hover:to-pink-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="add-first-baby-btn"
      >
        <Plus className="w-5 h-5 mr-2" />
        Add Your Baby
      </Button>
    </CardContent>
  </Card>
);

const LoadingDashboard = () => (
  <div className="space-y-6 animate-pulse">
    <div className="h-8 bg-gray-200 rounded w-1/3"></div>
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="h-24 bg-gray-200 rounded-lg"></div>
      ))}
    </div>
    <div className="grid lg:grid-cols-2 gap-6">
      {[...Array(2)].map((_, i) => (
        <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
      ))}
    </div>
  </div>
);

const StatCard = ({ icon, title, value, subtitle, time, bgColor }) => (
  <Card className="stat-card hover:scale-105 transition-all duration-300" data-testid={`stat-${title.toLowerCase().replace(/\s+/g, '-')}`}>
    <CardContent className="p-4">
      <div className="flex items-center justify-between mb-3">
        <div className={`p-2 rounded-lg bg-gradient-to-br ${bgColor} text-white`}>
          {icon}
        </div>
        <div className="text-right">
          <div className="stat-number text-2xl">{value}</div>
        </div>
      </div>
      <h3 className="font-medium text-gray-900 text-sm">{title}</h3>
      <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
      <p className="text-xs text-gray-400 mt-1">{time}</p>
    </CardContent>
  </Card>
);

const PredictionItem = ({ icon, title, time, subtitle, color }) => (
  <div className="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-100">
    <div className={`p-2 rounded-lg bg-${color}-100`}>
      {icon}
    </div>
    <div className="flex-1">
      <h4 className="font-medium text-gray-900">{title}</h4>
      <p className={`text-sm text-${color}-600 font-medium`}>{time}</p>
      <p className="text-xs text-gray-500">{subtitle}</p>
    </div>
  </div>
);

const QuickActionButton = ({ icon, title, subtitle, href, color }) => (
  <Button
    variant="outline"
    className="w-full justify-start p-4 h-auto hover:bg-gray-50 border-gray-200"
    onClick={() => window.location.href = href}
    data-testid={`quick-action-${title.toLowerCase().replace(/\s+/g, '-')}`}
  >
    <div className={`p-2 rounded-lg bg-${color}-100 text-${color}-600 mr-3`}>
      {icon}
    </div>
    <div className="text-left">
      <div className="font-medium text-gray-900">{title}</div>
      <div className="text-sm text-gray-500">{subtitle}</div>
    </div>
  </Button>
);

const ActivityCard = ({ title, icon, activities, renderActivity }) => (
  <Card className="glass border-0">
    <CardHeader>
      <CardTitle className="flex items-center gap-2 text-gray-800 text-lg">
        {icon}
        {title}
      </CardTitle>
    </CardHeader>
    <CardContent>
      {activities.length > 0 ? (
        <div className="space-y-3">
          {activities.map(renderActivity)}
        </div>
      ) : (
        <p className="text-gray-500 text-center py-4">No recent activity</p>
      )}
    </CardContent>
  </Card>
);

const ActivityItem = ({ icon, title, subtitle, time }) => (
  <div className="activity-item">
    <div className="activity-icon">
      {icon}
    </div>
    <div className="flex-1">
      <h4 className="font-medium text-gray-900">{title}</h4>
      <p className="text-sm text-gray-600">{subtitle}</p>
      <p className="text-xs text-gray-400">{time}</p>
    </div>
  </div>
);

export default Dashboard;