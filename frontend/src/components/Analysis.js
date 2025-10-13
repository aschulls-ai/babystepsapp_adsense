import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs';
import { ChevronLeft, ChevronRight, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { format, subDays, parseISO, differenceInMinutes, differenceInHours, differenceInDays } from 'date-fns';
import { androidFetch } from '../App';

const API = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Analysis = ({ currentBaby }) => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState('summary');
  const [dayOffset, setDayOffset] = useState(0); // 0 = today, 1 = yesterday, etc.

  useEffect(() => {
    if (currentBaby) {
      fetchActivities();
    }
  }, [currentBaby]);

  const fetchActivities = async () => {
    if (!currentBaby) return;
    
    console.log('📊 Analysis: Fetching activities for baby:', currentBaby.id);
    
    try {
      const token = localStorage.getItem('token');
      const url = `${API}/api/activities?baby_id=${currentBaby.id}`;
      console.log('📡 Analysis: Fetching from:', url);
      
      const response = await androidFetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('✅ Analysis: Received', data.length, 'activities');
        console.log('Sample activity:', data[0]);
        setActivities(data);
      } else {
        console.error('❌ Analysis: HTTP', response.status);
      }
    } catch (error) {
      console.error('❌ Analysis: Failed to fetch activities:', error);
    } finally {
      setLoading(false);
    }
  };

  // Get activities for a specific day
  const getActivitiesForDay = (offset) => {
    const targetDate = subDays(new Date(), offset);
    return activities.filter(activity => {
      const activityDate = parseISO(activity.timestamp);
      return format(activityDate, 'yyyy-MM-dd') === format(targetDate, 'yyyy-MM-dd');
    });
  };

  // Get activities by type with safe date parsing
  const getActivitiesByType = (type, days = 7) => {
    const cutoffDate = subDays(new Date(), days);
    return activities.filter(activity => {
      if (activity.type !== type) return false;
      try {
        const activityDate = new Date(activity.timestamp);
        return activityDate >= cutoffDate;
      } catch {
        return false;
      }
    });
  };

  // Get measurement activities (any activity with weight, height, or head_circumference)
  const getMeasurementActivities = () => {
    return activities.filter(activity => 
      activity.weight || activity.height || activity.head_circumference
    ).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  };

  // Calculate time since last activity with safe date parsing
  const getTimeSinceLast = (type) => {
    const typeActivities = activities.filter(a => a.type === type);
    if (typeActivities.length === 0) return 'No data';
    
    const latest = typeActivities.sort((a, b) => 
      new Date(b.timestamp) - new Date(a.timestamp)
    )[0];
    
    try {
      const now = new Date();
      const lastTime = new Date(latest.timestamp);
      const hours = differenceInHours(now, lastTime);
      const minutes = differenceInMinutes(now, lastTime) % 60;
      const days = differenceInDays(now, lastTime);
      
      if (days > 0) return `${days}d ${hours % 24}h ${minutes}m`;
      if (hours > 0) return `${hours}h ${minutes}m`;
      return `${minutes}m`;
    } catch {
      return 'Error';
    }
  };

  // Calculate WHO growth percentile
  const calculatePercentile = (measurement, type, ageMonths, gender) => {
    // Simplified WHO percentile calculation (you'd use actual WHO tables)
    // This is a placeholder - implement actual WHO chart lookup
    if (!measurement) return 'N/A';
    
    // For now, return a mock percentile
    // In production, use WHO growth charts data
    return '50th';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!currentBaby) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-gray-500">Please select a baby to view analysis</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analysis</h1>
          <p className="text-gray-600">{currentBaby.name}'s Data</p>
        </div>

        {/* Tabs */}
        <Tabs value={selectedTab} onValueChange={setSelectedTab}>
          <TabsList className="grid grid-cols-5 mb-6 bg-white/80 backdrop-blur-sm">
            <TabsTrigger value="summary">SUMMARY</TabsTrigger>
            <TabsTrigger value="bottle">BOTTLE</TabsTrigger>
            <TabsTrigger value="express">EXPRESS</TabsTrigger>
            <TabsTrigger value="diaper">DIAPER</TabsTrigger>
            <TabsTrigger value="growth">GROWTH</TabsTrigger>
          </TabsList>

          {/* Summary Tab */}
          <TabsContent value="summary">
            <SummaryView 
              activities={activities}
              currentBaby={currentBaby}
              getTimeSinceLast={getTimeSinceLast}
              dayOffset={dayOffset}
              setDayOffset={setDayOffset}
            />
          </TabsContent>

          {/* Bottle Tab */}
          <TabsContent value="bottle">
            <BottleView 
              activities={getActivitiesByType('feeding')}
              currentBaby={currentBaby}
              getTimeSinceLast={getTimeSinceLast}
              dayOffset={dayOffset}
              setDayOffset={setDayOffset}
            />
          </TabsContent>

          {/* Express (Pumping + Breastfeeding) Tab */}
          <TabsContent value="express">
            <ExpressView 
              activities={activities}
              currentBaby={currentBaby}
              getTimeSinceLast={getTimeSinceLast}
              dayOffset={dayOffset}
              setDayOffset={setDayOffset}
            />
          </TabsContent>

          {/* Diaper Tab */}
          <TabsContent value="diaper">
            <DiaperView 
              activities={getActivitiesByType('diaper')}
              currentBaby={currentBaby}
              getTimeSinceLast={getTimeSinceLast}
              dayOffset={dayOffset}
              setDayOffset={setDayOffset}
            />
          </TabsContent>

          {/* Growth Tab */}
          <TabsContent value="growth">
            <GrowthView 
              activities={getMeasurementActivities()}
              currentBaby={currentBaby}
              calculatePercentile={calculatePercentile}
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

