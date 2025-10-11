import React from 'react';
import ChatKitWrapper from './ChatKitWrapper';
import PageAd from './ads/PageAd';

const MealPlanner = ({ currentBaby }) => {
  return (
    <div className="space-y-6 fade-in">
      {/* ChatKit Integration */}
      <ChatKitWrapper 
        title="Meal Planner"
        subtitle="Get personalized meal ideas and recipes for your baby"
        currentBaby={currentBaby}
      />

      {/* Page Ad */}
      <div className="mt-6">
        <PageAd position="bottom" />
      </div>
    </div>
  );
};

export default MealPlanner;