import React, { useState, useEffect } from 'react';
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
import PageAd from './ads/PageAd';

const EmergencyTraining = ({ currentBaby }) => {
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, []);

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
            <h1 className="text-4xl font-bold font-display text-gray-900 dark:text-white" data-testid="emergency-training-title">
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

        {/* Disclaimer */}
        <Card className="bg-yellow-50 border border-yellow-200">
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-yellow-600 flex-shrink-0" />
              <p className="text-sm text-yellow-800">
                <strong>Educational content only.</strong> Take official AHA courses for certification. Always call 911 in emergencies.
              </p>
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
                <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
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

                {/* Normal Health Parameters */}
                <Card className="mt-6 bg-green-50 border-green-200">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <Heart className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" />
                      <div className="w-full">
                        <h3 className="font-semibold text-green-800 mb-3">
                          Normal Health Parameters by Age
                        </h3>
                        <p className="text-green-700 text-sm mb-4">
                          Reference ranges for healthy babies. Always consult your pediatrician if concerned.
                        </p>
                        
                        <div className="space-y-4">
                          {/* 0-3 months */}
                          <div className="bg-white border border-green-200 rounded-lg p-3">
                            <p className="font-semibold text-green-800 text-sm mb-2">0-3 Months</p>
                            <div className="grid grid-cols-2 gap-2 text-xs text-green-700">
                              <div>
                                <span className="font-medium">Heart Rate:</span> 100-150 bpm
                              </div>
                              <div>
                                <span className="font-medium">Temp:</span> 97.7-100.3°F (36.5-38°C)
                              </div>
                              <div>
                                <span className="font-medium">Respiratory:</span> 30-60 breaths/min
                              </div>
                              <div>
                                <span className="font-medium">O2 Sat:</span> 95-100%
                              </div>
                            </div>
                          </div>

                          {/* 4-6 months */}
                          <div className="bg-white border border-green-200 rounded-lg p-3">
                            <p className="font-semibold text-green-800 text-sm mb-2">4-6 Months</p>
                            <div className="grid grid-cols-2 gap-2 text-xs text-green-700">
                              <div>
                                <span className="font-medium">Heart Rate:</span> 90-140 bpm
                              </div>
                              <div>
                                <span className="font-medium">Temp:</span> 97.7-100.3°F (36.5-38°C)
                              </div>
                              <div>
                                <span className="font-medium">Respiratory:</span> 25-45 breaths/min
                              </div>
                              <div>
                                <span className="font-medium">O2 Sat:</span> 95-100%
                              </div>
                            </div>
                          </div>

                          {/* 7-12 months */}
                          <div className="bg-white border border-green-200 rounded-lg p-3">
                            <p className="font-semibold text-green-800 text-sm mb-2">7-12 Months</p>
                            <div className="grid grid-cols-2 gap-2 text-xs text-green-700">
                              <div>
                                <span className="font-medium">Heart Rate:</span> 80-130 bpm
                              </div>
                              <div>
                                <span className="font-medium">Temp:</span> 97.7-100.3°F (36.5-38°C)
                              </div>
                              <div>
                                <span className="font-medium">Respiratory:</span> 20-40 breaths/min
                              </div>
                              <div>
                                <span className="font-medium">O2 Sat:</span> 95-100%
                              </div>
                            </div>
                          </div>

                          {/* 13-18 months */}
                          <div className="bg-white border border-green-200 rounded-lg p-3">
                            <p className="font-semibold text-green-800 text-sm mb-2">13-18 Months</p>
                            <div className="grid grid-cols-2 gap-2 text-xs text-green-700">
                              <div>
                                <span className="font-medium">Heart Rate:</span> 75-120 bpm
                              </div>
                              <div>
                                <span className="font-medium">Temp:</span> 97.7-100.3°F (36.5-38°C)
                              </div>
                              <div>
                                <span className="font-medium">Respiratory:</span> 20-35 breaths/min
                              </div>
                              <div>
                                <span className="font-medium">O2 Sat:</span> 95-100%
                              </div>
                            </div>
                          </div>

                          {/* 19-24 months */}
                          <div className="bg-white border border-green-200 rounded-lg p-3">
                            <p className="font-semibold text-green-800 text-sm mb-2">19-24 Months</p>
                            <div className="grid grid-cols-2 gap-2 text-xs text-green-700">
                              <div>
                                <span className="font-medium">Heart Rate:</span> 70-110 bpm
                              </div>
                              <div>
                                <span className="font-medium">Temp:</span> 97.7-100.3°F (36.5-38°C)
                              </div>
                              <div>
                                <span className="font-medium">Respiratory:</span> 20-30 breaths/min
                              </div>
                              <div>
                                <span className="font-medium">O2 Sat:</span> 95-100%
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
                          <AlertTriangle className="w-3 h-3 inline mr-1" />
                          These are general ranges. Every baby is different. Contact your doctor if concerned.
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

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
              <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
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
              <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
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
                <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
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

      {/* Page Ad */}
      <PageAd position="bottom" />
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
          <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-gray-100">
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
        <p className="text-lg text-gray-600 dark:text-gray-300">{slide.subtitle}</p>
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
              <p className="text-gray-800 dark:text-gray-100">{instruction}</p>
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
              <p className="text-xs text-gray-700 dark:text-gray-200">{step.text}</p>
            </div>
          ))}
        </div>
      );
      
    default:
      return (
        <div className="text-center p-4 border border-gray-300 rounded bg-white">
          <p className="text-sm text-gray-600 dark:text-gray-300">{details.description}</p>
        </div>
      );
  }
};

