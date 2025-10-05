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