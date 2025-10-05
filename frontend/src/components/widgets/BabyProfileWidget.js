import React from 'react';
import BaseWidget from './BaseWidget';
import { Button } from '../ui/button';
import { Calendar, Weight, Ruler } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const BabyProfileWidget = ({ widget, currentBaby, isEditing, onRemove, onSettings }) => {
  const navigate = useNavigate();

  const calculateAge = (birthDate) => {
    if (!birthDate) return 'Unknown';
    const birth = new Date(birthDate);
    const now = new Date();
    const diffTime = Math.abs(now - birth);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 30) {
      return `${diffDays} days old`;
    } else if (diffDays < 365) {
      const months = Math.floor(diffDays / 30);
      return `${months} month${months > 1 ? 's' : ''} old`;
    } else {
      const years = Math.floor(diffDays / 365);
      const months = Math.floor((diffDays % 365) / 30);
      return `${years} year${years > 1 ? 's' : ''} ${months > 0 ? `${months} month${months > 1 ? 's' : ''}` : ''} old`;
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
        <div className="space-y-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-2xl">👶</span>
            </div>
            <h3 className="font-semibold text-lg">{currentBaby.name}</h3>
            <p className="text-sm text-gray-600">{calculateAge(currentBaby.birth_date)}</p>
          </div>
          
          <div className="grid grid-cols-1 gap-3">
            {currentBaby.birth_weight && (
              <div className="flex items-center gap-2 text-sm">
                <Weight className="h-4 w-4 text-gray-500" />
                <span>Birth Weight: {currentBaby.birth_weight} lbs</span>
              </div>
            )}
            {currentBaby.birth_length && (
              <div className="flex items-center gap-2 text-sm">
                <Ruler className="h-4 w-4 text-gray-500" />
                <span>Birth Length: {currentBaby.birth_length} in</span>
              </div>
            )}
            <div className="flex items-center gap-2 text-sm">
              <Calendar className="h-4 w-4 text-gray-500" />
              <span>Born: {new Date(currentBaby.birth_date).toLocaleDateString()}</span>
            </div>
          </div>
          
          {!isEditing && (
            <Button 
              onClick={() => navigate('/baby-profile')}
              className="w-full mt-3"
              size="sm"
            >
              View Full Profile
            </Button>
          )}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-gray-500 mb-4">No baby profile yet</p>
          {!isEditing && (
            <Button 
              onClick={() => navigate('/baby-profile')}
              size="sm"
            >
              Add Baby Profile
            </Button>
          )}
        </div>
      )}
    </BaseWidget>
  );
};

export default BabyProfileWidget;