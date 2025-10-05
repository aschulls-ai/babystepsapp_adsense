import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Baby, Plus } from 'lucide-react';
import CustomizableDashboard from './CustomizableDashboard';

const Dashboard = ({ currentBaby, onAddBaby }) => {
  if (!currentBaby) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <WelcomeCard onAddBaby={onAddBaby} />
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in">
      <CustomizableDashboard currentBaby={currentBaby} />
    </div>
  );
};

// Helper Components
const WelcomeCard = ({ onAddBaby }) => (
  <Card className="glass-strong border-0 max-w-md mx-auto text-center">
    <CardContent className="p-8">
      <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
        <Baby className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-2xl font-bold font-display text-gray-900 mb-4">
        Welcome to Baby Steps!
      </h2>
      <p className="text-gray-600 mb-6">
        Let's start by adding your baby's profile to get personalized nutrition guidance and safety information.
      </p>
      <Button
        onClick={() => window.location.href = '/baby-profile'}
        className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="add-first-baby-btn"
      >
        <Plus className="w-5 h-5 mr-2" />
        Add Your Baby
      </Button>
    </CardContent>
  </Card>
);

export default Dashboard;

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <QuickActionCard
          title="Food Safety Check"
          description="Check if foods are safe for your baby's age"
          icon={<Search className="w-8 h-8 text-green-600" />}
          href="/food-research"
          color="green"
          testId="food-research-action"
        />
        <QuickActionCard
          title="Emergency Training"
          description="Learn CPR and choking response"
          icon={<ShieldAlert className="w-8 h-8 text-red-600" />}
          href="/emergency-training"
          color="red"
          urgent={true}
          testId="emergency-training-action"
        />
        <QuickActionCard
          title="Meal Planner"
          description="Age-appropriate meal ideas and recipes"
          icon={<ChefHat className="w-8 h-8 text-orange-600" />}
          href="/meal-planner"
          color="orange"
          testId="meal-planner-action"
        />
        <QuickActionCard
          title="Baby Profile"
          description="Update your baby's information"
          icon={<Baby className="w-8 h-8 text-blue-600" />}
          href="/baby-profile"
          color="blue"
          testId="baby-profile-action"
        />
      </div>

      {/* Age-Specific Guidelines */}
      <div className="grid lg:grid-cols-2 gap-6">
        <Card className="glass-strong border-0" data-testid="feeding-guidelines">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-800">
              <BookOpen className="w-5 h-5 text-green-500" />
              Feeding Guidelines for {babyAgeMonths} Months
            </CardTitle>
          </CardHeader>
          <CardContent>
            <FeedingGuidelines babyAgeMonths={babyAgeMonths} />
          </CardContent>
        </Card>

        <Card className="emergency-card border-0" data-testid="safety-reminders">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-800">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              Safety Reminders
            </CardTitle>
          </CardHeader>
          <CardContent>
            <SafetyReminders babyAgeMonths={babyAgeMonths} />
          </CardContent>
        </Card>
      </div>

      {/* Educational Content */}
      <div className="grid lg:grid-cols-3 gap-6">
        <EducationalCard
          title="Introduction Timeline"
          content="Learn when to introduce different food groups and textures safely."
          icon={<Clock className="w-6 h-6 text-green-500" />}
          age="6+ months"
        />
        <EducationalCard
          title="Allergy Prevention"
          content="Evidence-based approaches to introducing common allergens."
          icon={<Heart className="w-6 h-6 text-red-500" />}
          age="All ages"
        />
        <EducationalCard
          title="Cultural Practices"
          content="Explore diverse cultural approaches to baby feeding safely."
          icon={<ChefHat className="w-6 h-6 text-orange-500" />}
          age="6+ months"
        />
      </div>
    </div>
  );
};

// Helper Components
const WelcomeCard = ({ onAddBaby }) => (
  <Card className="glass-strong border-0 max-w-md mx-auto text-center">
    <CardContent className="p-8">
      <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
        <Baby className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-2xl font-bold font-display text-gray-900 mb-4">
        Welcome to Baby Steps!
      </h2>
      <p className="text-gray-600 mb-6">
        Let's start by adding your baby's profile to get personalized nutrition guidance and safety information.
      </p>
      <Button
        onClick={() => window.location.href = '/baby-profile'}
        className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="add-first-baby-btn"
      >
        <Plus className="w-5 h-5 mr-2" />
        Add Your Baby
      </Button>
    </CardContent>
  </Card>
);

