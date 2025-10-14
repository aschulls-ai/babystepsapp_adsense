import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Calendar } from './ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { androidFetch } from '../App';
import { 
  Milk, 
  Droplet, 
  Moon, 
  Activity, 
  Scale, 
  Trophy, 
  Clock,
  Calendar as CalendarIcon,
  Plus,
  Save,
  Bell,
  AlarmClock,
  X,
  Check,
  BabyIcon as Baby2,
  Zap,
  Play,
  Square
} from 'lucide-react';
import { toast } from 'sonner';
import { format, formatDistanceToNow } from 'date-fns';
import PageAd from './ads/PageAd';

const TrackingPage = ({ currentBaby }) => {
  // PHASE 2: Cloud-first - Always use backend API
  const API = process.env.REACT_APP_BACKEND_URL;
  
  const [activeTab, setActiveTab] = useState('feeding');
  const [recentActivities, setRecentActivities] = useState({});
  const [reminders, setReminders] = useState([]);
  const [showReminderForm, setShowReminderForm] = useState(false);
  const [notificationPermission, setNotificationPermission] = useState('default');
  const [quickActionModal, setQuickActionModal] = useState({ show: false, type: null, data: {} });
  const [activeTimers, setActiveTimers] = useState({
    sleep: { active: false, startTime: null, elapsed: 0 },
    pumping: { active: false, startTime: null, elapsed: 0 }
  });
  const [allActivities, setAllActivities] = useState([]);
  const [activityFilter, setActivityFilter] = useState('all');
  const [activitySortBy, setActivitySortBy] = useState('timestamp');
  const [activitySortOrder, setActivitySortOrder] = useState('desc');

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, []);

  useEffect(() => {
    if (currentBaby) {
      fetchRecentActivities();
      fetchReminders();
      fetchAllActivities();
      fetchRecentFeeding(); // Fetch feeding activities for "Recent Feeding" widget
    }
  }, [currentBaby, activeTab]);

  useEffect(() => {
    // Request notification permission
    if ('Notification' in window) {
      setNotificationPermission(Notification.permission);
      if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
          setNotificationPermission(permission);
        });
      }
    }

    // Check reminders every minute
    const reminderInterval = setInterval(checkReminders, 60000);
    return () => clearInterval(reminderInterval);
  }, [reminders]);

  const fetchRecentActivities = async () => {
    if (!currentBaby) return;
    
    try {
      // PHASE 2: Fetch from backend API
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities?baby_id=${currentBaby.id}&type=${activeTab}&limit=5`, {
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
      setRecentActivities(prev => ({
        ...prev,
        [activeTab]: data
      }));
    } catch (error) {
      console.error('Failed to fetch recent activities:', error);
    }
  };

  const fetchAllActivities = async () => {
    if (!currentBaby) return;

    try {
      // PHASE 2: Fetch from backend API
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities?baby_id=${currentBaby.id}`, {
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
      
      // Add display type for each activity
      const activitiesWithDisplayType = data.map(activity => ({
        ...activity,
        activity_type: activity.type,
        display_type: activity.type.charAt(0).toUpperCase() + activity.type.slice(1)
      }));
      
      setAllActivities(activitiesWithDisplayType);
    } catch (error) {
      console.error('Failed to fetch all activities:', error);
    }
  };

  // Dedicated function to fetch feeding activities for "Recent Feeding" widget
  const fetchRecentFeeding = async () => {
    if (!currentBaby) {
      console.log('❌ fetchRecentFeeding: No current baby');
      return;
    }

    console.log('🔄 Fetching recent feeding for baby:', currentBaby.id);
    
    try {
      const token = localStorage.getItem('token');
      const url = `${API}/api/activities?baby_id=${currentBaby.id}&type=feeding&limit=5`;
      console.log('📡 Fetching from:', url);
      
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
      console.log('✅ Recent feeding data received:', data.length, 'activities');
      console.log('Sample:', data[0]);
      
      setRecentActivities(prev => {
        const updated = {
          ...prev,
          feeding: data
        };
        console.log('📊 Updated recentActivities.feeding:', updated.feeding.length);
        return updated;
      });
    } catch (error) {
      console.error('❌ Failed to fetch recent feeding:', error);
    }
  };

  const fetchReminders = async () => {
    if (!currentBaby) return;
    
    try {
      // Use standalone offline storage for reminders
      const storedReminders = JSON.parse(localStorage.getItem('babysteps_reminders') || '[]');
      setReminders(storedReminders);
    } catch (error) {
      console.error('Failed to fetch reminders:', error);
      setReminders([]);
    }
  };

  const checkReminders = () => {
    if (!reminders.length || notificationPermission !== 'granted') return;

    const now = new Date();
    
    reminders.forEach(reminder => {
      if (!reminder.is_active) return;

      const reminderTime = new Date(reminder.next_due);
      
      if (reminderTime <= now) {
        showNotification(reminder);
        markReminderAsNotified(reminder.id);
      }
    });
  };

  const showNotification = (reminder) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(`Baby Steps - ${reminder.title}`, {
        body: `Time for ${currentBaby.name}'s ${reminder.reminder_type}`,
        icon: '/favicon.ico',
        tag: `reminder-${reminder.id}`
      });
    }
  };

  const markReminderAsNotified = async (reminderId) => {
    try {
      // Update reminder in local storage
      const storedReminders = JSON.parse(localStorage.getItem('babysteps_reminders') || '[]');
      const updatedReminders = storedReminders.map(reminder => 
        reminder.id === reminderId 
          ? { ...reminder, lastNotified: new Date().toISOString() }
          : reminder
      );
      localStorage.setItem('babysteps_reminders', JSON.stringify(updatedReminders));
      fetchReminders(); // Refresh reminders
    } catch (error) {
      console.error('Failed to mark reminder as notified:', error);
    }
  };

  const createReminder = async (reminderData) => {
    try {
      const backendData = {
        baby_id: currentBaby.id,
        title: reminderData.title,
        reminder_type: reminderData.type,
        next_due: reminderData.next_notification,
        interval_hours: reminderData.frequency === 'daily' ? 24 : 
                       reminderData.frequency === 'weekly' ? 168 :
                       reminderData.frequency === 'monthly' ? 720 : null
      };
      
      // Use standalone offline API for reminders
      const offlineReminder = {
        id: Date.now().toString(),
        title: reminderData.title,
        type: reminderData.type,
        frequency: reminderData.frequency,
        time: reminderData.time,
        enabled: reminderData.enabled,
        created_at: new Date().toISOString()
      };
      
      // Store reminder locally
      const existingReminders = JSON.parse(localStorage.getItem('babysteps_reminders') || '[]');
      existingReminders.push(offlineReminder);
      localStorage.setItem('babysteps_reminders', JSON.stringify(existingReminders));
      
      toast.success('💾 Reminder saved to device!');
      fetchReminders();
      setShowReminderForm(false);
    } catch (error) {
      toast.error('Failed to create reminder');
    }
  };

  const toggleReminder = async (reminderId, enabled) => {
    try {
      // Update reminder in local storage
      const storedReminders = JSON.parse(localStorage.getItem('babysteps_reminders') || '[]');
      const updatedReminders = storedReminders.map(reminder => 
        reminder.id === reminderId 
          ? { ...reminder, enabled: enabled }
          : reminder
      );
      localStorage.setItem('babysteps_reminders', JSON.stringify(updatedReminders));
      toast.success(enabled ? 'Reminder enabled' : 'Reminder disabled');
      fetchReminders();
    } catch (error) {
      console.error('Failed to toggle reminder:', error);
    }
  };

  const deleteReminder = async (reminderId) => {
    try {
      // Remove reminder from local storage
      const storedReminders = JSON.parse(localStorage.getItem('babysteps_reminders') || '[]');
      const updatedReminders = storedReminders.filter(reminder => reminder.id !== reminderId);
      localStorage.setItem('babysteps_reminders', JSON.stringify(updatedReminders));
      toast.success('Reminder deleted');
      fetchReminders();
    } catch (error) {
      console.error('Failed to delete reminder:', error);
    }
  };

  const handleQuickAction = (type) => {
    // Handle timer-based actions differently
    if (type === 'sleep') {
      if (activeTimers.sleep.active) {
        // Stop sleep timer and show completion modal
        const elapsed = Math.floor((Date.now() - activeTimers.sleep.startTime) / 1000 / 60); // minutes
        setQuickActionModal({
          show: true,
          type: 'sleep',
          data: { duration: elapsed, isCompleting: true }
        });
      } else {
        // Start sleep timer
        setActiveTimers(prev => ({
          ...prev,
          sleep: { active: true, startTime: Date.now(), elapsed: 0 }
        }));
        toast.success('Sleep timer started!');
      }
      return;
    }

    if (type === 'pumping') {
      if (activeTimers.pumping.active) {
        // Stop pumping timer and show completion modal
        const elapsed = Math.floor((Date.now() - activeTimers.pumping.startTime) / 1000 / 60); // minutes
        setQuickActionModal({
          show: true,
          type: 'pumping',
          data: { duration: elapsed, leftBreast: 0, rightBreast: 0, isCompleting: true }
        });
      } else {
        // Start pumping timer
        setActiveTimers(prev => ({
          ...prev,
          pumping: { active: true, startTime: Date.now(), elapsed: 0 }
        }));
        toast.success('Pumping timer started!');
      }
      return;
    }

    // Handle non-timer actions
    const defaultData = {
      feeding: { type: 'bottle', amount: 4 },
      diaper: { type: 'wet' },
      measurements: { weight: '', height: '' },
      milestones: { title: '', category: 'physical' }
    };

    setQuickActionModal({
      show: true,
      type: type,
      data: defaultData[type] || {}
    });
  };

  const handleQuickSubmit = async (data) => {
    const { type } = quickActionModal;
    
    try {
      // Ensure we have a baby selected
      if (!currentBaby || !currentBaby.id) {
        toast.error('Please select a baby profile first');
        return;
      }

      const payload = {
        type: type,
        baby_id: currentBaby.id,
        timestamp: new Date().toISOString(),
        ...data
      };

      let successMessage = '';

      switch (type) {
        case 'feeding':
          // Rename 'type' field to 'feeding_type' to avoid conflict with activity type
          if (data.type) {
            payload.feeding_type = data.type;
            delete payload.type;
          }
          // Re-add the activity type
          payload.type = 'feeding';
          successMessage = 'Feeding logged successfully!';
          break;
        case 'diaper':
          // Rename 'type' field to 'diaper_type' to avoid conflict with activity type
          if (data.type) {
            payload.diaper_type = data.type;
            delete payload.type;
          }
          // Re-add the activity type
          payload.type = 'diaper';
          successMessage = 'Diaper change logged!';
          break;
        case 'sleep':
          payload.start_time = new Date().toISOString();
          successMessage = 'Sleep session logged!';
          break;
        case 'pumping':
          // Store individual breast amounts
          if (data.leftBreast !== undefined) {
            payload.left_breast = data.leftBreast || 0;
          }
          if (data.rightBreast !== undefined) {
            payload.right_breast = data.rightBreast || 0;
          }
          // Calculate total amount for backward compatibility
          payload.amount = (data.leftBreast || 0) + (data.rightBreast || 0);
          // Clean up frontend field names
          delete payload.leftBreast;
          delete payload.rightBreast;
          // Ensure duration is set (from timer or default)
          if (!payload.duration) {
            payload.duration = data.duration || 0;
          }
          // Remove frontend-specific fields
          delete payload.isCompleting;
          successMessage = 'Pumping session logged!';
          break;
        case 'measurements':
          successMessage = 'Measurements recorded!';
          break;
        case 'milestones':
          payload.achieved_date = new Date().toISOString();
          successMessage = 'Milestone recorded!';
          break;
      }

      // PHASE 2: Log to backend API
      console.log('📝 Logging activity to backend:', payload);
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      const result = await response.json();
      console.log('✅ Activity logged successfully to cloud:', result);
      
      toast.success(successMessage);
      
      fetchRecentActivities();
      fetchAllActivities(); // Refresh comprehensive activity list
      fetchRecentFeeding(); // Refresh Recent Feeding widget
      
      // Reset active timers if completing a timer-based action
      if (data.isCompleting) {
        setActiveTimers(prev => ({
          ...prev,
          [type]: { active: false, startTime: null, elapsed: 0 }
        }));
      }
      
      setQuickActionModal({ show: false, type: null, data: {} });
      
    } catch (error) {
      console.error('❌ Activity logging failed:', error);
      toast.error(`Failed to log ${type}: ${error.message || 'Unknown error'}`);
    }
  };

  if (!currentBaby) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="glass-strong border-0 max-w-md mx-auto text-center">
          <CardContent className="p-8">
            <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
              <Activity className="w-8 h-8 text-gray-400" />
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">No Baby Selected</h2>
            <p className="text-gray-600 dark:text-gray-300">Please select or add a baby to start tracking activities.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const tabs = [
    { id: 'feeding', label: 'Feeding', icon: Milk },
    { id: 'diaper', label: 'Diaper', icon: Droplet },
    { id: 'sleep', label: 'Sleep', icon: Moon },
    { id: 'pumping', label: 'Pumping', icon: Activity },
    { id: 'measurements', label: 'Growth', icon: Scale },
    { id: 'milestones', label: 'Milestones', icon: Trophy }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-6 fade-in">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold font-display text-gray-900 dark:text-white" data-testid="tracking-title">
            Track Activities
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Log {currentBaby.name}'s daily activities and milestones
          </p>
        </div>
      </div>

      {/* Quick Action Buttons */}
      <Card className="glass border-0 bg-gradient-to-r from-blue-50 to-green-50">
        <CardContent className="p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Play className="w-5 h-5 text-blue-600" />
            Quick Actions
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <QuickActionButton 
              icon={Baby2} 
              label="Quick Feed" 
              color="blue"
              testId="quick-action-feed"
              onClick={() => handleQuickAction('feeding')}
            />
            <QuickActionButton 
              icon={Droplet} 
              label="Diaper Change" 
              color="green"
              testId="quick-action-diaper"
              onClick={() => handleQuickAction('diaper')}
            />
            <TimerQuickActionButton 
              icon={activeTimers.sleep.active ? Square : Moon}
              label={activeTimers.sleep.active ? "Stop Sleep" : "Start Sleep"}
              color="purple"
              isActive={activeTimers.sleep.active}
              timer={activeTimers.sleep}
              testId="quick-action-sleep"
              onClick={() => handleQuickAction('sleep')}
            />
            <TimerQuickActionButton 
              icon={activeTimers.pumping.active ? Square : Zap}
              label={activeTimers.pumping.active ? "Stop Pump" : "Start Pump"}
              color="pink"
              isActive={activeTimers.pumping.active}
              timer={activeTimers.pumping}
              testId="quick-action-pump"
              onClick={() => handleQuickAction('pumping')}
            />
            <QuickActionButton 
              icon={Scale} 
              label="Measure" 
              color="orange"
              testId="quick-action-measure"
              onClick={() => handleQuickAction('measurements')}
            />
            <QuickActionButton 
              icon={Trophy} 
              label="Milestone" 
              color="yellow"
              testId="quick-action-milestone"
              onClick={() => handleQuickAction('milestones')}
            />
          </div>
        </CardContent>
      </Card>

      <div className="grid lg:grid-cols-4 gap-6">
        {/* Tracking Forms - HIDDEN */}
        <div className="lg:col-span-3" style={{display: 'none'}}>
          <Card className="glass-strong border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
                <Activity className="w-5 h-5 text-blue-600" />
                Log Activity Details
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6 pt-0">
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList className="grid grid-cols-3 lg:grid-cols-6 mb-6 bg-gray-100 p-1 rounded-xl">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <TabsTrigger
                        key={tab.id}
                        value={tab.id}
                        className="rounded-lg data-[state=active]:bg-white data-[state=active]:dark:bg-gray-700 data-[state=active]:shadow-md transition-all duration-200 flex items-center gap-1 px-2 py-2"
                        data-testid={`${tab.id}-tab`}
                      >
                        <Icon className="w-4 h-4" />
                        <span className="hidden sm:inline">{tab.label}</span>
                      </TabsTrigger>
                    );
                  })}
                </TabsList>

                <TabsContent value="feeding">
                  <FeedingForm babyId={currentBaby.id} onSuccess={fetchRecentActivities} />
                </TabsContent>
                <TabsContent value="diaper">
                  <DiaperForm babyId={currentBaby.id} onSuccess={fetchRecentActivities} />
                </TabsContent>
                <TabsContent value="sleep">
                  <SleepForm babyId={currentBaby.id} onSuccess={fetchRecentActivities} />
                </TabsContent>
                <TabsContent value="pumping">
                  <PumpingForm babyId={currentBaby.id} onSuccess={fetchRecentActivities} />
                </TabsContent>
                <TabsContent value="measurements">
                  <MeasurementForm babyId={currentBaby.id} onSuccess={fetchRecentActivities} />
                </TabsContent>
                <TabsContent value="milestones">
                  <MilestoneForm babyId={currentBaby.id} onSuccess={fetchRecentActivities} />
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Reminders Section - HIDDEN */}
          <Card className="glass border-0" style={{display: 'none'}}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
                  <Bell className="w-5 h-5 text-blue-500" />
                  Reminders
                </CardTitle>
                <Button
                  onClick={() => setShowReminderForm(true)}
                  size="sm"
                  className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                  <Plus className="w-4 h-4 mr-1" />
                  Add
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <ReminderList 
                reminders={reminders}
                onToggle={toggleReminder}
                onDelete={deleteReminder}
              />
              {showReminderForm && (
                <ReminderForm
                  onSubmit={createReminder}
                  onCancel={() => setShowReminderForm(false)}
                />
              )}
            </CardContent>
          </Card>

          {/* Recent Activities - HIDDEN */}
          <Card className="glass border-0" style={{display: 'none'}}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
                <Clock className="w-5 h-5 text-rose-500" />
                Recent Feeding
              </CardTitle>
            </CardHeader>
            <CardContent>
              <RecentActivityList 
                activities={recentActivities['feeding'] || []}
                type="feeding"
              />
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Activity History Section - Same Width as Log Activity Details */}
      <div className="grid lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <Card className="glass-strong border-0">
            <CardHeader>
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
                  <Activity className="w-5 h-5 text-indigo-500" />
                  Activity History
                  <span className="text-sm font-normal text-gray-500">
                    ({allActivities.length} activities)
                  </span>
                </CardTitle>
                <div className="flex flex-col sm:flex-row gap-2">
                  <Select value={activityFilter} onValueChange={setActivityFilter}>
                    <SelectTrigger className="w-full sm:w-40 bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
                      <SelectValue placeholder="Filter activities" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Activities</SelectItem>
                      <SelectItem value="feeding">Feeding</SelectItem>
                      <SelectItem value="diaper">Diaper</SelectItem>
                      <SelectItem value="sleep">Sleep</SelectItem>
                      <SelectItem value="pumping">Pumping</SelectItem>
                      <SelectItem value="measurement">Growth</SelectItem>
                      <SelectItem value="milestone">Milestones</SelectItem>
                    </SelectContent>
                  </Select>
                  <Select value={`${activitySortBy}-${activitySortOrder}`} onValueChange={(value) => {
                    const [sortBy, sortOrder] = value.split('-');
                    setActivitySortBy(sortBy);
                    setActivitySortOrder(sortOrder);
                  }}>
                    <SelectTrigger className="w-full sm:w-40 bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
                      <SelectValue placeholder="Sort by">
                        {activitySortBy === 'timestamp' && activitySortOrder === 'desc' && 'Newest First'}
                        {activitySortBy === 'timestamp' && activitySortOrder === 'asc' && 'Oldest First'}
                        {activitySortBy === 'type' && activitySortOrder === 'asc' && 'By Type A-Z'}
                        {activitySortBy === 'type' && activitySortOrder === 'desc' && 'By Type Z-A'}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="timestamp-desc">Newest First</SelectItem>
                      <SelectItem value="timestamp-asc">Oldest First</SelectItem>
                      <SelectItem value="type-asc">By Type A-Z</SelectItem>
                      <SelectItem value="type-desc">By Type Z-A</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ActivityHistoryList 
                activities={allActivities}
                filter={activityFilter}
                sortBy={activitySortBy}
                sortOrder={activitySortOrder}
                currentBaby={currentBaby}
              />
            </CardContent>
          </Card>
        </div>
        <div className="lg:col-span-1">
          {/* Empty space to maintain alignment */}
        </div>
      </div>

      {/* Quick Action Modal */}
      <QuickActionModal
        show={quickActionModal.show}
        type={quickActionModal.type}
        data={quickActionModal.data}
        onSubmit={handleQuickSubmit}
        onCancel={() => setQuickActionModal({ show: false, type: null, data: {} })}
      />

      {/* Page Ad */}
      <PageAd position="bottom" />
    </div>
  );
};

