import React, { useState } from 'react';
import BaseWidget from './BaseWidget';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Search, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const FoodSafetyQuickWidget = ({ widget, currentBaby, isEditing, onRemove, onSettings }) => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const quickSuggestions = [
    'honey',
    'peanuts',
    'eggs',
    'strawberries'
  ];

  const handleSearch = async (searchQuery = query) => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('/food/research', {
        query: `Is ${searchQuery} safe for my baby?`,
        baby_age_months: currentBaby ? calculateAgeInMonths(currentBaby.birth_date) : 6
      });
      
      setResult(response.data.results);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateAgeInMonths = (birthDate) => {
    if (!birthDate) return 6;
    const birth = new Date(birthDate);
    const now = new Date();
    const diffTime = Math.abs(now - birth);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return Math.floor(diffDays / 30);
  };

  const handleQuickCheck = (food) => {
    setQuery(food);
    handleSearch(food);
  };

  return (
    <BaseWidget
      widget={widget}
      isEditing={isEditing}
      onRemove={onRemove}
      onSettings={onSettings}
    >
      <div className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="Check if food is safe..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="flex-1"
            disabled={isEditing}
          />
          <Button
            onClick={() => handleSearch()}
            size="sm"
            disabled={loading || !query.trim() || isEditing}
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <Search className="h-4 w-4" />
            )}
          </Button>
        </div>

        {result && !isEditing && (
          <div className="bg-blue-50 p-3 rounded-lg">
            <p className="text-sm text-blue-800 line-clamp-3">{result}</p>
            <Button
              onClick={() => navigate('/food-research')}
              variant="ghost"
              size="sm"
              className="mt-2 p-0 text-blue-600"
            >
              View Full Results <ArrowRight className="h-3 w-3 ml-1" />
            </Button>
          </div>
        )}

        <div>
          <p className="text-xs font-medium text-gray-600 mb-2">Quick Checks:</p>
          <div className="grid grid-cols-2 gap-2">
            {quickSuggestions.map((suggestion) => (
              <Button
                key={suggestion}
                variant="outline"
                size="sm"
                onClick={() => handleQuickCheck(suggestion)}
                disabled={loading || isEditing}
                className="text-xs capitalize"
              >
                {suggestion}
              </Button>
            ))}
          </div>
        </div>

        {!isEditing && (
          <Button 
            onClick={() => navigate('/food-research')}
            className="w-full"
            size="sm"
          >
            Full Food Research
          </Button>
        )}
      </div>
    </BaseWidget>
  );
};

export default FoodSafetyQuickWidget;