// Training Slides Data
const getTrainingSlides = (topicId, babyAgeMonths) => {
  const isInfant = babyAgeMonths < 12;
  const ageGroup = isInfant ? 'infant' : 'toddler';

  switch (topicId) {
    case 'choking':
      return getChokingSlides(isInfant);
    case 'cpr':
      return getCPRSlides(isInfant);
    case 'assessment':
      return getAssessmentSlides();
    default:
      return [];
  }
};

const getChokingSlides = (isInfant) => [
  {
    title: "Choking Emergency Response",
    subtitle: `For ${isInfant ? 'Infants (Under 12 months)' : 'Toddlers (12+ months)'}`,
    diagram: {
      emoji: "🚨",
      type: "emergency_alert",
      details: { description: "Recognize choking signs immediately" }
    },
    emergency: [
      "Baby cannot cry, cough, or make sounds",
      "Baby is turning blue around lips or face",
      "Baby appears panicked or distressed",
      "Baby is unconscious"
    ]
  },
  {
    title: "Step 1: Assess the Situation",
    instructions: [
      "Stay calm and act quickly",
      "Check if baby can cry or cough - if yes, encourage coughing",
      "Look in mouth for visible object - remove only if you can see it clearly",
      "DO NOT blindly finger sweep - this can push object deeper"
    ],
    notes: [
      "If baby is coughing forcefully, let them continue",
      "Never shake a choking baby",
      "Call for someone to dial 911 immediately"
    ]
  },
  {
    title: isInfant ? "Step 2: Position Baby (Infant)" : "Step 2: Position Child (Toddler)",
    diagram: {
      emoji: isInfant ? "👶" : "🧒",
      type: "body_position",
      details: {
        position: isInfant ? "Face down on your forearm, head lower than body" : "Bend child forward at waist",
        support: isInfant ? "Support head with your hand" : "Support chest with one hand"
      }
    },
    instructions: isInfant ? [
      "Sit down and place baby face-down along your forearm",
      "Support baby's head with your hand under the jaw",
      "Keep baby's head lower than their body",
      "Rest your arm on your thigh for support"
    ] : [
      "Stand or kneel beside the child",
      "Bend child forward at the waist",
      "Support their chest with one hand",
      "Keep their head lower than chest"
    ]
  },
  {
    title: "Step 3: Back Blows",
    diagram: {
      emoji: "✋",
      type: "hand_position",
      details: {
        position: "Heel of hand between shoulder blades",
        pressure: "Firm, sharp blows - don't hold back"
      }
    },
    instructions: [
      "Use the heel of your free hand",
      "Give 5 firm back blows between the shoulder blades",
      "Each blow should be separate and forceful",
      "Check mouth after each blow for the object"
    ],
    notes: [
      "Back blows should be firm enough to dislodge object",
      "Don't be afraid to use force - you're trying to save a life"
    ]
  },
  {
    title: isInfant ? "Step 4: Chest Thrusts (Infant)" : "Step 4: Abdominal Thrusts (Toddler)",
    diagram: {
      emoji: isInfant ? "👐" : "🤲",
      type: "technique",
      details: {
        steps: isInfant ? [
          { icon: "👶", text: "Turn baby face-up" },
          { icon: "☝️", text: "2 fingers on breastbone" },
          { icon: "⬇️", text: "5 quick thrusts" },
          { icon: "👀", text: "Check mouth" }
        ] : [
          { icon: "🧒", text: "Stand behind child" },
          { icon: "✊", text: "Fist above navel" },
          { icon: "⬆️", text: "5 upward thrusts" },
          { icon: "👀", text: "Check mouth" }
        ]
      }
    },
    instructions: isInfant ? [
      "Turn baby face-up on your arm or lap",
      "Place 2 fingers on breastbone, just below nipple line",
      "Give 5 quick, firm chest thrusts",
      "Push down about 1.5 inches each time"
    ] : [
      "Stand behind child, wrap arms around waist",
      "Make a fist with one hand, place above navel",
      "Grasp fist with other hand",
      "Give 5 quick upward thrusts"
    ]
  },
  {
    title: "Step 5: Continue Cycle",
    instructions: [
      "Alternate between back blows and chest/abdominal thrusts",
      "Continue until object comes out or baby becomes unconscious",
      "Check mouth between cycles - remove object if visible",
      "If baby becomes unconscious, begin CPR immediately"
    ],
    emergency: [
      "Baby becomes unconscious",
      "Baby stops breathing",
      "You cannot dislodge the object after several cycles",
      "Baby's lips turn blue"
    ]
  },
  {
    title: "Prevention Tips",
    instructions: [
      "Cut food into small pieces (smaller than baby's thumb nail)",
      "Avoid hard foods like nuts, hard candy, whole grapes",
      "Always supervise meals and snacks",
      "Keep small objects out of reach",
      "Teach older children to chew slowly"
    ],
    notes: [
      "Most choking incidents are preventable",
      "Learn to recognize choking hazards",
      "Take a hands-on first aid course for practice"
    ]
  }
];

