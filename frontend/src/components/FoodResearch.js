import React from 'react';
import ChatKitWrapper from './ChatKitWrapper';
import PageAd from './ads/PageAd';

const FoodResearch = ({ currentBaby }) => {
  return (
    <div className="max-w-6xl mx-auto space-y-6 fade-in">
      <ChatKitWrapper
        currentBaby={currentBaby}
        pageType="food-research"
        title="Food Safety Research"
        subtitle="Get personalized food safety guidance for your baby"
        heroImage="https://images.unsplash.com/photo-1557939663-0619f304af9c"
        heroAlt="Baby safely eating age-appropriate foods"
        placeholder="Ask about food safety... (e.g., 'Can my 8-month-old have strawberries?')"
        gradientFrom="from-green-600/80"
        gradientTo="to-emerald-600/80"
        iconColor="text-green-500"
        buttonGradient="from-green-500 to-emerald-500"
        buttonHoverGradient="from-green-600 to-emerald-600"
      />
      
      {/* Page Ad */}
      <PageAd position="bottom" />
    </div>
  );

export default FoodResearch;