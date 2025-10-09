import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { 
  Search, 
  CheckCircle, 
  AlertTriangle, 
  X, 
  Stethoscope,
  Clock,
  Baby
} from 'lucide-react';
import { toast } from 'sonner';
import PageAd from './ads/PageAd';
import { shouldUseOfflineMode, offlineAPI } from '../offlineMode';

const FoodResearch = ({ currentBaby }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [safetyHistory, setSafetyHistory] = useState([]);
  const [quickChecks] = useState([
    'Can my baby have honey?',
    'Is avocado safe for babies?',
    'When can babies have eggs?',
    'Are strawberries safe for infants?',
    'Can babies drink water?',
    'Is peanut butter safe for babies?'
  ]);

  useEffect(() => {
    if (currentBaby) {
      fetchSafetyHistory();
    }
  }, [currentBaby]);

  const fetchSafetyHistory = async () => {
    try {
      const response = await axios.get('/food/safety-history', {
        params: { baby_id: currentBaby?.id }
      });
      setSafetyHistory(response.data.slice(0, 5)); // Show last 5 checks
    } catch (error) {
      console.error('Failed to fetch safety history:', error);
    }
  };

  const handleSearch = async (searchQuery = query) => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const babyAgeMonths = currentBaby ? 
        Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44)) : 6;

      // Always use standalone/offline mode for better reliability
      console.log('🔬 Using standalone mode with AI integration for food research');
      const response = await offlineAPI.foodResearch(searchQuery, babyAgeMonths);
      setResults(response.data);
      setQuery('');
      toast.success('Food research completed');
      
      // Refresh safety history
      if (currentBaby) {
        fetchSafetyHistory();
      }
    } catch (error) {
      console.error('Food research failed:', error);
      toast.error('Failed to get food safety information');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickCheck = async (foodItem) => {
    if (!currentBaby) {
      toast.error('Please add a baby profile first');
      return;
    }

    try {
      const babyAgeMonths = Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44));
      
      const response = await axios.post('/food/safety-check', {
        baby_id: currentBaby.id,
        food_item: foodItem,
        age_months: babyAgeMonths
      });

      toast.success(`Safety check completed for ${foodItem}`);
      fetchSafetyHistory();
    } catch (error) {
      toast.error('Failed to perform safety check');
    }
  };

  const getSafetyIcon = (level) => {
    switch (level) {
      case 'safe':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'caution':
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
      case 'avoid':
        return <X className="w-5 h-5 text-red-600" />;
      case 'consult_doctor':
        return <Stethoscope className="w-5 h-5 text-blue-600" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-gray-600" />;
    }
  };

  const getSafetyColor = (level) => {
    switch (level) {
      case 'safe': return 'safety-safe';
      case 'caution': return 'safety-caution';
      case 'avoid': return 'safety-avoid';
      case 'consult_doctor': return 'safety-consult';
      default: return 'bg-gray-500';
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
            <p className="text-gray-600 mb-4">Please add a baby profile to get personalized food safety guidance.</p>
            <Button
              onClick={() => window.location.href = '/baby-profile'}
              className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white"
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
          <h1 className="text-4xl font-bold font-display text-gray-900" data-testid="food-research-title">
            Food Safety Research
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            Get evidence-based guidance for feeding <span className="font-semibold text-green-600">{currentBaby.name}</span> ({babyAgeMonths} months)
          </p>
        </div>
      </div>

      {/* Hero Image */}
      <div className="relative h-48 rounded-2xl overflow-hidden mb-6">
        <img 
          src="https://images.unsplash.com/photo-1557939663-0619f304af9c"
          alt="Baby safely eating age-appropriate foods"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-green-600/80 to-emerald-600/80 flex items-center justify-center">
          <div className="text-center text-white">
            <Search className="w-12 h-12 mx-auto mb-3 opacity-90" />
            <h2 className="text-2xl font-bold mb-2">Safe Food Research</h2>
            <p className="text-green-100">Evidence-based nutrition guidance</p>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Search Interface */}
        <div className="lg:col-span-2">
          <Card className="glass-strong border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Search className="w-5 h-5 text-green-500" />
                Food Safety Research
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Search Form */}
              <div className="flex gap-3">
                <Input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask about any food or drink... (e.g., 'Can my baby have honey?')"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 transition-all duration-200"
                  data-testid="food-research-input"
                />
                <Button
                  onClick={() => handleSearch()}
                  disabled={loading || !query.trim()}
                  className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white px-6 py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
                  data-testid="research-submit-btn"
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

              {/* Quick Check Buttons */}
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-gray-700">Quick Safety Checks:</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {quickChecks.map((check, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      onClick={() => handleSearch(check)}
                      className="text-left justify-start p-3 h-auto border-gray-200 hover:border-green-300 hover:bg-green-50 transition-all duration-200"
                      data-testid={`quick-check-${index}`}
                    >
                      <div className="text-sm">{check}</div>
                    </Button>
                  ))}
                </div>
              </div>

              {/* Results */}
              {results && (
                <div className="space-y-4">
                  <div className={`p-4 rounded-lg border-2 food-${results.safety_level}`}>
                    <div className="flex items-center gap-3 mb-3">
                      {getSafetyIcon(results.safety_level)}
                      <div>
                        <Badge className={`${getSafetyColor(results.safety_level)} text-white`}>
                          {results.safety_level.replace('_', ' ').toUpperCase()}
                        </Badge>
                        {results.age_recommendation && (
                          <Badge variant="outline" className="ml-2">
                            {results.age_recommendation}
                          </Badge>
                        )}
                      </div>
                    </div>
                    <div className="prose prose-sm max-w-none">
                      <p className="text-gray-800 whitespace-pre-wrap">{results.answer}</p>
                    </div>
                    {results.sources && results.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <p className="text-xs text-gray-500">
                          Sources: {results.sources.join(', ')}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Disclaimer for this result */}
                  <div className="disclaimer">
                    <p className="text-xs text-gray-600">
                      <span className="warning-text">⚠️ Important:</span> This information is for educational purposes only. 
                      Always consult your pediatrician before introducing new foods, especially if your baby has allergies or medical conditions.
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Recent Checks */}
          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Clock className="w-5 h-5 text-orange-500" />
                Recent Checks
              </CardTitle>
            </CardHeader>
            <CardContent>
              {safetyHistory.length > 0 ? (
                <div className="space-y-3">
                  {safetyHistory.map((check) => (
                    <div key={check.id} className={`p-3 rounded-lg food-${check.is_safe ? 'safe' : 'avoid'}`}>
                      <div className="flex items-center gap-2 mb-1">
                        {check.is_safe ? (
                          <CheckCircle className="w-4 h-4 text-green-600" />
                        ) : (
                          <X className="w-4 h-4 text-red-600" />
                        )}
                        <span className="font-medium text-sm">{check.food_item}</span>
                      </div>
                      <p className="text-xs text-gray-600">
                        Age: {check.age_months} months
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-4">
                  No recent food safety checks
                </p>
              )}
            </CardContent>
          </Card>

          {/* Age-Appropriate Guidelines */}
          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Baby className="w-5 h-5 text-blue-500" />
                Age Guidelines
              </CardTitle>
            </CardHeader>
            <CardContent>
              <AgeGuidelinesWidget babyAgeMonths={babyAgeMonths} />
            </CardContent>
          </Card>

          {/* Emergency Notice */}
          <Card className="emergency-card border-0">
            <CardContent className="p-4">
              <div className="text-center">
                <AlertTriangle className="w-8 h-8 text-red-600 mx-auto mb-2" />
                <p className="text-sm font-medium text-red-800 mb-2">Food Emergency?</p>
                <p className="text-xs text-red-700 mb-3">
                  If your baby is choking, having an allergic reaction, or in distress after eating
                </p>
                <Button
                  onClick={() => window.location.href = '/emergency-training'}
                  className="btn-emergency text-sm py-2 px-4"
                  data-testid="emergency-training-link"
                >
                  Emergency Training
                </Button>
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
const AgeGuidelinesWidget = ({ babyAgeMonths }) => {
  let guidelines;

  if (babyAgeMonths < 4) {
    guidelines = [
      { text: "Breast milk or formula only", safe: true },
      { text: "No solid foods", safe: false },
      { text: "No water needed", safe: false },
      { text: "No juice or other liquids", safe: false }
    ];
  } else if (babyAgeMonths < 6) {
    guidelines = [
      { text: "Continue breast milk/formula", safe: true },
      { text: "Prepare for solids introduction", safe: true },
      { text: "Still no solid foods", safe: false },
      { text: "Watch for readiness signs", safe: true }
    ];
  } else if (babyAgeMonths < 12) {
    guidelines = [
      { text: "Iron-rich first foods", safe: true },
      { text: "Single-ingredient purees", safe: true },
      { text: "Avoid honey", safe: false },
      { text: "Watch for allergies", safe: true }
    ];
  } else {
    guidelines = [
      { text: "Most family foods OK", safe: true },
      { text: "Avoid choking hazards", safe: false },
      { text: "Whole milk introduction", safe: true },
      { text: "Self-feeding encouraged", safe: true }
    ];
  }

  return (
    <div className="space-y-2">
      {guidelines.map((guideline, index) => (
        <div key={index} className="flex items-center gap-2 text-sm">
          {guideline.safe ? (
            <CheckCircle className="w-3 h-3 text-green-500 flex-shrink-0" />
          ) : (
            <X className="w-3 h-3 text-red-500 flex-shrink-0" />
          )}
          <span className={guideline.safe ? 'text-gray-700' : 'text-gray-600'}>
            {guideline.text}
          </span>
        </div>
      ))}
    </div>
  );
};

export default FoodResearch;