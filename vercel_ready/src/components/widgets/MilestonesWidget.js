import React, { useState, useEffect } from 'react';
import BaseWidget from './BaseWidget';
import { Button } from '../ui/button';
import { CheckCircle, Circle, Star, Calendar, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const MilestonesWidget = ({ widget, currentBaby, isEditing, onRemove, onSettings }) => {
  const navigate = useNavigate();
  const [currentMilestones, setCurrentMilestones] = useState([]);
  const [upcomingMilestones, setUpcomingMilestones] = useState([]);

  useEffect(() => {
    if (currentBaby) {
      const ageInMonths = calculateAgeInMonths(currentBaby.birth_date);
      const milestones = getMilestonesByAge(ageInMonths);
      setCurrentMilestones(milestones.current);
      setUpcomingMilestones(milestones.upcoming);
    }
  }, [currentBaby]);

  const calculateAgeInMonths = (birthDate) => {
    if (!birthDate) return 0;
    const birth = new Date(birthDate);
    const now = new Date();
    const diffTime = Math.abs(now - birth);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.floor(diffDays / 30);
  };

  const getMilestonesByAge = (ageInMonths) => {
    const allMilestones = {
      0: [
        { id: 1, category: 'Physical', milestone: 'Holds head up briefly', type: 'current' },
        { id: 2, category: 'Social', milestone: 'Makes eye contact', type: 'current' },
        { id: 3, category: 'Communication', milestone: 'Cries to communicate needs', type: 'current' }
      ],
      2: [
        { id: 4, category: 'Physical', milestone: 'Holds head steady', type: 'current' },
        { id: 5, category: 'Social', milestone: 'Smiles responsively', type: 'current' },
        { id: 6, category: 'Communication', milestone: 'Coos and makes sounds', type: 'current' }
      ],
      4: [
        { id: 7, category: 'Physical', milestone: 'Rolls from tummy to back', type: 'current' },
        { id: 8, category: 'Social', milestone: 'Laughs and shows joy', type: 'current' },
        { id: 9, category: 'Cognitive', milestone: 'Pays attention to faces', type: 'current' }
      ],
      6: [
        { id: 10, category: 'Physical', milestone: 'Sits with support', type: 'current' },
        { id: 11, category: 'Communication', milestone: 'Babbles (ba-ba, ma-ma)', type: 'current' },
        { id: 12, category: 'Cognitive', milestone: 'Looks for dropped objects', type: 'current' }
      ],
      9: [
        { id: 13, category: 'Physical', milestone: 'Crawls or scoots', type: 'current' },
        { id: 14, category: 'Social', milestone: 'Shows stranger anxiety', type: 'current' },
        { id: 15, category: 'Cognitive', milestone: 'Plays peek-a-boo', type: 'current' }
      ],
      12: [
        { id: 16, category: 'Physical', milestone: 'Stands alone', type: 'current' },
        { id: 17, category: 'Communication', milestone: 'Says first words', type: 'current' },
        { id: 18, category: 'Cognitive', milestone: 'Imitates actions', type: 'current' }
      ],
      15: [
        { id: 19, category: 'Physical', milestone: 'Walks independently', type: 'current' },
        { id: 20, category: 'Communication', milestone: 'Says 3-5 words', type: 'current' },
        { id: 21, category: 'Social', milestone: 'Shows affection to familiar people', type: 'current' }
      ],
      18: [
        { id: 22, category: 'Physical', milestone: 'Runs and climbs', type: 'current' },
        { id: 23, category: 'Communication', milestone: 'Says 10-20 words', type: 'current' },
        { id: 24, category: 'Cognitive', milestone: 'Sorts shapes and colors', type: 'current' }
      ],
      24: [
        { id: 25, category: 'Physical', milestone: 'Kicks ball, jumps', type: 'current' },
        { id: 26, category: 'Communication', milestone: 'Uses 2-word phrases', type: 'current' },
        { id: 27, category: 'Social', milestone: 'Plays alongside other children', type: 'current' }
      ]
    };

    // Get current milestones (closest age group <= baby's age)
    const currentAgeGroups = Object.keys(allMilestones)
      .map(Number)
      .filter(age => age <= ageInMonths)
      .sort((a, b) => b - a);
    
    const currentGroup = currentAgeGroups[0] || 0;
    const current = allMilestones[currentGroup] || [];

    // Get upcoming milestones (next age group > baby's age)
    const upcomingAgeGroups = Object.keys(allMilestones)
      .map(Number)
      .filter(age => age > ageInMonths)
      .sort((a, b) => a - b);
    
    const upcomingGroup = upcomingAgeGroups[0];
    const upcoming = upcomingGroup ? allMilestones[upcomingGroup].slice(0, 3) : [];

    return { current, upcoming };
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Physical': 'text-blue-600 bg-blue-50',
      'Social': 'text-pink-600 bg-pink-50',
      'Communication': 'text-green-600 bg-green-50',
      'Cognitive': 'text-purple-600 bg-purple-50'
    };
    return colors[category] || 'text-gray-600 bg-gray-50';
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Physical': return '🤸';
      case 'Social': return '👶';
      case 'Communication': return '💬';
      case 'Cognitive': return '🧠';
      default: return '⭐';
    }
  };

  if (!currentBaby) {
    return (
      <BaseWidget
        widget={widget}
        isEditing={isEditing}
        onRemove={onRemove}
        onSettings={onSettings}
      >
        <div className="text-center py-8">
          <Star className="w-8 h-8 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-500 mb-4">Add a baby profile to track developmental milestones</p>
          {!isEditing && (
            <Button 
              onClick={() => navigate('/baby-profile')}
              size="sm"
            >
              Add Baby Profile
            </Button>
          )}
        </div>
      </BaseWidget>
    );
  }

  const babyAge = calculateAgeInMonths(currentBaby.birth_date);

  return (
    <BaseWidget
      widget={widget}
      isEditing={isEditing}
      onRemove={onRemove}
      onSettings={onSettings}
    >
      <div className="space-y-4">
        {/* Current Age Milestones */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h4 className="font-semibold text-sm flex items-center gap-2">
              <Calendar className="w-4 h-4 text-green-600" />
              Expected at {babyAge} months
            </h4>
          </div>
          
          {currentMilestones.length > 0 ? (
            <div className="space-y-2">
              {currentMilestones.slice(0, 3).map((milestone) => (
                <div key={milestone.id} className={`p-2 rounded-lg ${getCategoryColor(milestone.category)} flex items-start gap-2`}>
                  <span className="text-sm mt-0.5">{getCategoryIcon(milestone.category)}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium opacity-80">{milestone.category}</p>
                    <p className="text-sm font-medium">{milestone.milestone}</p>
                  </div>
                  <Circle className="w-4 h-4 mt-0.5 opacity-60" />
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-gray-500">Loading milestones...</p>
          )}
        </div>

        {/* Upcoming Milestones */}
        {upcomingMilestones.length > 0 && (
          <div>
            <h4 className="font-semibold text-xs text-gray-600 mb-2 flex items-center gap-1">
              <ArrowRight className="w-3 h-3" />
              Coming up next
            </h4>
            <div className="space-y-1">
              {upcomingMilestones.slice(0, 2).map((milestone) => (
                <div key={milestone.id} className="p-2 bg-gray-50 rounded border-l-2 border-gray-300">
                  <p className="text-xs text-gray-600 flex items-center gap-1">
                    <span>{getCategoryIcon(milestone.category)}</span>
                    {milestone.milestone}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        {!isEditing && (
          <div className="space-y-2">
            <Button 
              onClick={() => navigate('/tracking')}
              className="w-full"
              size="sm"
              variant="outline"
            >
              Track Development
            </Button>
          </div>
        )}

        {/* Disclaimer */}
        <div className="text-xs text-gray-500 text-center">
          ⚠️ All babies develop at their own pace
        </div>
      </div>
    </BaseWidget>
  );
};

export default MilestonesWidget;