import React, { useState, useEffect } from 'react';
import BaseWidget from './BaseWidget';
import { Button } from '../ui/button';
import { Moon, Baby } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const RecentActivitiesWidget = ({ widget, currentBaby, isEditing, onRemove, onSettings }) => {
  const navigate = useNavigate();
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentBaby && !isEditing) {
      fetchRecentActivities();
    }
  }, [currentBaby, isEditing]);

  const fetchRecentActivities = async () => {
    setLoading(true);
    try {
      // Fetch recent activities from different endpoints
      const [feedings, diapers, sleeps] = await Promise.all([
        axios.get(`/feedings?baby_id=${currentBaby.id}&limit=3`).catch(() => ({ data: [] })),
        axios.get(`/diapers?baby_id=${currentBaby.id}&limit=3`).catch(() => ({ data: [] })),
        axios.get(`/sleep?baby_id=${currentBaby.id}&limit=3`).catch(() => ({ data: [] }))
      ]);

      const allActivities = [
        ...feedings.data.map(f => ({ ...f, type: 'feeding', icon: '🍼', time: f.start_time || f.created_at })),
        ...diapers.data.map(d => ({ ...d, type: 'diaper', icon: '👶', time: d.checked_at || d.created_at })),
        ...sleeps.data.map(s => ({ ...s, type: 'sleep', icon: '😴', time: s.start_time || s.created_at }))
      ];

      // Sort by time and take most recent 5
      const sortedActivities = allActivities
        .sort((a, b) => new Date(b.time) - new Date(a.time))
        .slice(0, 5);

      setActivities(sortedActivities);
    } catch (error) {
      console.error('Error fetching activities:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timeString) => {
    return new Date(timeString).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getActivityDescription = (activity) => {
    switch (activity.type) {
      case 'feeding':
        return `Fed ${activity.amount}oz ${activity.type}`;
      case 'diaper':
        return `Diaper: ${activity.type}`;
      case 'sleep':
        return `Sleep: ${activity.duration ? `${activity.duration}min` : 'Started'}`;
      default:
        return 'Activity recorded';
    }
  };

  return (
    <BaseWidget
      widget={widget}
      isEditing={isEditing}
      onRemove={onRemove}
      onSettings={onSettings}
    >
      {currentBaby ? (
        <div className="space-y-3">
          {loading ? (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
            </div>
          ) : activities.length > 0 ? (
            <>
              <div className="space-y-2">
                {activities.map((activity, index) => (
                  <div key={index} className="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                    <span className="text-lg">{activity.icon}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate">
                        {getActivityDescription(activity)}
                      </p>
                      <p className="text-xs text-gray-500">
                        {formatTime(activity.time)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
              {!isEditing && (
                <Button 
                  onClick={() => navigate('/tracking')}
                  className="w-full"
                  size="sm"
                >
                  View All Activities
                </Button>
              )}
            </>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500 mb-4">No activities recorded yet</p>
              {!isEditing && (
                <Button 
                  onClick={() => navigate('/tracking')}
                  size="sm"
                >
                  Start Tracking
                </Button>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-gray-500">Select a baby to view activities</p>
        </div>
      )}
    </BaseWidget>
  );
};

export default RecentActivitiesWidget;