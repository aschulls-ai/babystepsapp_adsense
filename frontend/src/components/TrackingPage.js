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
  Check
} from 'lucide-react';
import { toast } from 'sonner';
import { format, formatDistanceToNow } from 'date-fns';

const TrackingPage = ({ currentBaby }) => {
  const [activeTab, setActiveTab] = useState('feeding');
  const [recentActivities, setRecentActivities] = useState({});
  const [reminders, setReminders] = useState([]);
  const [showReminderForm, setShowReminderForm] = useState(false);
  const [notificationPermission, setNotificationPermission] = useState('default');

  useEffect(() => {
    if (currentBaby) {
      fetchRecentActivities();
      fetchReminders();
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
      const endpoints = {
        feeding: '/feedings',
        diaper: '/diapers',
        sleep: '/sleep',
        pumping: '/pumping',
        measurements: '/measurements',
        milestones: '/milestones'
      };

      const response = await axios.get(endpoints[activeTab], {
        params: { baby_id: currentBaby.id }
      });
      
      setRecentActivities(prev => ({
        ...prev,
        [activeTab]: response.data.slice(0, 5)
      }));
    } catch (error) {
      console.error('Failed to fetch recent activities:', error);
    }
  };

  const fetchReminders = async () => {
    if (!currentBaby) return;
    
    try {
      const response = await axios.get('/reminders', {
        params: { baby_id: currentBaby.id }
      });
      setReminders(response.data);
    } catch (error) {
      console.error('Failed to fetch reminders:', error);
    }
  };

  const checkReminders = () => {
    if (!reminders.length || notificationPermission !== 'granted') return;

    const now = new Date();
    
    reminders.forEach(reminder => {
      if (!reminder.enabled) return;

      const reminderTime = new Date(reminder.next_notification);
      
      if (reminderTime <= now && !reminder.notified) {
        showNotification(reminder);
        markReminderAsNotified(reminder.id);
      }
    });
  };

  const showNotification = (reminder) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(`Baby Steps - ${reminder.title}`, {
        body: `Time for ${currentBaby.name}'s ${reminder.type}`,
        icon: '/favicon.ico',
        tag: `reminder-${reminder.id}`
      });
    }
  };

  const markReminderAsNotified = async (reminderId) => {
    try {
      await axios.patch(`/reminders/${reminderId}/notified`);
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
      
      await axios.post('/reminders', backendData);
      toast.success('Reminder created successfully!');
      fetchReminders();
      setShowReminderForm(false);
    } catch (error) {
      toast.error('Failed to create reminder');
    }
  };

  const toggleReminder = async (reminderId, enabled) => {
    try {
      await axios.patch(`/reminders/${reminderId}`, { is_active: enabled });
      toast.success(enabled ? 'Reminder enabled' : 'Reminder disabled');
      fetchReminders();
    } catch (error) {
      toast.error('Failed to update reminder');
    }
  };

  const deleteReminder = async (reminderId) => {
    try {
      await axios.delete(`/reminders/${reminderId}`);
      toast.success('Reminder deleted');
      fetchReminders();
    } catch (error) {
      toast.error('Failed to delete reminder');
    }
  };

  const handleQuickAction = (type) => {
    const quickActions = {
      feeding: () => {
        // Quick log with default values
        axios.post('/feedings', {
          baby_id: currentBaby.id,
          type: 'bottle',
          amount: 4, // default amount
          timestamp: new Date().toISOString()
        }).then(() => {
          toast.success('Quick feeding logged!');
          fetchRecentActivities();
        }).catch(() => toast.error('Failed to log feeding'));
      },
      diaper: () => {
        axios.post('/diapers', {
          baby_id: currentBaby.id,
          type: 'wet',
          timestamp: new Date().toISOString()
        }).then(() => {
          toast.success('Diaper change logged!');
          fetchRecentActivities();
        }).catch(() => toast.error('Failed to log diaper change'));
      },
      sleep: () => {
        axios.post('/sleep', {
          baby_id: currentBaby.id,
          start_time: new Date().toISOString()
        }).then(() => {
          toast.success('Sleep session started!');
          fetchRecentActivities();
        }).catch(() => toast.error('Failed to start sleep session'));
      },
      pumping: () => setActiveTab('pumping'),
      measurements: () => setActiveTab('measurements'),
      milestones: () => setActiveTab('milestones')
    };
    
    quickActions[type]();
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
            <p className="text-gray-600">Please select or add a baby to start tracking activities.</p>
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
          <h1 className="text-4xl font-bold font-display text-gray-900" data-testid="tracking-title">
            Track Activities
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Log {currentBaby.name}'s daily activities and milestones
          </p>
        </div>
      </div>

      {/* Quick Action Buttons */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
        <QuickActionButton 
          icon={Milk} 
          label="Quick Feed" 
          color="blue"
          onClick={() => handleQuickAction('feeding')}
        />
        <QuickActionButton 
          icon={Droplet} 
          label="Diaper Change" 
          color="green"
          onClick={() => handleQuickAction('diaper')}
        />
        <QuickActionButton 
          icon={Moon} 
          label="Start Sleep" 
          color="purple"
          onClick={() => handleQuickAction('sleep')}
        />
        <QuickActionButton 
          icon={Activity} 
          label="Pumping" 
          color="pink"
          onClick={() => handleQuickAction('pumping')}
        />
        <QuickActionButton 
          icon={Scale} 
          label="Measure" 
          color="orange"
          onClick={() => handleQuickAction('measurements')}
        />
        <QuickActionButton 
          icon={Trophy} 
          label="Milestone" 
          color="yellow"
          onClick={() => handleQuickAction('milestones')}
        />
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Tracking Forms */}
        <div className="lg:col-span-2">
          <Card className="glass-strong border-0">
            <CardContent className="p-6">
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList className="grid grid-cols-3 lg:grid-cols-6 mb-6 bg-gray-100 p-1 rounded-xl">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <TabsTrigger
                        key={tab.id}
                        value={tab.id}
                        className="rounded-lg data-[state=active]:bg-white data-[state=active]:shadow-md transition-all duration-200 flex items-center gap-1 px-2 py-2"
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

        <div className="space-y-6">
          {/* Reminders Section */}
          <Card className="glass border-0">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2 text-gray-800">
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

          {/* Recent Activities */}
          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Clock className="w-5 h-5 text-rose-500" />
                Recent {tabs.find(t => t.id === activeTab)?.label}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <RecentActivityList 
                activities={recentActivities[activeTab] || []}
                type={activeTab}
              />
            </CardContent>
          </Card>
        </div>
      </div>
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

      await axios.post('/feedings', data);
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
          <Label className="text-sm font-medium text-gray-700">Feeding Type</Label>
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
            <Label className="text-sm font-medium text-gray-700">Amount (oz)</Label>
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
            <Label className="text-sm font-medium text-gray-700">Duration (minutes)</Label>
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
        <Label className="text-sm font-medium text-gray-700">Notes (optional)</Label>
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

      await axios.post('/diapers', data);
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
        <Label className="text-sm font-medium text-gray-700">Diaper Type</Label>
        <Select value={formData.type} onValueChange={(value) => setFormData({...formData, type: value})}>
          <SelectTrigger data-testid="diaper-type-selector">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="wet">Wet</SelectItem>
            <SelectItem value="dirty">Dirty</SelectItem>
            <SelectItem value="mixed">Mixed (Wet & Dirty)</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700">Notes (optional)</Label>
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
      const data = {
        baby_id: babyId,
        start_time: formData.start_time.toISOString(),
        end_time: formData.end_time ? new Date(formData.end_time).toISOString() : null,
        quality: formData.quality || null,
        notes: formData.notes || null
      };

      await axios.post('/sleep', data);
      toast.success('Sleep session logged successfully!');
      setFormData({
        start_time: new Date(),
        end_time: '',
        quality: '',
        notes: ''
      });
      onSuccess();
    } catch (error) {
      toast.error('Failed to log sleep session');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700">Start Time</Label>
          <Input
            type="datetime-local"
            value={format(formData.start_time, "yyyy-MM-dd'T'HH:mm")}
            onChange={(e) => setFormData({...formData, start_time: new Date(e.target.value)})}
            data-testid="sleep-start-time-input"
          />
        </div>

        <div className="space-y-2">
          <Label className="text-sm font-medium text-gray-700">End Time (optional)</Label>
          <Input
            type="datetime-local"
            value={formData.end_time}
            onChange={(e) => setFormData({...formData, end_time: e.target.value})}
            data-testid="sleep-end-time-input"
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700">Sleep Quality (optional)</Label>
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
        <Label className="text-sm font-medium text-gray-700">Notes (optional)</Label>
        <Textarea
          placeholder="Sleep environment, interruptions, etc..."
          value={formData.notes}
          onChange={(e) => setFormData({...formData, notes: e.target.value})}
          data-testid="sleep-notes-input"
        />
      </div>

      <Button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-purple-500 to-violet-500 hover:from-purple-600 hover:to-violet-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="save-sleep-btn"
      >
        {loading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Saving...
          </div>
        ) : (
          <>
            <Save className="w-5 h-5 mr-2" />
            Log Sleep Session
          </>
        )}
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

      await axios.post('/pumping', data);
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
          <Label className="text-sm font-medium text-gray-700">Amount (oz) *</Label>
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
          <Label className="text-sm font-medium text-gray-700">Duration (minutes) *</Label>
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
        <Label className="text-sm font-medium text-gray-700">Notes (optional)</Label>
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

      await axios.post('/measurements', data);
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
          <Label className="text-sm font-medium text-gray-700">Weight (lbs)</Label>
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
          <Label className="text-sm font-medium text-gray-700">Height (inches)</Label>
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
          <Label className="text-sm font-medium text-gray-700">Head Circumference (inches)</Label>
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
          <Label className="text-sm font-medium text-gray-700">Temperature (°F)</Label>
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
        <Label className="text-sm font-medium text-gray-700">Notes (optional)</Label>
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

      await axios.post('/milestones', data);
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
      toast.error('Failed to log milestone');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700">Milestone Title *</Label>
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
        <Label className="text-sm font-medium text-gray-700">Category</Label>
        <Select value={formData.category} onValueChange={(value) => setFormData({...formData, category: value})}>
          <SelectTrigger data-testid="milestone-category-selector">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="physical">Physical Development</SelectItem>
            <SelectItem value="cognitive">Cognitive Development</SelectItem>
            <SelectItem value="social">Social Development</SelectItem>
            <SelectItem value="feeding">Feeding</SelectItem>
            <SelectItem value="sleep">Sleep</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700">Achievement Date</Label>
        <Input
          type="date"
          value={format(formData.achieved_date, 'yyyy-MM-dd')}
          onChange={(e) => setFormData({...formData, achieved_date: new Date(e.target.value)})}
          data-testid="milestone-date-input"
        />
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700">Description (optional)</Label>
        <Textarea
          placeholder="Describe the milestone in detail..."
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          data-testid="milestone-description-input"
        />
      </div>

      <div className="space-y-2">
        <Label className="text-sm font-medium text-gray-700">Notes (optional)</Label>
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
        return {
          title: `${activity.type.charAt(0).toUpperCase() + activity.type.slice(1)} feeding`,
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
            <p className="text-sm text-gray-600">{formatted.subtitle}</p>
            <p className="text-xs text-gray-400 mt-1">{formatted.time}</p>
          </div>
        );
      })}
    </div>
  );
};

// Quick Action Button Component
const QuickActionButton = ({ icon: Icon, label, color, onClick }) => {
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
      className={`${colorClasses[color]} p-4 rounded-xl transition-all duration-200 hover:scale-105 hover:shadow-md flex flex-col items-center gap-2 text-center`}
    >
      <Icon className="w-6 h-6" />
      <span className="text-sm font-medium">{label}</span>
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
        const nextTime = new Date(reminder.next_notification);
        return (
          <div key={reminder.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h4 className="font-medium text-gray-800 text-sm">{reminder.title}</h4>
                <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
                  {reminder.type}
                </span>
              </div>
              <p className="text-xs text-gray-600 mt-1">
                Next: {format(nextTime, 'MMM d, h:mm a')} ({reminder.frequency})
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => onToggle(reminder.id, !reminder.enabled)}
                className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
                  reminder.enabled 
                    ? 'bg-green-100 text-green-600 hover:bg-green-200' 
                    : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                }`}
                title={reminder.enabled ? 'Disable' : 'Enable'}
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

export default TrackingPage;