const getCPRSlides = (isInfant) => [
  {
    title: "Infant CPR Overview",
    subtitle: `For ${isInfant ? 'Babies Under 12 months' : 'Children 12+ months'}`,
    diagram: {
      emoji: "❤️",
      type: "emergency_alert",
      details: { description: "CPR can save lives when breathing or heartbeat stops" }
    },
    emergency: [
      "Baby is not breathing",
      "Baby has no pulse or heartbeat",
      "Baby is unconscious and unresponsive",
      "Baby's skin is blue or gray"
    ]
  },
  {
    title: "Step 1: Check Responsiveness",
    instructions: [
      "Gently tap baby's shoulders and shout their name",
      "Look for normal breathing for no more than 10 seconds",
      "Check for pulse (if trained) - don't spend more than 10 seconds",
      "If no response and no normal breathing, begin CPR immediately"
    ],
    notes: [
      "Don't shake the baby vigorously",
      "Agonal breathing (gasping) is not normal breathing",
      "When in doubt, start CPR - it's better to do CPR on someone who doesn't need it than to not do it when they do"
    ]
  },
  {
    title: "Step 2: Position Baby",
    diagram: {
      emoji: "👶",
      type: "body_position",
      details: {
        position: "Baby on firm, flat surface - back, head tilted slightly",
        support: "Open airway by tilting head back gently"
      }
    },
    instructions: [
      "Place baby on firm, flat surface (floor, table)",
      "Tilt head back slightly by lifting chin",
      "Don't overextend the neck - babies have short necks",
      "Ensure airway is open"
    ],
    notes: [
      "Surface must be firm for effective compressions",
      "If on bed, consider moving to floor"
    ]
  },
  {
    title: "Step 3: Hand Position for Compressions",
    diagram: {
      emoji: "✌️",
      type: "hand_position",
      details: {
        position: isInfant ? "2 fingers on breastbone, below nipple line" : "Heel of one hand on lower breastbone",
        pressure: isInfant ? "Press down 1.5 inches" : "Press down 2 inches"
      }
    },
    instructions: isInfant ? [
      "Place 2 fingers (index and middle) on breastbone",
      "Position just below the nipple line",
      "Keep fingers straight and perpendicular to chest",
      "Use only fingertips, not whole hand"
    ] : [
      "Place heel of one hand on lower half of breastbone",
      "Place other hand on top, interlace fingers",
      "Keep arms straight, shoulders over hands",
      "Don't lean on ribs"
    ]
  },
  {
    title: "Step 4: Perform Compressions",
    diagram: {
      emoji: "🔄",
      type: "technique",
      details: {
        steps: [
          { icon: "⬇️", text: "Push hard & fast" },
          { icon: "⬆️", text: "Complete release" },
          { icon: "🎵", text: "100-120/minute" },
          { icon: "🔢", text: "Count out loud" }
        ]
      }
    },
    instructions: [
      `Push hard and fast - compress at least ${isInfant ? '1.5' : '2'} inches`,
      "Allow complete chest recoil between compressions",
      "Compress at 100-120 beats per minute",
      "Count out loud: '1 and 2 and 3...'",
      "Minimize interruptions"
    ],
    notes: [
      "Don't be afraid to push hard - broken ribs heal, brains don't",
      "Quality compressions save lives",
      "Switch with someone every 2 minutes if possible"
    ]
  },
  {
    title: "Step 5: Rescue Breaths (If Trained)",
    instructions: [
      "After 30 compressions, tilt head back and lift chin",
      "Cover baby's mouth and nose with your mouth",
      "Give 2 gentle breaths, watch chest rise with each",
      "If trained in hands-only CPR, continue compressions without breaths"
    ],
    notes: [
      "Breaths should be gentle - baby's lungs are small",
      "Hands-only CPR is still effective",
      "Don't delay compressions for rescue breaths"
    ]
  },
  {
    title: "Continue CPR Until Help Arrives",
    instructions: [
      "Continue cycles of 30 compressions and 2 breaths",
      "Don't stop unless baby starts breathing normally",
      "Switch with someone every 2 minutes to avoid fatigue",
      "Continue until emergency medical services arrive"
    ],
    emergency: [
      "Continue CPR even if you're tired",
      "Don't check pulse during CPR unless baby moves",
      "Be prepared to continue for extended periods"
    ]
  }
];