// Form Components
const FeedingForm = ({ babyId, onSuccess }) => {
  const [formData, setFormData] = useState({
    type: 'bottle',
    amount: '',
    duration: '',
    notes: '',
    timestamp: new Date()
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = {
        baby_id: babyId,
        type: formData.type,
        amount: formData.amount ? parseFloat(formData.amount) : null,
        duration: formData.duration ? parseInt(formData.duration) : null,
        notes: formData.notes || null,
        timestamp: formData.timestamp.toISOString()
      };

      // PHASE 2: Log to backend API
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          baby_id: babyId,
          type: 'feeding',
          feeding_type: formData.type,
          amount: formData.amount || null,
          duration: formData.duration || null,
          notes: formData.notes || null,
          timestamp: formData.timestamp.toISOString()
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      toast.success('Feeding logged successfully!');
      setFormData({
        type: 'bottle',
        amount: '',
        duration: '',
        notes: '',
        timestamp: new Date()
      });
      onSuccess();
    } catch (error) {
      toast.error('Failed to log feeding');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Feeding Type</Label>
          <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
            <SelectTrigger data-testid="feeding-type-selector">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="bottle">Bottle</SelectItem>
              <SelectItem value="breast">Breastfeeding</SelectItem>
              <SelectItem value="solid">Solid Food</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {formData.type === 'bottle' && (
          <div className="space-y-2">
            <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Amount (oz)</Label>
            <Input
              type="number"
              step="0.5"
              placeholder="e.g., 4"
              value={formData.amount}
              onChange={(e) => setFormData({...formData, amount: e.target.value})}
              data-testid="feeding-amount-input"
            />
          </div>
        )}

        {formData.type === 'breast' && (
          <div className="space-y-2">
            <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Duration (minutes)</Label>
            <Input
              type="number"
              placeholder="e.g., 15"
              value={formData.duration}
              onChange={(e) => setFormData({...formData, duration: e.target.value})}
              data-testid="feeding-duration-input"
            />
          </div>
        )}
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Notes (optional)</Label>
        <Textarea
          placeholder="Any additional notes..."
          value={formData.notes}
          onChange={(e) => setFormData({...formData, notes: e.target.value})}
          data-testid="feeding-notes-input"
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="save-feeding-btn"
      >
        {loading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Saving...
          </div>
        ) : (
          <>
            <Save className="w-5 h-5 mr-2" />
            Log Feeding
          </>
        )}
      </Button>
    </form>
  );
};

