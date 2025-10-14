import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Bell, Clock, Edit2, X, Check } from 'lucide-react';

const FeedReminder = ({ currentBaby }) => {
  const [reminderHours, setReminderHours] = useState(3); // Default: 3 hours
  const [reminderMinutes, setReminderMinutes] = useState(0); // Default: 0 minutes
  const [lastFeedTime, setLastFeedTime] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [tempHours, setTempHours] = useState(3);
  const [tempMinutes, setTempMinutes] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState('');
  const [isDue, setIsDue] = useState(false);

  // Load last feed time from localStorage on mount
  useEffect(() => {
    if (currentBaby) {
      const stored = localStorage.getItem(`lastFeed_${currentBaby.id}`);
      if (stored) {
        setLastFeedTime(new Date(stored));
      }
      
      // Load saved interval (hours and minutes)
      const savedHours = localStorage.getItem(`feedIntervalHours_${currentBaby.id}`);
      const savedMinutes = localStorage.getItem(`feedIntervalMinutes_${currentBaby.id}`);
      
      if (savedHours) {
        setReminderHours(parseInt(savedHours));
        setTempHours(parseInt(savedHours));
      }
      
      if (savedMinutes) {
        setReminderMinutes(parseInt(savedMinutes));
        setTempMinutes(parseInt(savedMinutes));
      }
    }
  }, [currentBaby]);

  // Update timer every minute
  useEffect(() => {
    const updateTimer = () => {
      if (!lastFeedTime || (reminderHours === 0 && reminderMinutes === 0)) {
        setTimeRemaining('Not set');
        setIsDue(false);
        return;
      }

      const now = new Date();
      const totalMinutes = reminderHours * 60 + reminderMinutes;
      const nextFeedTime = new Date(lastFeedTime.getTime() + totalMinutes * 60 * 1000);
      const diffMs = nextFeedTime - now;

      if (diffMs <= 0) {
        setTimeRemaining('Feed is due now!');
        setIsDue(true);
      } else {
        const hours = Math.floor(diffMs / (1000 * 60 * 60));
        const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        
        if (hours > 0 && minutes > 0) {
          setTimeRemaining(`${hours}h ${minutes}m`);
        } else if (hours > 0) {
          setTimeRemaining(`${hours}h`);
        } else {
          setTimeRemaining(`${minutes}m`);
        }
        setIsDue(false);
      }
    };

    updateTimer();
    const timer = setInterval(updateTimer, 60000); // Update every minute

    return () => clearInterval(timer);
  }, [lastFeedTime, reminderHours, reminderMinutes]);

  const handleStartReminder = () => {
    const now = new Date();
    setLastFeedTime(now);
    localStorage.setItem(`lastFeed_${currentBaby.id}`, now.toISOString());
    setIsDue(false);
  };

  const handleSaveInterval = () => {
    setReminderHours(tempHours);
    setReminderMinutes(tempMinutes);
    localStorage.setItem(`feedIntervalHours_${currentBaby.id}`, tempHours.toString());
    localStorage.setItem(`feedIntervalMinutes_${currentBaby.id}`, tempMinutes.toString());
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setTempHours(reminderHours);
    setTempMinutes(reminderMinutes);
    setIsEditing(false);
  };

  const handleReset = () => {
    setLastFeedTime(null);
    setIsDue(false);
    localStorage.removeItem(`lastFeed_${currentBaby.id}`);
  };

  if (!currentBaby) return null;

  return (
    <Card className={`glass border-0 ${isDue ? 'ring-2 ring-red-500 animate-pulse' : ''}`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <Bell className={`w-5 h-5 ${isDue ? 'text-red-500' : 'text-blue-500'}`} />
          Next Feed is Due
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Time Display */}
        <div className="text-center py-4">
          {lastFeedTime ? (
            <>
              <div className={`text-4xl font-bold ${isDue ? 'text-red-600' : 'text-blue-600'}`}>
                {timeRemaining}
              </div>
              <p className="text-sm text-gray-600 mt-2">
                {isDue ? 'Time to feed!' : 'Until next feed'}
              </p>
            </>
          ) : (
            <>
              <div className="text-2xl font-semibold text-gray-400">
                No reminder set
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Start tracking to get reminders
              </p>
            </>
          )}
        </div>

        {/* Interval Setting */}
        <div className="border-t pt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600">Reminder interval:</span>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="text-blue-600 hover:text-blue-700"
              >
                <Edit2 className="w-4 h-4" />
              </button>
            )}
          </div>

          {isEditing ? (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                {/* Hours Input */}
                <div className="space-y-1">
                  <label className="text-xs text-gray-500">Hours</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min="0"
                      max="24"
                      value={tempHours}
                      onChange={(e) => setTempHours(parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 border-2 border-gray-200 dark:border-gray-600 dark:bg-gray-800 dark:text-white rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all"
                    />
                    <span className="text-gray-600 dark:text-gray-400 text-sm">h</span>
                  </div>
                </div>
                
                {/* Minutes Input */}
                <div className="space-y-1">
                  <label className="text-xs text-gray-500">Minutes</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min="0"
                      max="59"
                      value={tempMinutes}
                      onChange={(e) => setTempMinutes(parseInt(e.target.value) || 0)}
                      className="w-full px-3 py-2 border-2 border-gray-200 dark:border-gray-600 dark:bg-gray-800 dark:text-white rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all"
                    />
                    <span className="text-gray-600 dark:text-gray-400 text-sm">m</span>
                  </div>
                </div>
              </div>
              
              {/* Quick Presets */}
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => { setTempHours(0); setTempMinutes(30); }}
                  className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
                >
                  30 min
                </button>
                <button
                  onClick={() => { setTempHours(1); setTempMinutes(0); }}
                  className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
                >
                  1 hour
                </button>
                <button
                  onClick={() => { setTempHours(2); setTempMinutes(0); }}
                  className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
                >
                  2 hours
                </button>
                <button
                  onClick={() => { setTempHours(2); setTempMinutes(30); }}
                  className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
                >
                  2h 30m
                </button>
                <button
                  onClick={() => { setTempHours(3); setTempMinutes(0); }}
                  className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
                >
                  3 hours
                </button>
              </div>
              
              <div className="flex gap-2">
                <Button
                  onClick={handleSaveInterval}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                  size="sm"
                >
                  <Check className="w-4 h-4 mr-1" />
                  Save
                </Button>
                <Button
                  onClick={handleCancelEdit}
                  variant="outline"
                  className="flex-1"
                  size="sm"
                >
                  <X className="w-4 h-4 mr-1" />
                  Cancel
                </Button>
              </div>
            </div>
          ) : (
            <div className="text-center py-2 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
              <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {reminderHours > 0 && `${reminderHours}h `}
                {reminderMinutes > 0 && `${reminderMinutes}m`}
                {reminderHours === 0 && reminderMinutes === 0 && '0m'}
              </span>
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          {lastFeedTime ? (
            <>
              <Button
                onClick={handleStartReminder}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
              >
                <Clock className="w-4 h-4 mr-2" />
                Reset Timer
              </Button>
              <Button
                onClick={handleReset}
                variant="outline"
                className="flex-1"
              >
                Clear
              </Button>
            </>
          ) : (
            <Button
              onClick={handleStartReminder}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white"
            >
              <Clock className="w-4 h-4 mr-2" />
              Start Reminder
            </Button>
          )}
        </div>

        {/* Info Text */}
        <p className="text-xs text-gray-500 text-center">
          Internal app reminder only. No device notifications will be sent.
        </p>
      </CardContent>
    </Card>
  );
};

export default FeedReminder;
