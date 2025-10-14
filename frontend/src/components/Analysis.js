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

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, []);

  useEffect(() => {
    if (currentBaby) {
      fetchActivities();
    }
  }, [currentBaby]);

  const fetchActivities = async () => {
    if (!currentBaby) {
      console.log('❌ Analysis: No current baby');
      return;
    }

    console.log('📊 Analysis: Fetching activities for baby:', currentBaby.id);

    try {
      // EXACTLY match TrackingPage fetchAllActivities implementation
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
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ Analysis: Received', data.length, 'activities');
      console.log('📋 Sample activity:', data[0]);
      
      // Add display type for consistency with Activity History
      const activitiesWithDisplayType = data.map(activity => ({
        ...activity,
        activity_type: activity.type,
        display_type: activity.type.charAt(0).toUpperCase() + activity.type.slice(1)
      }));
      
      setActivities(activitiesWithDisplayType);
      console.log('💾 Analysis: Activities stored in state');
    } catch (error) {
      console.error('❌ Analysis: Failed to fetch all activities:', error);
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
    // WHO growth standard percentile calculation
    if (!measurement || ageMonths === undefined) return 'N/A';
    
    // WHO growth chart reference data (50th percentile values)
    // Weight in lbs, height in inches, head in inches
    const whoData = {
      weight: {
        boy: [7.5, 9.6, 11.5, 13.0, 14.2, 15.3, 16.3, 17.1, 17.8, 18.5, 19.1, 19.7, 20.2, 20.7, 21.2, 21.6, 22.0, 22.4, 22.8, 23.1, 23.5, 23.8, 24.2, 24.5],
        girl: [7.0, 9.0, 10.8, 12.2, 13.3, 14.3, 15.2, 15.9, 16.5, 17.1, 17.7, 18.2, 18.7, 19.2, 19.6, 20.1, 20.5, 20.9, 21.3, 21.7, 22.0, 22.4, 22.8, 23.1]
      },
      height: {
        boy: [19.7, 21.7, 23.2, 24.4, 25.4, 26.2, 26.9, 27.6, 28.2, 28.7, 29.2, 29.7, 30.2, 30.6, 31.0, 31.4, 31.8, 32.2, 32.6, 32.9, 33.3, 33.6, 34.0, 34.3],
        girl: [19.3, 21.3, 22.7, 23.9, 24.9, 25.7, 26.4, 27.1, 27.7, 28.2, 28.7, 29.2, 29.6, 30.0, 30.4, 30.8, 31.2, 31.6, 31.9, 32.3, 32.6, 33.0, 33.3, 33.6]
      },
      head: {
        boy: [13.8, 15.2, 16.1, 16.7, 17.1, 17.5, 17.8, 18.0, 18.2, 18.4, 18.6, 18.7, 18.9, 19.0, 19.1, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, 19.9, 20.0, 20.0],
        girl: [13.5, 14.9, 15.7, 16.3, 16.7, 17.1, 17.3, 17.6, 17.8, 18.0, 18.1, 18.3, 18.4, 18.5, 18.7, 18.8, 18.9, 19.0, 19.1, 19.2, 19.3, 19.4, 19.4, 19.5]
      }
    };
    
    // WHO standard deviations (SD) for z-score calculation
    const whoSD = {
      weight: {
        boy: [1.1, 1.3, 1.5, 1.6, 1.7, 1.8, 1.9, 1.9, 2.0, 2.0, 2.1, 2.1, 2.2, 2.2, 2.3, 2.3, 2.4, 2.4, 2.5, 2.5, 2.6, 2.6, 2.7, 2.7],
        girl: [1.0, 1.2, 1.4, 1.5, 1.6, 1.7, 1.7, 1.8, 1.9, 1.9, 2.0, 2.0, 2.1, 2.1, 2.2, 2.2, 2.3, 2.3, 2.4, 2.4, 2.5, 2.5, 2.6, 2.6]
      },
      height: {
        boy: [0.9, 1.0, 1.1, 1.1, 1.2, 1.2, 1.2, 1.3, 1.3, 1.3, 1.3, 1.4, 1.4, 1.4, 1.4, 1.5, 1.5, 1.5, 1.5, 1.6, 1.6, 1.6, 1.6, 1.7],
        girl: [0.9, 1.0, 1.0, 1.1, 1.1, 1.1, 1.2, 1.2, 1.2, 1.2, 1.3, 1.3, 1.3, 1.3, 1.3, 1.4, 1.4, 1.4, 1.4, 1.5, 1.5, 1.5, 1.5, 1.5]
      },
      head: {
        boy: [0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6],
        girl: [0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
      }
    };
    
    // Determine gender
    const genderKey = (gender === 'girl' || gender === 'female') ? 'girl' : 'boy';
    
    // Get reference values for the age (limit to available data)
    const ageIndex = Math.min(Math.floor(ageMonths), whoData[type][genderKey].length - 1);
    const median = whoData[type]?.[genderKey]?.[ageIndex];
    const sd = whoSD[type]?.[genderKey]?.[ageIndex];
    
    if (!median || !sd) return '50th';
    
    // Calculate z-score: (measurement - median) / SD
    const zScore = (measurement - median) / sd;
    
    // Convert z-score to percentile
    // z-score to percentile mapping (standard normal distribution)
    if (zScore >= 2.5) return '99th';
    if (zScore >= 2.0) return '98th';
    if (zScore >= 1.88) return '97th';
    if (zScore >= 1.75) return '96th';
    if (zScore >= 1.645) return '95th';
    if (zScore >= 1.5) return '93rd';
    if (zScore >= 1.28) return '90th';
    if (zScore >= 1.04) return '85th';
    if (zScore >= 0.84) return '80th';
    if (zScore >= 0.67) return '75th';
    if (zScore >= 0.52) return '70th';
    if (zScore >= 0.25) return '60th';
    if (zScore >= 0) return '55th';
    if (zScore >= -0.25) return '45th';
    if (zScore >= -0.52) return '35th';
    if (zScore >= -0.67) return '25th';
    if (zScore >= -0.84) return '20th';
    if (zScore >= -1.04) return '15th';
    if (zScore >= -1.28) return '10th';
    if (zScore >= -1.645) return '5th';
    if (zScore >= -1.88) return '3rd';
    return '1st';
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
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Analysis</h1>
          <p className="text-gray-600 dark:text-gray-300">{currentBaby.name}'s Data</p>
        </div>

        {/* Tabs */}
        <Tabs value={selectedTab} onValueChange={setSelectedTab}>
          <TabsList className="grid grid-cols-5 mb-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm">
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
              <p className="text-sm text-gray-600 dark:text-gray-300">{format(today, 'MMM d, yyyy')}</p>
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
              <p className="text-sm text-gray-600 dark:text-gray-300">Feedings</p>
              <p className="text-3xl font-bold text-pink-600">{feedingCount}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600 dark:text-gray-300">Diapers</p>
              <p className="text-3xl font-bold text-blue-600">{diaperCount}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600 dark:text-gray-300">Sleep</p>
              <p className="text-3xl font-bold text-purple-600">
                {Math.floor(sleepTotal / 60)}h {sleepTotal % 60}m
              </p>
            </div>
          </div>

          <div className="pt-4 border-t space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Time since last feed:</span>
              <span className="font-semibold">{getTimeSinceLast('feeding')}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Time since last diaper:</span>
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
              <p className="text-sm text-gray-600 dark:text-gray-300">{format(today, 'MMM d, yyyy')}</p>
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
            <span className="text-gray-600 dark:text-gray-300">Total amount</span>
            <span className="font-semibold text-orange-600">{totalAmount} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Avg. per feed</span>
            <span className="font-semibold text-orange-600">{avgAmount} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Number of feeds</span>
            <span className="font-semibold text-orange-600">{todayFeeds.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Time since last feed</span>
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
              {(() => {
                // Calculate 7-day averages
                const last7Days = [...Array(7)].map((_, i) => subDays(new Date(), i));
                const feedsByDay = last7Days.map(day => {
                  const dayFeeds = bottleFeeds.filter(a => {
                    try {
                      return format(new Date(a.timestamp), 'yyyy-MM-dd') === format(day, 'yyyy-MM-dd');
                    } catch {
                      return false;
                    }
                  });
                  return {
                    count: dayFeeds.length,
                    totalOz: dayFeeds.reduce((sum, a) => sum + (parseFloat(a.amount) || 0), 0)
                  };
                });
                
                const avgDailyFeeds = (feedsByDay.reduce((sum, day) => sum + day.count, 0) / 7).toFixed(1);
                const avgDailyOz = (feedsByDay.reduce((sum, day) => sum + day.totalOz, 0) / 7).toFixed(1);
                
                // Calculate avg time between feeds (in hours)
                const allFeedTimes = bottleFeeds
                  .filter(a => {
                    try {
                      const feedDate = new Date(a.timestamp);
                      return feedDate >= subDays(new Date(), 7);
                    } catch {
                      return false;
                    }
                  })
                  .map(a => new Date(a.timestamp).getTime())
                  .sort((a, b) => a - b);
                
                let avgTimeBetween = '-';
                if (allFeedTimes.length > 1) {
                  const intervals = [];
                  for (let i = 1; i < allFeedTimes.length; i++) {
                    intervals.push(allFeedTimes[i] - allFeedTimes[i - 1]);
                  }
                  const avgMs = intervals.reduce((sum, interval) => sum + interval, 0) / intervals.length;
                  const avgHours = Math.floor(avgMs / (1000 * 60 * 60));
                  const avgMinutes = Math.round((avgMs % (1000 * 60 * 60)) / (1000 * 60));
                  avgTimeBetween = avgHours > 0 ? `${avgHours}h ${avgMinutes}m` : `${avgMinutes}m`;
                }
                
                return (
                  <>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-300">Avg. ounces per day</span>
                      <span className="font-semibold text-orange-600">{avgDailyOz} oz</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-300">Avg. daily number of feeds</span>
                      <span className="font-semibold text-orange-600">{avgDailyFeeds}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-300">Avg. time between feeds</span>
                      <span className="font-semibold text-orange-600">{avgTimeBetween}</span>
                    </div>
                  </>
                );
              })()}
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
  const totalLeftBreast = todayPumping.reduce((sum, a) => sum + (parseFloat(a.left_breast) || 0), 0);
  const totalRightBreast = todayPumping.reduce((sum, a) => sum + (parseFloat(a.right_breast) || 0), 0);
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
  
  // 7-day totals for left/right breast
  const avg7DayLeftBreast = last7DaysPumping.length > 0 
    ? (last7DaysPumping.reduce((sum, a) => sum + (parseFloat(a.left_breast) || 0), 0) / 7).toFixed(1) 
    : '0';
  const avg7DayRightBreast = last7DaysPumping.length > 0 
    ? (last7DaysPumping.reduce((sum, a) => sum + (parseFloat(a.right_breast) || 0), 0) / 7).toFixed(1) 
    : '0';
  const avg7DayTotalOz = last7DaysPumping.length > 0 
    ? (last7DaysPumping.reduce((sum, a) => sum + (parseFloat(a.amount) || 0), 0) / 7).toFixed(1) 
    : '0';

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
              <p className="text-sm text-gray-600 dark:text-gray-300">{format(today, 'MMM d, yyyy')}</p>
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
            <span className="text-gray-600 dark:text-gray-300">Total amount pumped</span>
            <span className="font-semibold text-orange-600">{totalPumpAmount.toFixed(1)} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Left breast total</span>
            <span className="font-semibold text-blue-600">{totalLeftBreast.toFixed(1)} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Right breast total</span>
            <span className="font-semibold text-purple-600">{totalRightBreast.toFixed(1)} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Avg. per session</span>
            <span className="font-semibold text-orange-600">{avgPumpAmount} oz</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Number of sessions</span>
            <span className="font-semibold text-orange-600">{todayPumping.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Time since last pumped</span>
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
            <span className="text-gray-600 dark:text-gray-300">Total breastfeeding time</span>
            <span className="font-semibold text-pink-600">{Math.floor(totalBreastDuration / 60)}h {totalBreastDuration % 60}m</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Number of sessions</span>
            <span className="font-semibold text-pink-600">{todayBreastfeeding.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Avg. duration per session</span>
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
            <p className="text-sm font-semibold mb-2">7 DAY AVERAGE - PUMPING</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Avg. total ounces per day</span>
                <span className="font-semibold text-orange-600">{avg7DayTotalOz} oz</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Avg. left breast per day</span>
                <span className="font-semibold text-blue-600">{avg7DayLeftBreast} oz</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Avg. right breast per day</span>
                <span className="font-semibold text-purple-600">{avg7DayRightBreast} oz</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Avg. pumping sessions per day</span>
                <span className="font-semibold text-orange-600">{avg7DayPumping}</span>
              </div>
            </div>
          </div>
          <div>
            <p className="text-sm font-semibold mb-2">7 DAY AVERAGE - BREASTFEEDING</p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Avg. breastfeeding sessions per day</span>
                <span className="font-semibold text-pink-600">{avg7DayBreastfeeding}</span>
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
              <p className="text-sm text-gray-600 dark:text-gray-300">{format(today, 'MMM d, yyyy')}</p>
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
            <span className="text-gray-600 dark:text-gray-300">Total number of diapers</span>
            <span className="font-semibold text-blue-600">{todayDiapers.length}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Number of wet diapers</span>
            <span className="font-semibold text-blue-400">{wetCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Number of dirty diapers</span>
            <span className="font-semibold text-yellow-600">{dirtyCount}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-300">Number of wet & dirty diapers</span>
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

      {/* 7-Day Trends */}
      <Card className="glass-strong border-0">
        <CardHeader>
          <CardTitle>7-Day Trends</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(7)].map((_, index) => {
              const dayDate = subDays(new Date(), 6 - index);
              const dayDiapers = activities.filter(a => {
                try {
                  return format(new Date(a.timestamp), 'yyyy-MM-dd') === format(dayDate, 'yyyy-MM-dd');
                } catch {
                  return false;
                }
              });
              
              const dayWet = dayDiapers.filter(a => a.diaper_type === 'wet').length;
              const dayDirty = dayDiapers.filter(a => a.diaper_type === 'dirty').length;
              const dayMixed = dayDiapers.filter(a => a.diaper_type === 'mixed').length;
              const totalCount = dayDiapers.length;
              
              return (
                <div key={index} className="border-b border-gray-200 pb-3 last:border-0">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">{format(dayDate, 'EEE, MMM d')}</span>
                    <span className="font-bold text-blue-600">{totalCount} total</span>
                  </div>
                  {totalCount > 0 && (
                    <div className="flex gap-2 text-sm">
                      {dayWet > 0 && <span className="text-blue-400">💧 {dayWet} wet</span>}
                      {dayDirty > 0 && <span className="text-yellow-600">💩 {dayDirty} dirty</span>}
                      {dayMixed > 0 && <span className="text-orange-600">💧💩 {dayMixed} both</span>}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
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
              <span className="text-gray-600 dark:text-gray-300">Date of last measurement</span>
              <span className="font-semibold">
                {format(parseISO(latestMeasurement.timestamp), 'MMM d, yyyy')}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-300">Age at last measurement</span>
              <span className="font-semibold">{ageMonths} months</span>
            </div>
            <div className="flex items-center justify-between pt-4 border-t">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Weight</p>
                <p className="text-4xl font-bold text-green-600">{latestMeasurement.weight}</p>
                <p className="text-sm text-gray-500">lb</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600 dark:text-gray-300">Percentile</p>
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
                <p className="text-sm text-gray-600 dark:text-gray-300">length</p>
                <p className="text-4xl font-bold text-green-600">{latestMeasurement.height}</p>
                <p className="text-sm text-gray-500">inches</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600 dark:text-gray-300">Percentile</p>
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
                <p className="text-sm text-gray-600 dark:text-gray-300">Head circumference</p>
                <p className="text-4xl font-bold text-purple-600">{latestMeasurement.head_circumference}</p>
                <p className="text-sm text-gray-500">inches</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600 dark:text-gray-300">Percentile</p>
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