const DiaperForm = ({ babyId, onSuccess }) => {
  const [formData, setFormData] = useState({
    type: 'wet',
    notes: '',
    timestamp: new Date()
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = {
        baby_id: babyId,
        type: formData.type,
        notes: formData.notes || null,
        timestamp: formData.timestamp.toISOString()
      };

      // PHASE 2: Log to backend API
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          baby_id: babyId,
          type: 'diaper',
          diaper_type: formData.type,
          notes: formData.notes || null,
          timestamp: formData.timestamp.toISOString()
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      toast.success('Diaper change logged successfully!');
      setFormData({
        type: 'wet',
        notes: '',
        timestamp: new Date()
      });
      onSuccess();
    } catch (error) {
      toast.error('Failed to log diaper change');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Diaper Type</Label>
        <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
          <SelectTrigger data-testid="diaper-type-selector">
            <SelectValue />
          </SelectTrigger>
          <SelectContent position="popper" sideOffset={5}>
            <SelectItem value="wet">Wet</SelectItem>
            <SelectItem value="dirty">Dirty</SelectItem>
            <SelectItem value="mixed">Mixed (Wet & Dirty)</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Notes (optional)</Label>
        <Textarea
          placeholder="Any observations or notes..."
          value={formData.notes}
          onChange={(e) => setFormData({...formData, notes: e.target.value})}
          data-testid="diaper-notes-input"
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="save-diaper-btn"
      >
        {loading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Saving...
          </div>
        ) : (
          <>
            <Save className="w-5 h-5 mr-2" />
            Log Diaper Change
          </>
        )}
      </Button>
    </form>
  );
};

