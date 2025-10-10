import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { 
  ChefHat, 
  Plus, 
  Clock, 
  Baby,
  Search,
  Utensils,
  BookOpen
} from 'lucide-react';
import { toast } from 'sonner';
import PageAd from './ads/PageAd';
import { shouldUseOfflineMode, offlineAPI } from '../offlineMode';

const MealPlanner = ({ currentBaby }) => {
  const [mealPlans, setMealPlans] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    meal_name: '',
    ingredients: [''],
    instructions: [''],
    nutrition_notes: ''
  });

  // Meal planning suggestions - focused only on meal ideas and recipes
  const commonSuggestions = [
    // Breakfast Ideas
    'Healthy breakfast ideas for babies',
    'Easy morning meals for 8 month old',
    'Quick breakfast recipes for toddlers',
    
    // Lunch & Dinner Ideas  
    'Nutritious lunch ideas for 10 month old',
    'Easy dinner recipes for babies',
    'Family meal ideas baby can share',
    
    // Snacks & Special Occasions
    'Healthy snack ideas for toddlers',
    'Finger foods for baby led weaning',
    'First birthday party food ideas'
  ];

  useEffect(() => {
    if (currentBaby) {
      fetchMealPlans();
    }
  }, [currentBaby]);

  const fetchMealPlans = async () => {
    try {
      const response = await axios.get('/meals', {
        params: { baby_id: currentBaby.id }
      });
      setMealPlans(response.data);
    } catch (error) {
      console.error('Failed to fetch meal plans:', error);
    }
  };

  const handleSearch = async (query = searchQuery) => {
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    try {
      const babyAgeMonths = currentBaby ? 
        Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44)) : 12;

      // Always use standalone mode with AI integration
      console.log('🍽️ Using standalone mode with AI for meal planning');
      const response = await offlineAPI.mealSearch(query, babyAgeMonths);
      
      if (response.data && response.data.results) {
        setSearchResults(response.data.results);
        setError('');
        toast.success('Meal ideas found');
      } else {
        setError('No results found. Please try a different search.');
      }
      setSearchQuery('');
    } catch (error) {
      console.error('Meal search error:', error);
      setError(`Search failed: ${error.message || 'Unable to search for meals'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleSearch(suggestion);
  };

  const handleAddIngredient = () => {
    setFormData({
      ...formData,
      ingredients: [...formData.ingredients, '']
    });
  };

  const handleAddInstruction = () => {
    setFormData({
      ...formData,
      instructions: [...formData.instructions, '']
    });
  };

  const handleIngredientChange = (index, value) => {
    const newIngredients = [...formData.ingredients];
    newIngredients[index] = value;
    setFormData({ ...formData, ingredients: newIngredients });
  };

  const handleInstructionChange = (index, value) => {
    const newInstructions = [...formData.instructions];
    newInstructions[index] = value;
    setFormData({ ...formData, instructions: newInstructions });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const babyAgeMonths = Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44));
      
      const mealData = {
        baby_id: currentBaby.id,
        age_months: babyAgeMonths,
        ...formData,
        ingredients: formData.ingredients.filter(ing => ing.trim()),
        instructions: formData.instructions.filter(inst => inst.trim())
      };

      await axios.post('/meals', mealData);
      toast.success('Meal plan saved successfully!');
      
      setShowAddForm(false);
      setFormData({
        meal_name: '',
        ingredients: [''],
        instructions: [''],
        nutrition_notes: ''
      });
      
      fetchMealPlans();
    } catch (error) {
      toast.error('Failed to save meal plan');
    }
  };

  if (!currentBaby) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="glass-strong border-0 max-w-md mx-auto text-center">
          <CardContent className="p-8">
            <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
              <Baby className="w-8 h-8 text-gray-400" />
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">No Baby Profile</h2>
            <p className="text-gray-600 mb-4">Please add a baby profile to get personalized meal planning.</p>
            <Button
              onClick={() => window.location.href = '/baby-profile'}
              className="bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white"
            >
              Add Baby Profile
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const babyAgeMonths = Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44));

  return (
    <div className="max-w-6xl mx-auto space-y-6 fade-in">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold font-display text-gray-900" data-testid="meal-planner-title">
            Meal Planner
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Search meal ideas and food safety info for <span className="font-semibold text-orange-600">{currentBaby.name}</span> ({babyAgeMonths} months)
          </p>
        </div>
        <Button
          onClick={() => setShowAddForm(true)}
          className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-2 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
          data-testid="add-meal-btn"
        >
          <Plus className="w-5 h-5 mr-2" />
          Save Custom Meal
        </Button>
      </div>

      {/* Hero Image */}
      <div className="relative h-48 rounded-2xl overflow-hidden">
        <img 
          src="https://images.unsplash.com/photo-1582568469591-329655b4c24c"
          alt="Baby enjoying healthy, age-appropriate foods"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-orange-600/80 to-amber-600/80 flex items-center justify-center">
          <div className="text-center text-white">
            <Search className="w-12 h-12 mx-auto mb-3 opacity-90" />
            <h2 className="text-2xl font-bold mb-2">Smart Food & Meal Search</h2>
            <p className="text-orange-100">Ask about any food or get meal ideas instantly</p>
          </div>
        </div>
      </div>

      {/* Age Alert */}
      <AgeAppropriateAlert babyAgeMonths={babyAgeMonths} />

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main Search Interface */}
        <div className="lg:col-span-2 space-y-6">
          {/* Search Bar */}
          <Card className="glass-strong border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Search className="w-5 h-5 text-orange-500" />
                Search Meals & Food Safety
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Search Form */}
              <div className="flex gap-3">
                <Input
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Ask about food safety or search for meal ideas... (e.g., 'Is honey safe?' or 'breakfast ideas')"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all duration-200"
                  data-testid="meal-search-input"
                />
                <Button
                  onClick={() => handleSearch()}
                  disabled={loading || !searchQuery.trim()}
                  className="bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white px-6 py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
                  data-testid="search-submit-btn"
                >
                  {loading ? (
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    <Search className="w-5 h-5" />
                  )}
                </Button>
              </div>
              <p className="text-xs text-gray-500 mt-2 flex items-center">
                <Clock className="w-3 h-3 mr-1" />
                Response may take up to a minute due to AI processing and customizing for {currentBaby?.name || 'your baby'}
              </p>

              {/* Common Suggestions */}
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-gray-700">Popular searches:</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {commonSuggestions.slice(0, 8).map((suggestion, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      onClick={() => handleSuggestionClick(suggestion)}
                      disabled={loading}
                      className="text-left justify-start p-3 h-auto border-gray-200 hover:border-orange-300 hover:bg-orange-50 transition-all duration-200 text-xs"
                      data-testid={`suggestion-${index}`}
                    >
                      {suggestion}
                    </Button>
                  ))}
                </div>
                <Button
                  variant="ghost"
                  onClick={() => {
                    const moreButton = document.getElementById('more-suggestions');
                    moreButton.style.display = moreButton.style.display === 'none' ? 'block' : 'none';
                  }}
                  className="text-orange-600 text-sm"
                >
                  Show more suggestions →
                </Button>
                <div id="more-suggestions" style={{display: 'none'}} className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {commonSuggestions.slice(8).map((suggestion, index) => (
                    <Button
                      key={index + 8}
                      variant="outline"
                      onClick={() => handleSuggestionClick(suggestion)}
                      disabled={loading}
                      className="text-left justify-start p-3 h-auto border-gray-200 hover:border-orange-300 hover:bg-orange-50 transition-all duration-200 text-xs"
                      data-testid={`suggestion-${index + 8}`}
                    >
                      {suggestion}
                    </Button>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Search Results */}
          {searchResults && (
            <Card className="glass-strong border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <BookOpen className="w-5 h-5 text-green-500" />
                  Results for "{searchResults.query}"
                  {searchResults.age_months && (
                    <span className="text-sm bg-orange-100 text-orange-800 px-2 py-1 rounded-full">
                      {searchResults.age_months} months
                    </span>
                  )}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="prose prose-sm max-w-none">
                  <div className="whitespace-pre-wrap text-gray-800">{searchResults.results}</div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Error Display */}
          {error && (
            <Card className="glass-strong border-0 border-l-4 border-l-red-500">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="w-5 h-5 text-red-500">⚠️</div>
                  <p className="text-red-700 font-medium">{error}</p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Add Custom Meal Form */}
          {showAddForm && (
            <Card className="glass-strong border-0">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-gray-800">
                    <Plus className="w-5 h-5 text-green-500" />
                    Save Custom Meal Plan
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => setShowAddForm(false)}
                    data-testid="cancel-add-meal"
                  >
                    Cancel
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="meal-name" className="text-sm font-medium text-gray-700">
                          Meal Name *
                        </Label>
                        <Input
                          id="meal-name"
                          value={formData.meal_name}
                          onChange={(e) => setFormData({...formData, meal_name: e.target.value})}
                          placeholder="e.g., Sweet Potato Puree"
                          required
                          data-testid="meal-name-input"
                        />
                      </div>
                    </div>

                    <div className="space-y-4">
                      <div className="space-y-2">
                        <Label className="text-sm font-medium text-gray-700">Ingredients *</Label>
                        {formData.ingredients.map((ingredient, index) => (
                          <Input
                            key={index}
                            value={ingredient}
                            onChange={(e) => handleIngredientChange(index, e.target.value)}
                            placeholder={`Ingredient ${index + 1}`}
                            data-testid={`ingredient-${index}`}
                          />
                        ))}
                        <Button
                          type="button"
                          variant="outline"
                          onClick={handleAddIngredient}
                          className="w-full"
                          data-testid="add-ingredient-btn"
                        >
                          <Plus className="w-4 h-4 mr-2" />
                          Add Ingredient
                        </Button>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-sm font-medium text-gray-700">Instructions *</Label>
                    {formData.instructions.map((instruction, index) => (
                      <Textarea
                        key={index}
                        value={instruction}
                        onChange={(e) => handleInstructionChange(index, e.target.value)}
                        placeholder={`Step ${index + 1}`}
                        data-testid={`instruction-${index}`}
                      />
                    ))}
                    <Button
                      type="button"
                      variant="outline"
                      onClick={handleAddInstruction}
                      className="w-full"
                      data-testid="add-instruction-btn"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      Add Instruction
                    </Button>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="nutrition-notes" className="text-sm font-medium text-gray-700">
                      Nutrition Notes (optional)
                    </Label>
                    <Textarea
                      id="nutrition-notes"
                      value={formData.nutrition_notes}
                      onChange={(e) => setFormData({...formData, nutrition_notes: e.target.value})}
                      placeholder="Any nutritional benefits or considerations..."
                      data-testid="nutrition-notes-input"
                    />
                  </div>

                  <Button
                    type="submit"
                    className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                    data-testid="save-meal-plan-btn"
                  >
                    <ChefHat className="w-5 h-5 mr-2" />
                    Save Meal Plan
                  </Button>
                </form>
              </CardContent>
            </Card>
          )}

          {/* Saved Meal Plans */}
          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Clock className="w-5 h-5 text-green-500" />
                Your Saved Meals
              </CardTitle>
            </CardHeader>
            <CardContent>
              {mealPlans.length > 0 ? (
                <div className="space-y-4">
                  {mealPlans.map((meal) => (
                    <MealPlanCard key={meal.id} meal={meal} />
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <ChefHat className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">No saved meals yet. Use the search above to find meal ideas, then save your favorites!</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Feeding Guidelines */}
          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Utensils className="w-5 h-5 text-blue-500" />
                Feeding Guidelines
              </CardTitle>
            </CardHeader>
            <CardContent>
              <FeedingGuidelines babyAgeMonths={babyAgeMonths} />
            </CardContent>
          </Card>

          {/* Safety Reminders */}
          <Card className="emergency-card border-0">
            <CardHeader>
              <CardTitle className="text-gray-800 text-sm">
                ⚠️ Meal Safety Reminders
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-xs">
              <p>• Always supervise during meals</p>
              <p>• Check food temperature before serving</p>
              <p>• Cut foods to appropriate sizes</p>
              <p>• Introduce one new food at a time</p>
              <p>• Watch for allergic reactions</p>
              <p>• Never force feeding</p>
            </CardContent>
          </Card>

          {/* Search Tips */}
          <Card className="glass border-0 bg-gradient-to-br from-blue-50 to-purple-50">
            <CardContent className="p-4">
              <Search className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <p className="text-sm text-gray-700 font-medium mb-1 text-center">Search Tips</p>
              <div className="text-xs text-gray-600 space-y-1">
                <p>• Ask "Is [food] safe for my baby?"</p>
                <p>• Search "[age] month meal ideas"</p>
                <p>• Try "finger foods for teething"</p>
                <p>• Ask "how to prepare [food]"</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Page Ad */}
      <PageAd position="bottom" />
    </div>
  );
};

// Helper Components
const AgeAppropriateAlert = ({ babyAgeMonths }) => {
  let alert;

  if (babyAgeMonths < 6) {
    alert = {
      message: "Your baby isn't ready for solid foods yet. Continue with breast milk or formula only.",
      type: "caution",
      icon: <Baby className="w-5 h-5" />
    };
  } else if (babyAgeMonths < 8) {
    alert = {
      message: "Perfect time for purees and very soft finger foods. Start with single ingredients.",
      type: "safe",
      icon: <ChefHat className="w-5 h-5" />
    };
  } else if (babyAgeMonths < 12) {
    alert = {
      message: "Ready for more textures! Small, soft finger foods and mashed family meals work well.",
      type: "safe",
      icon: <Utensils className="w-5 h-5" />
    };
  } else {
    alert = {
      message: "Transitioning to family foods! Most foods are safe with appropriate modifications.",
      type: "safe",
      icon: <BookOpen className="w-5 h-5" />
    };
  }

  return (
    <Card className={`border-0 food-${alert.type}`}>
      <CardContent className="p-4">
        <div className="flex items-center gap-3">
          {alert.icon}
          <p className="text-gray-800 font-medium">{alert.message}</p>
        </div>
      </CardContent>
    </Card>
  );
};

const MealPlanCard = ({ meal }) => (
  <Card className="meal-card">
    <CardContent className="p-4">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="font-semibold text-gray-900">{meal.meal_name}</h3>
          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
            {meal.age_months} months
          </span>
        </div>
      </div>
      
      <div className="space-y-3 text-sm">
        <div>
          <p className="font-medium text-gray-800 mb-1">Ingredients:</p>
          <ul className="text-gray-600 list-disc list-inside">
            {meal.ingredients.map((ingredient, index) => (
              <li key={index}>{ingredient}</li>
            ))}
          </ul>
        </div>
        
        <div>
          <p className="font-medium text-gray-800 mb-1">Instructions:</p>
          <ol className="text-gray-600 list-decimal list-inside space-y-1">
            {meal.instructions.map((instruction, index) => (
              <li key={index}>{instruction}</li>
            ))}
          </ol>
        </div>
        
        {meal.nutrition_notes && (
          <div>
            <p className="font-medium text-gray-800 mb-1">Nutrition Notes:</p>
            <p className="text-gray-600">{meal.nutrition_notes}</p>
          </div>
        )}
      </div>
    </CardContent>
  </Card>
);

const FeedingGuidelines = ({ babyAgeMonths }) => {
  let guidelines;

  if (babyAgeMonths < 6) {
    guidelines = [
      "Breast milk or formula only",
      "No solid foods yet",
      "6+ feedings per day",
      "Watch for readiness cues"
    ];
  } else if (babyAgeMonths < 8) {
    guidelines = [
      "Start with iron-rich purees",
      "One new food every 3-5 days",
      "Smooth, thin consistency",
      "Continue milk feeds"
    ];
  } else if (babyAgeMonths < 12) {
    guidelines = [
      "Thicker textures and lumps",
      "Soft finger foods",
      "Self-feeding encouraged",
      "Family meal adaptations"
    ];
  } else {
    guidelines = [
      "Most family foods appropriate",
      "Cut foods appropriately",
      "Whole milk introduction",
      "3 meals + 2 snacks"
    ];
  }

  return (
    <div className="space-y-2">
      {guidelines.map((guideline, index) => (
        <div key={index} className="flex items-center gap-2 text-sm">
          <ChefHat className="w-3 h-3 text-orange-500 flex-shrink-0" />
          <span className="text-gray-700">{guideline}</span>
        </div>
      ))}
    </div>
  );
};

export default MealPlanner;