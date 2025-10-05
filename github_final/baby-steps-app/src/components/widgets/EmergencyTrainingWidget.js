import React from 'react';
import BaseWidget from './BaseWidget';
import { Button } from '../ui/button';
import { AlertTriangle, Heart, Phone } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const EmergencyTrainingWidget = ({ widget, isEditing, onRemove, onSettings }) => {
  const navigate = useNavigate();

  const emergencyActions = [
    {
      icon: AlertTriangle,
      title: "Choking",
      description: "Back blows & chest thrusts",
      color: "text-red-600 bg-red-50"
    },
    {
      icon: Heart,
      title: "CPR",
      description: "Infant CPR steps",
      color: "text-pink-600 bg-pink-50"
    },
    {
      icon: Phone,
      title: "Emergency",
      description: "Call 911 immediately",
      color: "text-orange-600 bg-orange-50"
    }
  ];

  return (
    <BaseWidget
      widget={widget}
      isEditing={isEditing}
      onRemove={onRemove}
      onSettings={onSettings}
    >
      <div className="space-y-4">
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-xs text-red-800 font-medium text-center">
            🚨 For Real Emergencies: Call 911 First
          </p>
        </div>

        <div className="space-y-2">
          {emergencyActions.map((action, index) => (
            <div key={index} className={`p-3 rounded-lg ${action.color} flex items-center gap-3`}>
              <action.icon className="h-5 w-5" />
              <div className="flex-1">
                <p className="font-medium text-sm">{action.title}</p>
                <p className="text-xs opacity-80">{action.description}</p>
              </div>
            </div>
          ))}
        </div>

        {!isEditing && (
          <Button 
            onClick={() => navigate('/emergency-training')}
            className="w-full bg-red-600 hover:bg-red-700"
            size="sm"
          >
            Full Training Guide
          </Button>
        )}

        <div className="text-xs text-gray-600 text-center">
          ⚠️ This is educational content only. Get certified CPR training.
        </div>
      </div>
    </BaseWidget>
  );
};

export default EmergencyTrainingWidget;