const getAssessmentSlides = () => [
  {
    title: "Emergency Assessment",
    subtitle: "How to Quickly Assess Any Emergency Situation",
    diagram: {
      emoji: "🔍",
      type: "emergency_alert",
      details: { description: "Quick assessment can save precious time" }
    },
    instructions: [
      "Stay calm and think before acting",
      "Ensure scene is safe for you and baby",
      "Call 911 immediately for serious emergencies",
      "Follow the ABC approach: Airway, Breathing, Circulation"
    ]
  },
  {
    title: "Check for Responsiveness",
    diagram: {
      emoji: "👋",
      type: "technique",
      details: {
        steps: [
          { icon: "👋", text: "Gentle tap" },
          { icon: "🗣️", text: "Call name loudly" },
          { icon: "👀", text: "Watch for response" },
          { icon: "📞", text: "Call 911 if none" }
        ]
      }
    },
    instructions: [
      "Gently tap baby's shoulders",
      "Call their name loudly",
      "Look for any movement or response",
      "If no response, call 911 immediately"
    ],
    notes: [
      "Don't shake vigorously",
      "Any response, even slight movement, is good"
    ]
  },
  {
    title: "Check Breathing",
    instructions: [
      "Look at chest for rise and fall",
      "Listen for breath sounds",
      "Feel for air on your cheek",
      "Normal breathing: 20-60 breaths per minute for infants"
    ],
    notes: [
      "Irregular breathing in babies can be normal",
      "Gasping is NOT normal breathing",
      "When in doubt, get medical help"
    ]
  },
  {
    title: "When to Call 911 Immediately",
    emergency: [
      "Baby is unconscious or unresponsive",
      "Not breathing or turning blue",
      "Choking and cannot cry or cough",
      "Severe allergic reaction",
      "High fever with lethargy (under 3 months: any fever)",
      "Severe injury or bleeding",
      "Poisoning or suspected poisoning",
      "Any time you're worried about baby's safety"
    ]
  },
  {
    title: "Information to Give 911",
    instructions: [
      "Your location and phone number",
      "Baby's age and what happened",
      "Current condition (conscious, breathing, etc.)",
      "What you've done so far",
      "Follow dispatcher's instructions exactly"
    ],
    notes: [
      "Stay on the phone unless told to hang up",
      "Dispatcher can guide you through emergency care",
      "Don't hang up until help arrives"
    ]
  }
];

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
          <span className="text-gray-700 dark:text-gray-200">{note}</span>
        </div>
      ))}
    </div>
  );
};

export default EmergencyTraining;