import React, { useState } from 'react';
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
  BookOpen,
  ChevronLeft,
  ChevronRight,
  RotateCcw,
  Hand,
  Users
} from 'lucide-react';

const EmergencyTraining = ({ currentBaby }) => {
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);

  const emergencyTopics = [
    {
      id: 'choking',
      title: 'Choking Response',
      description: 'Learn how to help a choking infant or toddler',
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
      id: 'assessment',
      title: 'Emergency Assessment',
      description: 'How to assess and respond to emergencies',
      icon: <ShieldAlert className="w-8 h-8 text-red-600" />,
      urgency: 'high',
      ageRestricted: false
    }
  ];

  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic);
    setCurrentSlide(0);
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
            /* Training Slideshow */
            <EmergencySlideshow 
              topic={selectedTopic}
              currentSlide={currentSlide}
              setCurrentSlide={setCurrentSlide}
              babyAgeMonths={babyAgeMonths}
              onBack={() => setSelectedTopic(null)}
            />
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

// Emergency Training Slideshows
const EmergencySlideshow = ({ topic, currentSlide, setCurrentSlide, babyAgeMonths, onBack }) => {
  const slides = getTrainingSlides(topic.id, babyAgeMonths);
  const totalSlides = slides.length;

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % totalSlides);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + totalSlides) % totalSlides);
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  return (
    <Card className="emergency-card border-0">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-gray-800">
            {topic.icon}
            {topic.title}
            <Badge variant="outline" className="ml-2">
              {currentSlide + 1} of {totalSlides}
            </Badge>
          </CardTitle>
          <Button variant="outline" onClick={onBack} data-testid="back-to-topics">
            Back to Topics
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {/* Slide Content */}
        <div className="min-h-[400px] mb-6">
          <SlideContent slide={slides[currentSlide]} />
        </div>

        {/* Navigation Controls */}
        <div className="flex items-center justify-between border-t border-gray-200 pt-4">
          <Button
            variant="outline"
            onClick={prevSlide}
            disabled={currentSlide === 0}
            className="flex items-center gap-2"
          >
            <ChevronLeft className="w-4 h-4" />
            Previous
          </Button>

          {/* Slide Indicators */}
          <div className="flex space-x-2">
            {slides.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`w-3 h-3 rounded-full transition-colors ${
                  index === currentSlide 
                    ? 'bg-red-500' 
                    : 'bg-gray-300 hover:bg-gray-400'
                }`}
              />
            ))}
          </div>

          <Button
            variant="outline"
            onClick={nextSlide}
            disabled={currentSlide === totalSlides - 1}
            className="flex items-center gap-2"
          >
            Next
            <ChevronRight className="w-4 h-4" />
          </Button>
        </div>

        {/* Restart Button */}
        {currentSlide === totalSlides - 1 && (
          <div className="text-center mt-4">
            <Button
              onClick={() => setCurrentSlide(0)}
              className="bg-red-600 hover:bg-red-700 text-white flex items-center gap-2 mx-auto"
            >
              <RotateCcw className="w-4 h-4" />
              Restart Training
            </Button>
          </div>
        )}

        {/* Small Disclaimer */}
        <div className="mt-6 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-xs text-yellow-800 text-center">
            Educational content only. Take official AHA courses for certification. Call 911 in emergencies.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

// Slide Content Component
const SlideContent = ({ slide }) => (
  <div className="space-y-4">
    <div className="text-center">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">{slide.title}</h2>
      {slide.subtitle && (
        <p className="text-lg text-gray-600">{slide.subtitle}</p>
      )}
    </div>

    {/* Visual Diagram */}
    {slide.diagram && (
      <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
        <div className="text-6xl mb-4">{slide.diagram.emoji}</div>
        <div className="max-w-md mx-auto">
          <DiagramComponent type={slide.diagram.type} details={slide.diagram.details} />
        </div>
      </div>
    )}

    {/* Instructions */}
    {slide.instructions && (
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <div className="space-y-2">
          {slide.instructions.map((instruction, index) => (
            <div key={index} className="flex items-start gap-3">
              <div className="w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 mt-0.5">
                {index + 1}
              </div>
              <p className="text-gray-800">{instruction}</p>
            </div>
          ))}
        </div>
      </div>
    )}

    {/* Important Notes */}
    {slide.notes && (
      <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
        <div className="flex items-start gap-2">
          <AlertTriangle className="w-5 h-5 text-orange-600 flex-shrink-0 mt-0.5" />
          <div className="space-y-2">
            <p className="font-semibold text-orange-800">Important:</p>
            {slide.notes.map((note, index) => (
              <p key={index} className="text-orange-700 text-sm">• {note}</p>
            ))}
          </div>
        </div>
      </div>
    )}

    {/* Emergency Alert */}
    {slide.emergency && (
      <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
        <div className="flex items-start gap-2">
          <Phone className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-bold text-red-800 mb-1">CALL 911 IF:</p>
            {slide.emergency.map((situation, index) => (
              <p key={index} className="text-red-700 text-sm">• {situation}</p>
            ))}
          </div>
        </div>
      </div>
    )}
  </div>
);

// Diagram Component for Visual Instructions
const DiagramComponent = ({ type, details }) => {
  switch (type) {
    case 'hand_position':
      return (
        <div className="space-y-2">
          <div className="border-2 border-gray-400 rounded-lg p-4 bg-white">
            <Hand className="w-12 h-12 mx-auto text-gray-600 mb-2" />
            <p className="text-sm text-gray-700 text-center">{details.position}</p>
            <p className="text-xs text-gray-500 text-center mt-1">{details.pressure}</p>
          </div>
        </div>
      );
    
    case 'body_position':
      return (
        <div className="space-y-2">
          <div className="border-2 border-gray-400 rounded-lg p-4 bg-white">
            <Users className="w-12 h-12 mx-auto text-gray-600 mb-2" />
            <p className="text-sm text-gray-700 text-center">{details.position}</p>
            <p className="text-xs text-gray-500 text-center mt-1">{details.support}</p>
          </div>
        </div>
      );
      
    case 'technique':
      return (
        <div className="grid grid-cols-2 gap-2">
          {details.steps.map((step, index) => (
            <div key={index} className="border border-gray-300 rounded p-2 bg-white text-center">
              <div className="text-2xl mb-1">{step.icon}</div>
              <p className="text-xs text-gray-700">{step.text}</p>
            </div>
          ))}
        </div>
      );
      
    default:
      return (
        <div className="text-center p-4 border border-gray-300 rounded bg-white">
          <p className="text-sm text-gray-600">{details.description}</p>
        </div>
      );
  }
};

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