import React, { useState } from 'react';
import BaseWidget from './BaseWidget';
import { Button } from '../ui/button';
import { RefreshCw, ChefHat, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const MealIdeasWidget = ({ widget, currentBaby, isEditing, onRemove, onSettings }) => {
  const navigate = useNavigate();
  const [mealIdea, setMealIdea] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateAgeInMonths = (birthDate) => {
    if (!birthDate) return 6;
    const birth = new Date(birthDate);
    const now = new Date();
    const diffTime = Math.abs(now - birth);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.floor(diffDays / 30);
  };

  const getMealIdea = async () => {
    if (!currentBaby) return;
    
    setLoading(true);
    try {
      const ageInMonths = calculateAgeInMonths(currentBaby.birth_date);
      const response = await axios.post('/meals/search', {
        query: `meal ideas for ${ageInMonths} month old baby`,
        baby_age_months: ageInMonths
      });
      
      setMealIdea(response.data.results);
    } catch (error) {
      console.error('Error getting meal idea:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickMealTypes = [
    { name: "Breakfast", emoji: "🥣" },
    { name: "Lunch", emoji: "🥪" },
    { name: "Dinner", emoji: "🍽️" },
    { name: "Snack", emoji: "🍌" }
  ];

  return (
    <BaseWidget
      widget={widget}
      isEditing={isEditing}
      onRemove={onRemove}
      onSettings={onSettings}
    >
      {currentBaby ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ChefHat className="h-4 w-4 text-orange-600" />
              <span className="text-sm font-medium">
                For {calculateAgeInMonths(currentBaby.birth_date)} month old
              </span>
            </div>
            <Button
              onClick={getMealIdea}
              size="sm"
              variant="ghost"
              disabled={loading || isEditing}
            >
              {loading ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <RefreshCw className="h-4 w-4" />
              )}
            </Button>
          </div>

          {mealIdea && !isEditing ? (
            <div className="bg-orange-50 p-3 rounded-lg">
              <p className="text-sm text-orange-800 line-clamp-4">{mealIdea}</p>
              <Button
                onClick={() => navigate('/meal-planner')}
                variant="ghost"
                size="sm"
                className="mt-2 p-0 text-orange-600"
              >
                More Ideas <ArrowRight className="h-3 w-3 ml-1" />
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-2">
              {quickMealTypes.map((meal) => (
                <Button
                  key={meal.name}
                  variant="outline"
                  size="sm"
                  disabled={isEditing}
                  className="flex items-center gap-2 text-xs"
                >
                  <span>{meal.emoji}</span>
                  {meal.name}
                </Button>
              ))}
            </div>
          )}

          {!isEditing && (
            <Button 
              onClick={() => navigate('/meal-planner')}
              className="w-full bg-orange-600 hover:bg-orange-700"
              size="sm"
            >
              Full Meal Planner
            </Button>
          )}
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-gray-500 mb-4">Add a baby profile to get personalized meal ideas</p>
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

export default MealIdeasWidget;