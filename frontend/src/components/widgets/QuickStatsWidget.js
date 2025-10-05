import React, { useState, useEffect } from 'react';
import BaseWidget from './BaseWidget';
import { Clock, Baby, TrendingUp, Activity } from 'lucide-react';
import axios from 'axios';

const QuickStatsWidget = ({ widget, currentBaby, isEditing, onRemove, onSettings }) => {
  const [stats, setStats] = useState({
    todayFeedings: 0,
    lastSleep: null,
    todayDiapers: 0,
    totalActivities: 0
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentBaby && !isEditing) {
      fetchTodayStats();
    }
  }, [currentBaby, isEditing]);

  const fetchTodayStats = async () => {
    setLoading(true);
    try {
      const today = new Date().toISOString().split('T')[0];
      
      const [feedings, diapers, sleeps] = await Promise.all([
        axios.get(`/feedings?baby_id=${currentBaby.id}`).catch(() => ({ data: [] })),
        axios.get(`/diapers?baby_id=${currentBaby.id}`).catch(() => ({ data: [] })),
        axios.get(`/sleep?baby_id=${currentBaby.id}`).catch(() => ({ data: [] }))
      ]);

      // Filter for today's activities
      const todayFeedings = feedings.data.filter(f => 
        f.start_time && f.start_time.startsWith(today)
      ).length;

      const todayDiapers = diapers.data.filter(d => 
        d.checked_at && d.checked_at.startsWith(today)
      ).length;

      const lastSleep = sleeps.data
        .filter(s => s.start_time)
        .sort((a, b) => new Date(b.start_time) - new Date(a.start_time))[0];

      setStats({
        todayFeedings,
        lastSleep,
        todayDiapers,
        totalActivities: todayFeedings + todayDiapers + sleeps.data.length
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatLastSleep = (sleep) => {
    if (!sleep || !sleep.start_time) return 'No sleep recorded';
    
    const sleepTime = new Date(sleep.start_time);
    const now = new Date();
    const diffHours = Math.floor((now - sleepTime) / (1000 * 60 * 60));
    const diffMinutes = Math.floor(((now - sleepTime) % (1000 * 60 * 60)) / (1000 * 60));
    
    if (diffHours > 0) {
      return `${diffHours}h ${diffMinutes}m ago`;
    } else {
      return `${diffMinutes}m ago`;
    }
  };

  const statItems = [
    {
      icon: Bottle,
      label: "Today's Feedings",
      value: stats.todayFeedings,
      color: "text-blue-600"
    },
    {
      icon: Baby,
      label: "Diaper Changes",
      value: stats.todayDiapers,
      color: "text-green-600"
    },
    {
      icon: Clock,
      label: "Last Sleep",
      value: formatLastSleep(stats.lastSleep),
      color: "text-purple-600"
    },
    {
      icon: TrendingUp,
      label: "Total Activities",
      value: stats.totalActivities,
      color: "text-orange-600"
    }
  ];

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
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {statItems.map((item, index) => (
                <div key={index} className="bg-gray-50 p-3 rounded-lg text-center">
                  <item.icon className={`h-5 w-5 ${item.color} mx-auto mb-2`} />
                  <p className="text-lg font-semibold">{item.value}</p>
                  <p className="text-xs text-gray-600">{item.label}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-gray-500">Select a baby to view stats</p>
        </div>
      )}
    </BaseWidget>
  );
};

export default QuickStatsWidget;