const SleepForm = ({ babyId, onSuccess }) => {
  const [formData, setFormData] = useState({
    start_time: new Date(),
    end_time: '',
    quality: '',
    notes: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Use standalone offline API - Enhanced safety checks for sleep tracking
      const startTime = formData.start_time instanceof Date ? formData.start_time : new Date(formData.start_time);
      const endTime = (formData.end_time && formData.end_time !== '') ? new Date(formData.end_time) : null;
      
      const sleepActivityData = {
        baby_id: babyId,
        type: 'sleep',
        timestamp: startTime.toISOString(),
        duration: endTime ? Math.round((endTime - startTime) / (1000 * 60)) : null, // minutes
        quality: formData.quality || null,
        notes: formData.notes || null,
        sleep_start: startTime.toISOString(),
        sleep_end: endTime ? endTime.toISOString() : null
      };
      
      console.log('🛌 Logging sleep activity:', sleepActivityData);
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(sleepActivityData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      toast.success('Sleep session logged successfully!');
      setFormData({
        start_time: new Date(),
        end_time: '',
        quality: '',
        notes: ''
      });
      onSuccess();
    } catch (error) {
      console.error('❌ Sleep form error:', error);
      toast.error(`Failed to log sleep session: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Start Time</Label>
          <Input
            type="datetime-local"
            value={format(formData.start_time, "yyyy-MM-dd'T'HH:mm")}
            onChange={(e) => setFormData({...formData, start_time: new Date(e.target.value)})}
            data-testid="sleep-start-time-input"
          />
        </div>

        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">End Time (optional)</Label>
          <Input
            type="datetime-local"
            value={formData.end_time}
            onChange={(e) => setFormData({...formData, end_time: e.target.value})}
            data-testid="sleep-end-time-input"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Sleep Quality (optional)</Label>
        <Select value={formData.quality} onValueChange={(value) => setFormData({...formData, quality: value})}>
          <SelectTrigger data-testid="sleep-quality-selector">
            <SelectValue placeholder="Select quality" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="good">Good</SelectItem>
            <SelectItem value="fair">Fair</SelectItem>
            <SelectItem value="poor">Poor</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Notes (optional)</Label>
        <Textarea
          placeholder="Sleep environment, interruptions, etc..."
          value={formData.notes}
          onChange={(e) => setFormData({...formData, notes: e.target.value})}
          data-testid="sleep-notes-input"
        />
      </div>

      <Button
        type="button"
        disabled={true}
        className="w-full bg-gray-400 text-white font-semibold py-3 rounded-xl shadow-lg cursor-not-allowed"
        data-testid="save-sleep-btn"
        onClick={() => {
          toast.info("Sleep logging temporarily disabled - was causing app issues");
        }}
      >
        <Save className="w-5 h-5 mr-2" />
        Sleep Logging Disabled
      </Button>
    </form>
  );
};

const PumpingForm = ({ babyId, onSuccess }) => {
  const [formData, setFormData] = useState({
    amount: '',
    duration: '',
    notes: '',
    timestamp: new Date()
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = {
        baby_id: babyId,
        amount: parseFloat(formData.amount),
        duration: parseInt(formData.duration),
        notes: formData.notes || null,
        timestamp: formData.timestamp.toISOString()
      };

      // PHASE 2: Log to backend API
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          baby_id: babyId,
          type: 'pumping',
          amount: formData.amount || null,
          duration: formData.duration || null,
          notes: formData.notes || null,
          timestamp: formData.timestamp.toISOString()
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      toast.success('Pumping session logged successfully!');
      setFormData({
        amount: '',
        duration: '',
        notes: '',
        timestamp: new Date()
      });
      onSuccess();
    } catch (error) {
      toast.error('Failed to log pumping session');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Amount (oz) *</Label>
          <Input
            type="number"
            step="0.5"
            placeholder="e.g., 3.5"
            value={formData.amount}
            onChange={(e) => setFormData({...formData, amount: e.target.value})}
            required
            data-testid="pumping-amount-input"
          />
        </div>

        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Duration (minutes) *</Label>
          <Input
            type="number"
            placeholder="e.g., 20"
            value={formData.duration}
            onChange={(e) => setFormData({...formData, duration: e.target.value})}
            required
            data-testid="pumping-duration-input"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Notes (optional)</Label>
        <Textarea
          placeholder="Comfort level, pump settings, etc..."
          value={formData.notes}
          onChange={(e) => setFormData({...formData, notes: e.target.value})}
          data-testid="pumping-notes-input"
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="save-pumping-btn"
      >
        {loading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Saving...
          </div>
        ) : (
          <>
            <Save className="w-5 h-5 mr-2" />
            Log Pumping Session
          </>
        )}
      </Button>
    </form>
  );
};

const MeasurementForm = ({ babyId, onSuccess }) => {
  const [formData, setFormData] = useState({
    weight: '',
    height: '',
    head_circumference: '',
    temperature: '',
    notes: '',
    timestamp: new Date()
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = {
        baby_id: babyId,
        weight: formData.weight ? parseFloat(formData.weight) : null,
        height: formData.height ? parseFloat(formData.height) : null,
        head_circumference: formData.head_circumference ? parseFloat(formData.head_circumference) : null,
        temperature: formData.temperature ? parseFloat(formData.temperature) : null,
        notes: formData.notes || null,
        timestamp: formData.timestamp.toISOString()
      };

      // PHASE 2: Log to backend API
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          baby_id: babyId,
          type: 'measurement',
          weight: formData.weight || null,
          height: formData.height || null,
          head_circumference: formData.head_circumference || null,
          temperature: formData.temperature || null,
          notes: formData.notes || null,
          timestamp: formData.timestamp.toISOString()
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      toast.success('Measurements logged successfully!');
      setFormData({
        weight: '',
        height: '',
        head_circumference: '',
        temperature: '',
        notes: '',
        timestamp: new Date()
      });
      onSuccess();
    } catch (error) {
      toast.error('Failed to log measurements');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Weight (lbs)</Label>
          <Input
            type="number"
            step="0.1"
            placeholder="e.g., 8.5"
            value={formData.weight}
            onChange={(e) => setFormData({...formData, weight: e.target.value})}
            data-testid="measurement-weight-input"
          />
        </div>

        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Height (inches)</Label>
          <Input
            type="number"
            step="0.1"
            placeholder="e.g., 22.5"
            value={formData.height}
            onChange={(e) => setFormData({...formData, height: e.target.value})}
            data-testid="measurement-height-input"
          />
        </div>

        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Head Circumference (inches)</Label>
          <Input
            type="number"
            step="0.1"
            placeholder="e.g., 15.2"
            value={formData.head_circumference}
            onChange={(e) => setFormData({...formData, head_circumference: e.target.value})}
            data-testid="measurement-head-input"
          />
        </div>

        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Temperature (°F)</Label>
          <Input
            type="number"
            step="0.1"
            placeholder="e.g., 98.6"
            value={formData.temperature}
            onChange={(e) => setFormData({...formData, temperature: e.target.value})}
            data-testid="measurement-temperature-input"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Notes (optional)</Label>
        <Textarea
          placeholder="Doctor visit, growth concerns, etc..."
          value={formData.notes}
          onChange={(e) => setFormData({...formData, notes: e.target.value})}
          data-testid="measurement-notes-input"
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-indigo-500 to-blue-500 hover:from-indigo-600 hover:to-blue-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="save-measurement-btn"
      >
        {loading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Saving...
          </div>
        ) : (
          <>
            <Save className="w-5 h-5 mr-2" />
            Save Measurements
          </>
        )}
      </Button>
    </form>
  );
};

const MilestoneForm = ({ babyId, onSuccess }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'physical',
    achieved_date: new Date(),
    notes: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = {
        baby_id: babyId,
        title: formData.title,
        description: formData.description || null,
        category: formData.category,
        achieved_date: formData.achieved_date.toISOString(),
        notes: formData.notes || null
      };

      // PHASE 2: Log to backend API
      const milestoneData = {
        baby_id: babyId,
        type: 'milestone',
        title: formData.title,
        description: formData.description || null,
        category: formData.category,
        timestamp: formData.achieved_date.toISOString(),
        notes: formData.notes || null
      };
      
      console.log('🏆 Logging milestone activity to backend:', milestoneData);
      
      const token = localStorage.getItem('token');
      const response = await androidFetch(`${API}/api/activities`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(milestoneData)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      
      toast.success('Milestone logged successfully!');
      setFormData({
        title: '',
        description: '',
        category: 'physical',
        achieved_date: new Date(),
        notes: ''
      });
      onSuccess();
    } catch (error) {
      console.error('❌ Milestone form error:', error);
      toast.error(`Failed to log milestone: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Milestone Title *</Label>
        <Input
          type="text"
          placeholder="e.g., First smile, Rolling over"
          value={formData.title}
          onChange={(e) => setFormData({...formData, title: e.target.value})}
          required
          data-testid="milestone-title-input"
        />
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Category</Label>
        <Select value={formData.category} onValueChange={(value) => setFormData({...formData, category: value})}>
          <SelectTrigger data-testid="milestone-category-selector">
            <SelectValue />
          </SelectTrigger>
          <SelectContent position="popper" sideOffset={5}>
            <SelectItem value="physical">Physical Development</SelectItem>
            <SelectItem value="cognitive">Cognitive Development</SelectItem>
            <SelectItem value="social">Social Development</SelectItem>
            <SelectItem value="feeding">Feeding</SelectItem>
            <SelectItem value="sleep">Sleep</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Achievement Date</Label>
        <Input
          type="date"
          value={format(formData.achieved_date, 'yyyy-MM-dd')}
          onChange={(e) => setFormData({...formData, achieved_date: new Date(e.target.value)})}
          data-testid="milestone-date-input"
        />
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Description (optional)</Label>
        <Textarea
          placeholder="Describe the milestone in detail..."
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          data-testid="milestone-description-input"
        />
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700 dark:text-gray-200">Notes (optional)</Label>
        <Textarea
          placeholder="Additional notes or memories..."
          value={formData.notes}
          onChange={(e) => setFormData({...formData, notes: e.target.value})}
          data-testid="milestone-notes-input"
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="save-milestone-btn"
      >
        {loading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Saving...
          </div>
        ) : (
          <>
            <Save className="w-5 h-5 mr-2" />
            Record Milestone
          </>
        )}
      </Button>
    </form>
  );
};

// Recent Activities List
const RecentActivityList = ({ activities, type }) => {
  if (!activities.length) {
    return (
      <p className="text-gray-500 text-center py-8">
        No recent {type} activities
      </p>
    );
  }

  const formatActivity = (activity, type) => {
    switch (type) {
      case 'feeding':
        // Map feeding_type to display names
        const feedingTypeMap = {
          'bottle': 'Bottle',
          'breast': 'Breastfeeding',
          'breastfeeding': 'Breastfeeding',
          'solid': 'Solid Food',
          'formula': 'Formula'
        };
        const feedingLabel = feedingTypeMap[activity.feeding_type?.toLowerCase()] || 'Feeding';
        
        return {
          title: feedingLabel,
          subtitle: activity.amount ? `${activity.amount} oz` : `${activity.duration || 0} min`,
          time: formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })
        };
      case 'diaper':
        return {
          title: `${activity.type.charAt(0).toUpperCase() + activity.type.slice(1)} diaper`,
          subtitle: 'Changed',
          time: formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })
        };
      case 'sleep':
        return {
          title: 'Sleep session',
          subtitle: activity.duration ? `${Math.round(activity.duration / 60)}h ${activity.duration % 60}m` : 'In progress',
          time: formatDistanceToNow(new Date(activity.start_time), { addSuffix: true })
        };
      case 'pumping':
        return {
          title: 'Pumping session',
          subtitle: `${activity.amount} oz in ${activity.duration} min`,
          time: formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })
        };
      case 'measurements':
        return {
          title: 'Growth measurement',
          subtitle: [activity.weight && `${activity.weight} lbs`, activity.height && `${activity.height} in`].filter(Boolean).join(', ') || 'Measured',
          time: formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })
        };
      case 'milestones':
        return {
          title: activity.title,
          subtitle: activity.category.charAt(0).toUpperCase() + activity.category.slice(1),
          time: formatDistanceToNow(new Date(activity.achieved_date), { addSuffix: true })
        };
      default:
        return { title: 'Activity', subtitle: '', time: '' };
    }
  };

  return (
    <div className="space-y-3">
      {activities.map((activity, index) => {
        const formatted = formatActivity(activity, type);
        return (
          <div key={activity.id || index} className="p-3 bg-gray-50 rounded-lg border border-gray-100">
            <h4 className="font-medium text-gray-900 text-sm">{formatted.title}</h4>
            <p className="text-sm text-gray-600 dark:text-gray-300">{formatted.subtitle}</p>
            <p className="text-xs text-gray-400 mt-1">{formatted.time}</p>
          </div>
        );
      })}
    </div>
  );
};

