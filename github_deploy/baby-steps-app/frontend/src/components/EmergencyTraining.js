import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  ShieldAlert, 
  Phone, 
  AlertTriangle, 
  Baby, 
  Heart,
  Clock,
  BookOpen
} from 'lucide-react';
import { toast } from 'sonner';

const EmergencyTraining = ({ currentBaby }) => {
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [trainingContent, setTrainingContent] = useState(null);
  const [loading, setLoading] = useState(false);

  const emergencyTopics = [
    {
      id: 'choking',
      title: 'Choking Response',
      description: 'Learn how to help a choking infant',
      icon: <AlertTriangle className="w-8 h-8 text-red-600" />,
      urgency: 'critical',
      ageRestricted: false
    },
    {
      id: 'cpr',
      title: 'Infant CPR',
      description: 'Cardiopulmonary resuscitation for babies',
      icon: <Heart className="w-8 h-8 text-red-600" />,
      urgency: 'critical',
      ageRestricted: false
    },
    {
      id: 'general',
      title: 'General Emergency Response',
      description: 'Basic emergency assessment and response',
      icon: <ShieldAlert className="w-8 h-8 text-red-600" />,
      urgency: 'high',
      ageRestricted: false
    }
  ];

  const handleTopicSelect = async (topic) => {
    setSelectedTopic(topic);
    setLoading(true);

    try {
      const babyAgeMonths = currentBaby ? 
        Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44)) : null;

      const response = await axios.post('/emergency/training', {
        emergency_type: topic.id,
        baby_age_months: babyAgeMonths
      });

      setTrainingContent(response.data);
    } catch (error) {
      toast.error('Failed to load emergency training content');
      setTrainingContent(null);
    } finally {
      setLoading(false);
    }
  };

  const babyAgeMonths = currentBaby ? 
    Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44)) : 0;

  return (
    <div className="max-w-6xl mx-auto space-y-6 fade-in">
      {/* Header with Strong Disclaimer */}
      <div className="space-y-4">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
          <div>
            <h1 className="text-4xl font-bold font-display text-gray-900" data-testid="emergency-training-title">
              Emergency Training
            </h1>
            <p className="text-lg text-gray-600 mt-2">
              {currentBaby ? `Life-saving skills for ${currentBaby.name}` : 'Essential emergency response training'}
            </p>
          </div>
          <Badge variant="destructive" className="text-sm px-4 py-2">
            <Phone className="w-4 h-4 mr-2" />
            Call 911 First
          </Badge>
        </div>

        {/* Critical Disclaimer */}
        <Card className="emergency-card border-2 border-red-300">
          <CardContent className="p-6">
            <div className="flex items-start gap-4">
              <AlertTriangle className="w-8 h-8 text-red-600 flex-shrink-0 mt-1" />
              <div className="space-y-2">
                <h2 className="text-xl font-bold text-red-800">⚠️ CRITICAL DISCLAIMER</h2>
                <div className="text-red-700 space-y-2">
                  <p className="font-semibold">THIS IS EDUCATIONAL CONTENT ONLY - NOT PROFESSIONAL TRAINING</p>
                  <ul className="text-sm space-y-1 list-disc list-inside">
                    <li>This content does NOT replace formal CPR/First Aid certification</li>
                    <li>We STRONGLY recommend taking an AHA-certified course from qualified instructors</li>
                    <li>In ANY emergency: <strong>CALL 911 IMMEDIATELY</strong></li>
                    <li>This app and its creators are not liable for any outcomes from using this information</li>
                    <li>Always prioritize professional medical help over app-based guidance</li>
                  </ul>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Hero Image */}
      <div className="relative h-48 rounded-2xl overflow-hidden">
        <img 
          src="https://images.unsplash.com/flagged/photo-1570560558077-45ad028193e5"
          alt="Parent learning emergency response techniques"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-red-600/80 to-red-800/80 flex items-center justify-center">
          <div className="text-center text-white">
            <ShieldAlert className="w-16 h-16 mx-auto mb-4 opacity-90" />
            <h2 className="text-2xl font-bold mb-2">Emergency Preparedness</h2>
            <p className="text-red-100">Knowledge that can save lives</p>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Training Topics */}
        <div className="lg:col-span-2">
          {!selectedTopic ? (
            <Card className="glass-strong border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <BookOpen className="w-5 h-5 text-red-500" />
                  Select Emergency Training Topic
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4">
                  {emergencyTopics.map((topic) => (
                    <Card 
                      key={topic.id}
                      className="emergency-card cursor-pointer hover:shadow-lg transition-all duration-300"
                      onClick={() => handleTopicSelect(topic)}
                      data-testid={`emergency-topic-${topic.id}`}
                    >
                      <CardContent className="p-6">
                        <div className="flex items-center gap-4">
                          <div className="p-3 bg-red-50 rounded-full">
                            {topic.icon}
                          </div>
                          <div className="flex-1">
                            <h3 className="text-lg font-semibold text-gray-900 mb-1">
                              {topic.title}
                            </h3>
                            <p className="text-gray-600 text-sm mb-2">
                              {topic.description}
                            </p>
                            <Badge 
                              variant={topic.urgency === 'critical' ? 'destructive' : 'secondary'}
                              className="text-xs"
                            >
                              {topic.urgency.toUpperCase()}
                            </Badge>
                          </div>
                          <Button className="btn-emergency">
                            Start Training
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>

                {/* Professional Training Recommendation */}
                <Card className="mt-6 bg-blue-50 border-blue-200">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <BookOpen className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
                      <div>
                        <h3 className="font-semibold text-blue-800 mb-2">
                          Recommended: Take a Professional Course
                        </h3>
                        <p className="text-blue-700 text-sm mb-3">
                          While this training is helpful, hands-on practice with certified instructors is invaluable for emergency preparedness.
                        </p>
                        <div className="text-xs text-blue-600 space-y-1">
                          <p>• American Heart Association (AHA) Infant CPR courses</p>
                          <p>• Red Cross First Aid/CPR training</p>
                          <p>• Local hospital or community center classes</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </CardContent>
            </Card>
          ) : (
            /* Training Content */
            <Card className="emergency-card border-0">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2 text-gray-800">
                    {selectedTopic.icon}
                    {selectedTopic.title}
                    {currentBaby && (
                      <Badge variant="outline" className="ml-2">
                        {babyAgeMonths} months old
                      </Badge>
                    )}
                  </CardTitle>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSelectedTopic(null);
                      setTrainingContent(null);
                    }}
                    data-testid="back-to-topics"
                  >
                    Back to Topics
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <div className="w-8 h-8 border-2 border-red-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading emergency training content...</p>
                  </div>
                ) : trainingContent ? (
                  <EmergencyTrainingContent content={trainingContent} />
                ) : (
                  <div className="text-center py-8">
                    <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                    <p className="text-gray-600">Failed to load training content. In a real emergency, call 911 immediately.</p>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Emergency Numbers */}
          <Card className="emergency-card border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Phone className="w-5 h-5 text-red-500" />
                Emergency Numbers
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-3 bg-red-100 rounded-lg text-center">
                <Phone className="w-6 h-6 text-red-600 mx-auto mb-2" />
                <p className="font-bold text-red-800 text-lg">911</p>
                <p className="text-red-700 text-sm">Fire, Police, Medical</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg text-center">
                <p className="font-semibold text-blue-800">Poison Control</p>
                <p className="text-blue-700">1-800-222-1222</p>
              </div>
              <div className="text-xs text-gray-600 text-center pt-2">
                <p>Keep these numbers easily accessible</p>
              </div>
            </CardContent>
          </Card>

          {/* Quick Emergency Assessment */}
          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Clock className="w-5 h-5 text-orange-500" />
                When to Call 911
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-3 h-3 text-red-500" />
                  <span>Baby is unconscious</span>
                </div>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-3 h-3 text-red-500" />
                  <span>Not breathing or turning blue</span>
                </div>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-3 h-3 text-red-500" />
                  <span>Choking and can't cry/cough</span>
                </div>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-3 h-3 text-red-500" />
                  <span>Severe allergic reaction</span>
                </div>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-3 h-3 text-red-500" />
                  <span>Any doubt about safety</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Age-Specific Notes */}
          {currentBaby && (
            <Card className="glass border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <Baby className="w-5 h-5 text-blue-500" />
                  Age-Specific Notes
                </CardTitle>
              </CardHeader>
              <CardContent>
                <AgeSpecificNotes babyAgeMonths={babyAgeMonths} />
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

// Helper Components
const EmergencyTrainingContent = ({ content }) => (
  <div className="space-y-6">
    {/* Steps */}
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
        <AlertTriangle className="w-5 h-5 text-red-500" />
        Emergency Steps
      </h3>
      {content.steps.map((step, index) => (
        <div key={index} className="emergency-step">
          <div className="flex items-start gap-3">
            <div className="emergency-step-number">
              {index + 1}
            </div>
            <div className="flex-1">
              <p className="text-gray-800">{step}</p>
            </div>
          </div>
        </div>
      ))}
    </div>

    {/* Important Notes */}
    {content.important_notes.length > 0 && (
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-orange-500" />
          Important Notes
        </h3>
        {content.important_notes.map((note, index) => (
          <div key={index} className="p-3 bg-orange-50 border border-orange-200 rounded-lg">
            <p className="text-orange-800 text-sm">{note}</p>
          </div>
        ))}
      </div>
    )}

    {/* When to Call 911 */}
    {content.when_to_call_911.length > 0 && (
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <Phone className="w-5 h-5 text-red-500" />
          When to Call 911
        </h3>
        {content.when_to_call_911.map((situation, index) => (
          <div key={index} className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 text-sm font-medium">{situation}</p>
          </div>
        ))}
      </div>
    )}

    {/* Disclaimer */}
    <div className="disclaimer bg-yellow-50 border-yellow-200">
      <AlertTriangle className="w-5 h-5 text-yellow-600 mb-2" />
      <p className="warning-text text-yellow-800 font-semibold mb-2">DISCLAIMER</p>
      <p className="text-xs text-yellow-700">{content.disclaimer}</p>
    </div>
  </div>
);

const AgeSpecificNotes = ({ babyAgeMonths }) => {
  let notes;

  if (babyAgeMonths < 6) {
    notes = [
      "Infant CPR uses 2 fingers, not full hand",
      "Very small airway - gentle technique required",
      "Check for breathing by looking at chest movement",
      "Never leave unattended during feeding"
    ];
  } else if (babyAgeMonths < 12) {
    notes = [
      "Choking risk increases with solid foods",
      "Still use infant CPR technique",
      "Watch for small objects in reach",
      "Food pieces should be appropriate size"
    ];
  } else {
    notes = [
      "Transitioning to child CPR technique",
      "More mobile - watch for climbing hazards",
      "Can eat more varied foods safely",
      "Beginning to understand simple safety words"
    ];
  }

  return (
    <div className="space-y-2">
      {notes.map((note, index) => (
        <div key={index} className="flex items-start gap-2 text-sm">
          <Baby className="w-3 h-3 text-blue-500 flex-shrink-0 mt-1" />
          <span className="text-gray-700">{note}</span>
        </div>
      ))}
    </div>
  );
};

export default EmergencyTraining;