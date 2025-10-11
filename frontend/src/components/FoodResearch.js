import React from 'react';
import ChatKitWrapper from './ChatKitWrapper';
import PageAd from './ads/PageAd';

const FoodResearch = ({ currentBaby }) => {
  return (
    <div className="space-y-6 fade-in">
      {/* ChatKit Integration */}
      <ChatKitWrapper 
        title="Food Safety Research"
        subtitle="Get evidence-based food safety guidance for your baby"
        currentBaby={currentBaby}
      />

      {/* Page Ad */}
      <div className="mt-6">
        <PageAd position="bottom" />
      </div>
    </div>
  );
};

export default FoodResearch;