// Quick Action Button Component
const QuickActionButton = ({ icon: Icon, label, color, onClick, testId }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-700 hover:bg-blue-200',
    green: 'bg-green-100 text-green-700 hover:bg-green-200',
    purple: 'bg-purple-100 text-purple-700 hover:bg-purple-200',
    pink: 'bg-pink-100 text-pink-700 hover:bg-pink-200',
    orange: 'bg-orange-100 text-orange-700 hover:bg-orange-200',
    yellow: 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
  };

  return (
    <button
      onClick={onClick}
      data-testid={testId || `quick-action-${label.toLowerCase().replace(' ', '-')}`}
      className={`${colorClasses[color]} p-4 rounded-xl transition-all duration-200 hover:scale-105 hover:shadow-md flex flex-col items-center gap-2 text-center`}
    >
      <Icon className="w-6 h-6" />
      <span className="text-sm font-medium">{label}</span>
    </button>
  );
};

// Timer Quick Action Button Component with live timer display
const TimerQuickActionButton = ({ icon: Icon, label, color, isActive, timer, onClick, testId }) => {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    let interval;
    if (isActive && timer.startTime) {
      interval = setInterval(() => {
        setElapsed(Math.floor((Date.now() - timer.startTime) / 1000));
      }, 1000);
    } else {
      setElapsed(0);
    }
    return () => clearInterval(interval);
  }, [isActive, timer.startTime]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const colorClasses = {
    blue: isActive ? 'bg-blue-200 text-blue-800 border-2 border-blue-400 animate-pulse' : 'bg-blue-100 text-blue-700 hover:bg-blue-200',
    green: isActive ? 'bg-green-200 text-green-800 border-2 border-green-400 animate-pulse' : 'bg-green-100 text-green-700 hover:bg-green-200',
    purple: isActive ? 'bg-purple-200 text-purple-800 border-2 border-purple-400 animate-pulse' : 'bg-purple-100 text-purple-700 hover:bg-purple-200',
    pink: isActive ? 'bg-pink-200 text-pink-800 border-2 border-pink-400 animate-pulse' : 'bg-pink-100 text-pink-700 hover:bg-pink-200',
    orange: isActive ? 'bg-orange-200 text-orange-800 border-2 border-orange-400 animate-pulse' : 'bg-orange-100 text-orange-700 hover:bg-orange-200',
    yellow: isActive ? 'bg-yellow-200 text-yellow-800 border-2 border-yellow-400 animate-pulse' : 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
  };

  return (
    <button
      onClick={onClick}
      data-testid={testId || `timer-action-${label.toLowerCase().replace(' ', '-')}`}
      className={`${colorClasses[color]} p-4 rounded-xl transition-all duration-200 hover:scale-105 hover:shadow-md flex flex-col items-center gap-2 text-center`}
    >
      <Icon className="w-6 h-6" />
      <span className="text-sm font-medium">{label}</span>
      {isActive && (
        <div className="text-xs font-mono bg-white dark:bg-gray-700 bg-opacity-50 px-2 py-1 rounded">
          {formatTime(elapsed)}
        </div>
      )}
    </button>
  );
};