// Summary View Component
const SummaryView = ({ activities, currentBaby, getTimeSinceLast, dayOffset, setDayOffset }) => {
  const today = subDays(new Date(), dayOffset);
  const todayActivities = activities.filter(a => 
    format(parseISO(a.timestamp), 'yyyy-MM-dd') === format(today, 'yyyy-MM-dd')
  );

  const feedingCount = todayActivities.filter(a => a.type === 'feeding').length;
  const diaperCount = todayActivities.filter(a => a.type === 'diaper').length;
  const sleepTotal = todayActivities
    .filter(a => a.type === 'sleep')
    .reduce((sum, a) => sum + (a.duration || 0), 0);

  return (
    <div className="space-y-6">
      {/* Date Navigator */}
      <Card className="glass-strong border-0">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setDayOffset(Math.min(dayOffset + 1, 30))}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <div className="text-center">
              <h3 className="text-lg font-semibold">
                {dayOffset === 0 ? 'TODAY' : format(today, 'EEEE')}
              </h3>
              <p className="text-sm text-gray-600">{format(today, 'MMM d, yyyy')}</p>
            </div>
            <button
              onClick={() => setDayOffset(Math.max(dayOffset - 1, 0))}
              disabled={dayOffset === 0}
              className="p-2 hover:bg-gray-100 rounded-lg transition disabled:opacity-50"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Overview */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Overview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-sm text-gray-600">Feedings</p>
              <p className="text-3xl font-bold text-pink-600">{feedingCount}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600">Diapers</p>
              <p className="text-3xl font-bold text-blue-600">{diaperCount}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600">Sleep</p>
              <p className="text-3xl font-bold text-purple-600">
                {Math.floor(sleepTotal / 60)}h {sleepTotal % 60}m
              </p>
            </div>
          </div>

          <div className="pt-4 border-t space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Time since last feed:</span>
              <span className="font-semibold">{getTimeSinceLast('feeding')}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Time since last diaper:</span>
              <span className="font-semibold">{getTimeSinceLast('diaper')}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Bottle View Component
const BottleView = ({ activities, currentBaby, getTimeSinceLast, dayOffset, setDayOffset }) => {
  const bottleFeeds = activities.filter(a => a.feeding_type === 'bottle');
  const today = subDays(new Date(), dayOffset);
  const todayFeeds = bottleFeeds.filter(a => 
    format(parseISO(a.timestamp), 'yyyy-MM-dd') === format(today, 'yyyy-MM-dd')
  );

  const totalAmount = todayFeeds.reduce((sum, a) => sum + (parseFloat(a.amount) || 0), 0);
  const avgAmount = todayFeeds.length > 0 ? (totalAmount / todayFeeds.length).toFixed(1) : 0;

  return (
    <div className="space-y-6">
      {/* Date Navigator */}
      <Card className="glass-strong border-0">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setDayOffset(Math.min(dayOffset + 1, 30))}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <div className="text-center">
              <h3 className="text-lg font-semibold">
                {dayOffset === 0 ? 'TODAY' : format(today, 'EEEE')}
              </h3>
              <p className="text-sm text-gray-600">{format(today, 'MMM d, yyyy')}</p>
            </div>
            <button
              onClick={() => setDayOffset(Math.max(dayOffset - 1, 0))}
              disabled={dayOffset === 0}
              className="p-2 hover:bg-gray-100 rounded-lg transition disabled:opacity-50"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Overview */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Overview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Total amount</span>
            <span className="font-semibold text-orange-600">{totalAmount} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Avg. per feed</span>
            <span className="font-semibold text-orange-600">{avgAmount} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Number of feeds</span>
            <span className="font-semibold text-orange-600">{todayFeeds.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Time since last feed</span>
            <span className="font-semibold text-orange-600">{getTimeSinceLast('feeding')}</span>
          </div>
        </CardContent>
      </Card>

      {/* Trends */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Trends</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm font-semibold mb-2">7 DAY AVERAGE</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Avg. time between feeds</span>
                <span className="font-semibold">-</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg. daily number of feeds</span>
                <span className="font-semibold">-</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Express (Pumping + Breastfeeding) View Component
const ExpressView = ({ activities, currentBaby, getTimeSinceLast, dayOffset, setDayOffset }) => {
  const today = subDays(new Date(), dayOffset);
  
  // Filter for pumping and breastfeeding
  const pumpingActivities = activities.filter(a => a.type === 'pumping');
  const breastfeedingActivities = activities.filter(a => 
    a.type === 'feeding' && (a.feeding_type === 'breast' || a.feeding_type === 'breastfeeding')
  );
  
  // Today's pumping
  const todayPumping = pumpingActivities.filter(a => {
    try {
      return format(new Date(a.timestamp), 'yyyy-MM-dd') === format(today, 'yyyy-MM-dd');
    } catch {
      return false;
    }
  });
  
  // Today's breastfeeding
  const todayBreastfeeding = breastfeedingActivities.filter(a => {
    try {
      return format(new Date(a.timestamp), 'yyyy-MM-dd') === format(today, 'yyyy-MM-dd');
    } catch {
      return false;
    }
  });

  const totalPumpAmount = todayPumping.reduce((sum, a) => sum + (parseFloat(a.amount) || 0), 0);
  const avgPumpAmount = todayPumping.length > 0 ? (totalPumpAmount / todayPumping.length).toFixed(1) : 0;
  const totalBreastDuration = todayBreastfeeding.reduce((sum, a) => sum + (parseInt(a.duration) || 0), 0);
  
  // 7-day averages
  const last7DaysPumping = pumpingActivities.filter(a => {
    try {
      const date = new Date(a.timestamp);
      return date >= subDays(new Date(), 7);
    } catch {
      return false;
    }
  });
  
  const last7DaysBreastfeeding = breastfeedingActivities.filter(a => {
    try {
      const date = new Date(a.timestamp);
      return date >= subDays(new Date(), 7);
    } catch {
      return false;
    }
  });
  
  const avg7DayPumping = last7DaysPumping.length > 0 ? (last7DaysPumping.length / 7).toFixed(1) : 0;
  const avg7DayBreastfeeding = last7DaysBreastfeeding.length > 0 ? (last7DaysBreastfeeding.length / 7).toFixed(1) : 0;

  return (
    <div className="space-y-6">
      {/* Date Navigator */}
      <Card className="glass-strong border-0">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setDayOffset(Math.min(dayOffset + 1, 30))}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <div className="text-center">
              <h3 className="text-lg font-semibold">
                {dayOffset === 0 ? 'TODAY' : format(today, 'EEEE')}
              </h3>
              <p className="text-sm text-gray-600">{format(today, 'MMM d, yyyy')}</p>
            </div>
            <button
              onClick={() => setDayOffset(Math.max(dayOffset - 1, 0))}
              disabled={dayOffset === 0}
              className="p-2 hover:bg-gray-100 rounded-lg transition disabled:opacity-50"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Pumping Overview */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Pumping Overview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Total amount pumped</span>
            <span className="font-semibold text-orange-600">{totalPumpAmount} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Avg. per session</span>
            <span className="font-semibold text-orange-600">{avgPumpAmount} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Number of sessions</span>
            <span className="font-semibold text-orange-600">{todayPumping.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Time since last pumped</span>
            <span className="font-semibold text-orange-600">{getTimeSinceLast('pumping')}</span>
          </div>
        </CardContent>
      </Card>

      {/* Breastfeeding Overview */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Breastfeeding Overview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Total breastfeeding time</span>
            <span className="font-semibold text-pink-600">{Math.floor(totalBreastDuration / 60)}h {totalBreastDuration % 60}m</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Number of sessions</span>
            <span className="font-semibold text-pink-600">{todayBreastfeeding.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Avg. duration per session</span>
            <span className="font-semibold text-pink-600">
              {todayBreastfeeding.length > 0 ? Math.round(totalBreastDuration / todayBreastfeeding.length) : 0} min
            </span>
          </div>
        </CardContent>
      </Card>

      {/* Trends */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Trends</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm font-semibold mb-2">7 DAY AVERAGE</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Avg. pumping sessions per day</span>
                <span className="font-semibold">{avg7DayPumping}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg. breastfeeding sessions per day</span>
                <span className="font-semibold">{avg7DayBreastfeeding}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Diaper View Component
const DiaperView = ({ activities, currentBaby, getTimeSinceLast, dayOffset, setDayOffset }) => {
  const today = subDays(new Date(), dayOffset);
  const todayDiapers = activities.filter(a => {
    try {
      return format(new Date(a.timestamp), 'yyyy-MM-dd') === format(today, 'yyyy-MM-dd');
    } catch {
      return false;
    }
  });

  const wetCount = todayDiapers.filter(a => a.diaper_type === 'wet').length;
  const dirtyCount = todayDiapers.filter(a => a.diaper_type === 'dirty').length;
  const mixedCount = todayDiapers.filter(a => a.diaper_type === 'mixed').length;

  return (
    <div className="space-y-6">
      {/* Date Navigator */}
      <Card className="glass-strong border-0">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setDayOffset(Math.min(dayOffset + 1, 30))}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <div className="text-center">
              <h3 className="text-lg font-semibold">
                {dayOffset === 0 ? 'TODAY' : format(today, 'EEEE')}
              </h3>
              <p className="text-sm text-gray-600">{format(today, 'MMM d, yyyy')}</p>
            </div>
            <button
              onClick={() => setDayOffset(Math.max(dayOffset - 1, 0))}
              disabled={dayOffset === 0}
              className="p-2 hover:bg-gray-100 rounded-lg transition disabled:opacity-50"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Overview */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Overview</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Total number of diapers</span>
            <span className="font-semibold text-blue-600">{todayDiapers.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Number of wet diapers</span>
            <span className="font-semibold text-blue-400">{wetCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Number of dirty diapers</span>
            <span className="font-semibold text-yellow-600">{dirtyCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Number of wet & dirty diapers</span>
            <span className="font-semibold text-orange-600">{mixedCount}</span>
          </div>
        </CardContent>
      </Card>

      {/* Last Diaper */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>Last Diaper</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-4xl font-bold text-blue-600 text-center">
            {getTimeSinceLast('diaper')}
          </div>
          <p className="text-center text-sm text-gray-600 mt-2">Since last Diaper</p>
        </CardContent>
      </Card>
    </div>
  );
};

// Growth View Component
const GrowthView = ({ activities, currentBaby, calculatePercentile }) => {
  const measurements = activities.filter(a => a.weight || a.height || a.head_circumference);
  const latestMeasurement = measurements.length > 0 ? measurements[0] : null;

  // Calculate baby age in months
  const ageMonths = currentBaby.birth_date 
    ? Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44))
    : 0;

  return (
    <div className="space-y-6">
      {/* Weight */}
      {latestMeasurement?.weight && (
        <Card className="glass-strong border-0">
          <CardHeader>
            <CardTitle>Weight</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Date of last measurement</span>
              <span className="font-semibold">
                {format(parseISO(latestMeasurement.timestamp), 'MMM d, yyyy')}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Age at last measurement</span>
              <span className="font-semibold">{ageMonths} months</span>
            </div>
            <div className="flex items-center justify-between pt-4 border-t">
              <div>
                <p className="text-sm text-gray-600">Weight</p>
                <p className="text-4xl font-bold text-green-600">{latestMeasurement.weight}</p>
                <p className="text-sm text-gray-500">lb</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Percentile</p>
                <p className="text-4xl font-bold text-green-600">
                  {calculatePercentile(latestMeasurement.weight, 'weight', ageMonths, currentBaby.gender)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Length */}
      {latestMeasurement?.height && (
        <Card className="glass-strong border-0">
          <CardHeader>
            <CardTitle>Length</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">length</p>
                <p className="text-4xl font-bold text-green-600">{latestMeasurement.height}</p>
                <p className="text-sm text-gray-500">inches</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Percentile</p>
                <p className="text-4xl font-bold text-green-600">
                  {calculatePercentile(latestMeasurement.height, 'height', ageMonths, currentBaby.gender)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Head Circumference */}
      {latestMeasurement?.head_circumference && (
        <Card className="glass-strong border-0">
          <CardHeader>
            <CardTitle>Head Circumference</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Head circumference</p>
                <p className="text-4xl font-bold text-purple-600">{latestMeasurement.head_circumference}</p>
                <p className="text-sm text-gray-500">inches</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600">Percentile</p>
                <p className="text-4xl font-bold text-purple-600">
                  {calculatePercentile(latestMeasurement.head_circumference, 'head', ageMonths, currentBaby.gender)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Analysis;