const AgeBasedAlert = ({ babyAgeMonths }) => {
  let alertContent;
  let alertType = "info";

  if (babyAgeMonths < 4) {
    alertContent = {
      title: "Exclusive Milk Feeding Period",
      message: "Your baby should only receive breast milk or formula. No solid foods, water, or other liquids are recommended.",
      type: "safe"
    };
  } else if (babyAgeMonths < 6) {
    alertContent = {
      title: "Pre-Solid Food Period", 
      message: "You're approaching the introduction period! Start preparing for solid foods around 6 months.",
      type: "caution"
    };
  } else if (babyAgeMonths < 12) {
    alertContent = {
      title: "Food Introduction Phase",
      message: "Time to introduce solid foods! Start with single ingredients and watch for allergic reactions.",
      type: "safe"
    };
  } else {
    alertContent = {
      title: "Varied Diet Phase",
      message: "Your toddler can enjoy most foods! Continue to avoid choking hazards and monitor for reactions.",
      type: "safe"
    };
  }

  return (
    <Card className={`border-0 food-${alertContent.type}`} data-testid="age-alert">
      <CardContent className="p-4">
        <div className="flex items-center gap-3">
          <CheckCircle className="w-6 h-6 text-current" />
          <div>
            <h3 className="font-semibold text-gray-900">{alertContent.title}</h3>
            <p className="text-gray-700 text-sm">{alertContent.message}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const QuickActionCard = ({ title, description, icon, href, color, urgent = false, testId }) => (
  <Card className={`card-interactive hover:scale-105 transition-all duration-300 ${urgent ? 'emergency-card' : ''}`}>
    <CardContent className="p-6 text-center">
      <div className={`mb-4 flex justify-center ${urgent ? 'animate-pulse' : ''}`}>
        {icon}
      </div>
      <h3 className="font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm mb-4">{description}</p>
      <Button
        onClick={() => window.location.href = href}
        className={`w-full ${
          urgent 
            ? 'btn-emergency' 
            : color === 'green' 
              ? 'btn-primary' 
              : 'bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white'
        } py-2 rounded-xl transition-all duration-300`}
        data-testid={testId}
      >
        {urgent ? 'Start Training' : 'Get Started'}
      </Button>
    </CardContent>
  </Card>
);

const FeedingGuidelines = ({ babyAgeMonths }) => {
  let guidelines;

  if (babyAgeMonths < 6) {
    guidelines = [
      "Breast milk or formula only",
      "Feed on demand (8-12 times/day)",
      "No water, juice, or solid foods",
      "Watch for growth and development cues"
    ];
  } else if (babyAgeMonths < 12) {
    guidelines = [
      "Continue breast milk or formula",
      "Introduce single-ingredient purees",
      "Start with iron-rich foods",
      "Introduce one new food every 3-5 days",
      "Watch for allergic reactions"
    ];
  } else {
    guidelines = [
      "Transition to family foods",
      "Include variety from all food groups",
      "Continue breast milk or whole milk",
      "Avoid choking hazards",
      "Encourage self-feeding"
    ];
  }

  return (
    <div className="space-y-3">
      {guidelines.map((guideline, index) => (
        <div key={index} className="flex items-center gap-3">
          <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
          <span className="text-gray-700 text-sm">{guideline}</span>
        </div>
      ))}
    </div>
  );
};

const SafetyReminders = ({ babyAgeMonths }) => {
  const safetyTips = [
    "Always supervise during feeding",
    "Keep emergency numbers handy",
    "Learn infant CPR and choking response",
    "Check food temperature before serving",
    "Ensure proper food storage and hygiene"
  ];

  return (
    <div className="space-y-3">
      {safetyTips.map((tip, index) => (
        <div key={index} className="flex items-center gap-3">
          <AlertTriangle className="w-4 h-4 text-red-500 flex-shrink-0" />
          <span className="text-gray-700 text-sm">{tip}</span>
        </div>
      ))}
      <div className="mt-4 p-3 bg-red-50 rounded-lg">
        <p className="text-xs text-red-700">
          <strong>Emergency:</strong> Call 911 immediately if your baby is choking, unconscious, or having trouble breathing.
        </p>
      </div>
    </div>
  );
};

const EducationalCard = ({ title, content, icon, age }) => (
  <Card className="glass border-0 hover:shadow-lg transition-all duration-300">
    <CardContent className="p-6">
      <div className="flex items-center gap-3 mb-3">
        {icon}
        <div>
          <h3 className="font-semibold text-gray-900">{title}</h3>
          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{age}</span>
        </div>
      </div>
      <p className="text-gray-600 text-sm">{content}</p>
    </CardContent>
  </Card>
);

export default Dashboard;