// Reminder Form Component
const ReminderForm = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    type: 'feeding',
    frequency: 'daily',
    time: '09:00',
    enabled: true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const now = new Date();
    const [hours, minutes] = formData.time.split(':');
    const nextNotification = new Date();
    nextNotification.setHours(parseInt(hours), parseInt(minutes), 0, 0);
    
    // If time has passed today, set for tomorrow
    if (nextNotification <= now) {
      nextNotification.setDate(nextNotification.getDate() + 1);
    }

    onSubmit({
      ...formData,
      next_notification: nextNotification.toISOString()
    });
  };

  return (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg border">
      <h4 className="font-medium text-gray-800 mb-3">Create New Reminder</h4>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <Label className="text-sm font-medium">Reminder Title</Label>
          <Input
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            placeholder="e.g., Morning feeding"
            required
            className="mt-1"
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label className="text-sm font-medium">Type</Label>
            <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
              <SelectTrigger className="mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="feeding">Feeding</SelectItem>
                <SelectItem value="pumping">Pumping</SelectItem>
                <SelectItem value="diaper">Diaper Check</SelectItem>
                <SelectItem value="medicine">Medicine</SelectItem>
                <SelectItem value="playtime">Play Time</SelectItem>
                <SelectItem value="bath">Bath Time</SelectItem>
                <SelectItem value="appointment">Appointment</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label className="text-sm font-medium">Time</Label>
            <Input
              type="time"
              value={formData.time}
              onChange={(e) => setFormData({...formData, time: e.target.value})}
              className="mt-1"
              required
            />
          </div>
        </div>

        <div>
          <Label className="text-sm font-medium">Frequency</Label>
          <Select value={formData.frequency} onValueChange={(value) => setFormData({...formData, frequency: value})}>
            <SelectTrigger className="mt-1">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="daily">Daily</SelectItem>
              <SelectItem value="weekly">Weekly</SelectItem>
              <SelectItem value="monthly">Monthly</SelectItem>
              <SelectItem value="once">One-time</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="flex gap-2 pt-2">
          <Button type="submit" size="sm" className="bg-blue-600 hover:bg-blue-700 text-white">
            <Check className="w-4 h-4 mr-1" />
            Create Reminder
          </Button>
          <Button type="button" onClick={onCancel} variant="outline" size="sm">
            <X className="w-4 h-4 mr-1" />
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
};

// Reminder List Component
const ReminderList = ({ reminders, onToggle, onDelete }) => {
  if (reminders.length === 0) {
    return (
      <div className="text-center py-4 text-gray-500">
        <AlarmClock className="w-8 h-8 mx-auto mb-2 text-gray-400" />
        <p className="text-sm">No reminders set</p>
        <p className="text-xs">Add reminders to get notified about important activities</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {reminders.map((reminder) => {
        const nextTime = new Date(reminder.next_due);
        const frequency = reminder.interval_hours === 24 ? 'daily' : 
                         reminder.interval_hours === 168 ? 'weekly' :
                         reminder.interval_hours === 720 ? 'monthly' : 'custom';
        return (
          <div key={reminder.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h4 className="font-medium text-gray-800 text-sm">{reminder.title}</h4>
                <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
                  {reminder.reminder_type}
                </span>
              </div>
              <p className="text-xs text-gray-600 mt-1">
                Next: {format(nextTime, 'MMM d, h:mm a')} ({frequency})
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => onToggle(reminder.id, !reminder.is_active)}
                className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
                  reminder.is_active 
                    ? 'bg-green-100 text-green-600 hover:bg-green-200' 
                    : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                }`}
                title={reminder.is_active ? 'Disable' : 'Enable'}
              >
                <Bell className="w-4 h-4" />
              </button>
              <button
                onClick={() => onDelete(reminder.id)}
                className="w-8 h-8 rounded-full bg-red-100 text-red-600 hover:bg-red-200 flex items-center justify-center transition-colors"
                title="Delete"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

// Quick Action Modal Component
const QuickActionModal = ({ show, type, data, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState(data);

  useEffect(() => {
    setFormData(data);
  }, [data]);

  if (!show) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const getModalTitle = () => {
    switch (type) {
      case 'feeding': return 'Quick Feeding';
      case 'diaper': return 'Quick Diaper Change';
      case 'sleep': return 'Start Sleep Session';
      case 'pumping': return 'Quick Pumping';
      case 'measurements': return 'Quick Measurement';
      case 'milestones': return 'Record Milestone';
      default: return 'Quick Action';
    }
  };

  const renderFormFields = () => {
    switch (type) {
      case 'feeding':
        return (
          <>
            <div>
              <Label className="text-sm font-medium">Type</Label>
              <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
                <SelectTrigger className="mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="bottle">Bottle</SelectItem>
                  <SelectItem value="breast">Breastfeeding</SelectItem>
                  <SelectItem value="solid">Solid Food</SelectItem>
                </SelectContent>
              </Select>
            </div>
            {formData.type === 'bottle' && (
              <div>
                <Label className="text-sm font-medium">Amount (oz)</Label>
                <Input
                  type="number"
                  step="0.5"
                  value={formData.amount}
                  onChange={(e) => setFormData({...formData, amount: e.target.value})}
                  className="mt-1"
                />
              </div>
            )}
            {formData.type === 'breast' && (
              <div>
                <Label className="text-sm font-medium">Duration (minutes)</Label>
                <Input
                  type="number"
                  value={formData.duration}
                  onChange={(e) => setFormData({...formData, duration: e.target.value})}
                  className="mt-1"
                />
              </div>
            )}
          </>
        );
      case 'diaper':
        return (
          <div>
            <Label className="text-sm font-medium">Type</Label>
            <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
              <SelectTrigger className="mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="wet">Wet</SelectItem>
                <SelectItem value="dirty">Dirty</SelectItem>
                <SelectItem value="mixed">Mixed</SelectItem>
              </SelectContent>
            </Select>
          </div>
        );
      case 'sleep':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">
              {data.isCompleting ? 'Complete Sleep Session' : 'Log Sleep Session'}
            </h3>
            {data.isCompleting && (
              <div className="bg-purple-50 p-3 rounded-lg">
                <p className="text-sm text-purple-800">
                  <Clock className="w-4 h-4 inline mr-1" />
                  Sleep Duration: {data.duration} minutes ({Math.floor(data.duration / 60)}h {data.duration % 60}m)
                </p>
              </div>
            )}
            <div>
              <Label>Duration (minutes)</Label>
              <Input
                type="number"
                value={formData.duration || data.duration || ''}
                onChange={(e) => setFormData({...formData, duration: parseInt(e.target.value)})}
                placeholder="60"
                readOnly={data.isCompleting}
              />
              {data.isCompleting && (
                <div className="text-sm text-gray-500 mt-1">
                  Duration automatically calculated from timer. You can adjust if needed.
                </div>
              )}
            </div>
            <div>
              <Label>Sleep Quality</Label>
              <Select value={formData.quality || 'good'} onValueChange={(value) => setFormData({...formData, quality: value})}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="excellent">😴 Excellent</SelectItem>
                  <SelectItem value="good">😊 Good</SelectItem>
                  <SelectItem value="fair">😐 Fair</SelectItem>
                  <SelectItem value="restless">😣 Restless</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        );
      case 'pumping':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">
              {data.isCompleting ? 'Complete Pumping Session' : 'Log Pumping Session'}
            </h3>
            {data.isCompleting && (
              <div className="bg-blue-50 p-3 rounded-lg">
                <p className="text-sm text-blue-800">
                  <Clock className="w-4 h-4 inline mr-1" />
                  Session Duration: {data.duration} minutes
                </p>
              </div>
            )}
            <div className="bg-pink-50 border border-pink-200 rounded-lg p-3 mb-3">
              <p className="text-sm text-pink-800 font-medium">
                💡 Enter the amount pumped from each breast (enter 0 if nothing was pumped)
              </p>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label className="text-sm font-semibold text-blue-700">Left Breast (oz) *</Label>
                <Input
                  type="number"
                  step="0.1"
                  value={formData.leftBreast === 0 ? '0' : (formData.leftBreast || '')}
                  onChange={(e) => setFormData({...formData, leftBreast: parseFloat(e.target.value) || 0})}
                  placeholder="0.0"
                  className="mt-1 border-blue-300 focus:border-blue-500"
                />
              </div>
              <div>
                <Label className="text-sm font-semibold text-purple-700">Right Breast (oz) *</Label>
                <Input
                  type="number"
                  step="0.1"
                  value={formData.rightBreast === 0 ? '0' : (formData.rightBreast || '')}
                  onChange={(e) => setFormData({...formData, rightBreast: parseFloat(e.target.value) || 0})}
                  placeholder="0.0"
                  className="mt-1 border-purple-300 focus:border-purple-500"
                />
              </div>
            </div>
            <div className="text-xs text-gray-500 text-center">
              Total: {((formData.leftBreast || 0) + (formData.rightBreast || 0)).toFixed(1)} oz
            </div>
            <div>
              <Label>Duration (minutes)</Label>
              <Input
                type="number"
                value={formData.duration || data.duration || ''}
                onChange={(e) => setFormData({...formData, duration: parseInt(e.target.value)})}
                placeholder="15"
              />
              {data.isCompleting && (
                <div className="text-sm text-gray-500 mt-1">
                  Duration automatically calculated from timer ({data.duration} min). You can adjust if needed.
                </div>
              )}
            </div>
          </div>
        );
      case 'measurements':
        return (
          <>
            <div>
              <Label className="text-sm font-medium">Weight (lbs)</Label>
              <Input
                type="number"
                step="0.1"
                value={formData.weight}
                onChange={(e) => setFormData({...formData, weight: e.target.value})}
                className="mt-1"
              />
            </div>
            <div>
              <Label className="text-sm font-medium">Height (inches)</Label>
              <Input
                type="number"
                step="0.1"
                value={formData.height}
                onChange={(e) => setFormData({...formData, height: e.target.value})}
                className="mt-1"
              />
            </div>
          </>
        );
      case 'milestones':
        return (
          <>
            <div>
              <Label className="text-sm font-medium">Title</Label>
              <Input
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                placeholder="e.g., First smile"
                className="mt-1"
              />
            </div>
            <div>
              <Label className="text-sm font-medium">Category</Label>
              <Select value={formData.category} onValueChange={(value) => setFormData({...formData, category: value})}>
                <SelectTrigger className="mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="physical">Physical</SelectItem>
                  <SelectItem value="cognitive">Cognitive</SelectItem>
                  <SelectItem value="social">Social</SelectItem>
                  <SelectItem value="feeding">Feeding</SelectItem>
                  <SelectItem value="sleep">Sleep</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl w-full max-w-md flex flex-col" style={{maxHeight: '95vh'}}>
        <div className="flex items-center justify-between p-6 pb-4 flex-shrink-0">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{getModalTitle()}</h3>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="flex flex-col flex-1 min-h-0">
          <div className="px-6 overflow-y-auto flex-1 space-y-4">
            {renderFormFields()}
          </div>
          
          <div className="flex gap-3 p-6 pt-4 flex-shrink-0 border-t">
            <Button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Save className="w-4 h-4 mr-2" />
              Save
            </Button>
            <Button
              type="button"
              onClick={onCancel}
              variant="outline"
              className="flex-1"
            >
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Activity History List Component
const ActivityHistoryList = ({ activities, filter, sortBy, sortOrder, currentBaby }) => {
  // Filter activities - Fix field name mismatch
  const filteredActivities = activities.filter(activity => {
    if (filter === 'all') return true;
    return activity.type === filter || activity.activity_type === filter;
  });

  // Sort activities
  const sortedActivities = [...filteredActivities].sort((a, b) => {
    if (sortBy === 'timestamp') {
      const aTime = new Date(a.timestamp || a.start_time || a.achieved_date);
      const bTime = new Date(b.timestamp || b.start_time || b.achieved_date);
      return sortOrder === 'desc' ? bTime - aTime : aTime - bTime;
    } else if (sortBy === 'type') {
      const aType = a.type || a.activity_type || '';
      const bType = b.type || b.activity_type || '';
      return sortOrder === 'desc' ? bType.localeCompare(aType) : aType.localeCompare(bType);
    }
    return 0;
  });

  if (sortedActivities.length === 0) {
    return (
      <div className="text-center py-8">
        <Activity className="w-12 h-12 mx-auto text-gray-300 mb-4" />
        <h3 className="text-lg font-medium text-gray-500 mb-2">No Activities Found</h3>
        <p className="text-gray-400">
          {filter === 'all' 
            ? `Start logging ${currentBaby?.name || 'your baby'}'s activities to see them here.`
            : `No ${filter} activities recorded yet.`
          }
        </p>
      </div>
    );
  }

  const getActivityIcon = (type) => {
    const icons = {
      feeding: Milk,
      diaper: Droplet,
      sleep: Moon,
      pumping: Zap,
      measurements: Scale,
      milestones: Trophy
    };
    return icons[type] || Activity;
  };

  const getActivityColor = (type) => {
    const colors = {
      feeding: 'bg-blue-100 text-blue-700 border-blue-200',
      diaper: 'bg-green-100 text-green-700 border-green-200',
      sleep: 'bg-purple-100 text-purple-700 border-purple-200',
      pumping: 'bg-pink-100 text-pink-700 border-pink-200',
      measurements: 'bg-orange-100 text-orange-700 border-orange-200',
      milestones: 'bg-yellow-100 text-yellow-700 border-yellow-200'
    };
    return colors[type] || 'bg-gray-100 text-gray-700 border-gray-200';
  };

  const formatActivityDetails = (activity) => {
    const type = activity.activity_type;
    const details = [];
    
    switch (type) {
      case 'feeding':
        // Show feeding type first
        if (activity.feeding_type) {
          details.push({ label: 'Type', value: activity.feeding_type });
        }
        // Show amount and duration
        if (activity.amount) {
          details.push({ label: 'Amount', value: `${activity.amount} oz` });
        }
        if (activity.duration) {
          details.push({ label: 'Duration', value: `${activity.duration} min` });
        }
        break;
        
      case 'diaper':
        if (activity.diaper_type || activity.type) {
          const diaperType = activity.diaper_type || activity.type;
          details.push({ label: 'Type', value: diaperType.charAt(0).toUpperCase() + diaperType.slice(1) });
        }
        break;
        
      case 'sleep':
        if (activity.duration) {
          details.push({ label: 'Duration', value: `${activity.duration} min` });
        }
        if (activity.start_time) {
          const startTime = new Date(activity.start_time);
          details.push({ label: 'Started', value: format(startTime, 'h:mm a') });
        }
        if (activity.end_time) {
          const endTime = new Date(activity.end_time);
          details.push({ label: 'Ended', value: format(endTime, 'h:mm a') });
        }
        break;
        
      case 'pumping':
        // Show individual breast amounts if available
        if (activity.left_breast !== undefined && activity.left_breast > 0) {
          details.push({ label: 'Left', value: `${activity.left_breast} oz` });
        }
        if (activity.right_breast !== undefined && activity.right_breast > 0) {
          details.push({ label: 'Right', value: `${activity.right_breast} oz` });
        }
        
        // Show total amount (always show if > 0, or if no individual amounts)
        const total = (activity.left_breast || 0) + (activity.right_breast || 0);
        if (total > 0) {
          details.push({ label: 'Total', value: `${total} oz` });
        } else if (activity.amount && activity.amount > 0) {
          // Fallback to amount field if no breast-specific data
          details.push({ label: 'Amount', value: `${activity.amount} oz` });
        }
        
        // Always show duration if available
        if (activity.duration) {
          details.push({ label: 'Duration', value: `${activity.duration} min` });
        }
        break;
        
      case 'measurements':
        if (activity.weight) {
          details.push({ label: 'Weight', value: `${activity.weight} lbs` });
        }
        if (activity.height) {
          details.push({ label: 'Height', value: `${activity.height} in` });
        }
        if (activity.head_circumference) {
          details.push({ label: 'Head Circumference', value: `${activity.head_circumference} in` });
        }
        if (activity.temperature) {
          details.push({ label: 'Temperature', value: `${activity.temperature}°F` });
        }
        break;
        
      case 'milestones':
        if (activity.title) {
          details.push({ label: 'Milestone', value: activity.title });
        }
        if (activity.description) {
          details.push({ label: 'Description', value: activity.description });
        }
        if (activity.category) {
          details.push({ label: 'Category', value: activity.category });
        }
        break;
        
      default:
        details.push({ label: 'Info', value: 'Activity logged' });
    }
    
    return details;
  };

  const getActivityTimestamp = (activity) => {
    return activity.timestamp || activity.start_time || activity.achieved_date;
  };

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      <div className="text-sm text-gray-500 mb-4">
        Showing {sortedActivities.length} {filter === 'all' ? 'activities' : `${filter} entries`}
      </div>
      
      {sortedActivities.map((activity, index) => {
        const activityType = activity.type || activity.activity_type;
        const Icon = getActivityIcon(activityType);
        const timestamp = getActivityTimestamp(activity);
        const date = new Date(timestamp);
        
        return (
          <div key={`${activityType}-${activity.id || index}`} 
               className="flex items-start gap-3 p-3 bg-white dark:bg-gray-800 rounded-lg border dark:border-gray-700 hover:shadow-sm transition-shadow">
            {/* Activity Icon */}
            <div className={`w-10 h-10 rounded-full flex items-center justify-center border ${getActivityColor(activityType)}`}>
              <Icon className="w-4 h-4" />
            </div>
            
            {/* Activity Details */}
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 dark:text-white text-sm">
                    {activity.display_type}
                  </h4>
                  
                  {/* Display all activity details */}
                  <div className="mt-2 space-y-1">
                    {formatActivityDetails(activity).map((detail, idx) => (
                      <div key={idx} className="text-sm text-gray-600 flex items-baseline gap-2">
                        <span className="font-medium text-gray-700 dark:text-gray-200">{detail.label}:</span>
                        <span>{detail.value}</span>
                      </div>
                    ))}
                  </div>
                  
                  {activity.notes && (
                    <p className="text-xs text-gray-500 mt-2 italic border-l-2 border-gray-300 pl-2">
                      "{activity.notes}"
                    </p>
                  )}
                </div>
                
                {/* Timestamp */}
                <div className="text-right flex-shrink-0">
                  <div className="text-xs font-medium text-gray-500">
                    {format(date, 'MMM d')}
                  </div>
                  <div className="text-xs text-gray-400">
                    {format(date, 'h:mm a')}
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default TrackingPage;