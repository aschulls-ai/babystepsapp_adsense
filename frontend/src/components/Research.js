import React from 'react';
import ChatKitWrapper from './ChatKitWrapper';
import PageAd from './ads/PageAd';

const Research = ({ currentBaby }) => {
  return (
    <div className="space-y-6 fade-in">
      {/* ChatKit Integration */}
      <ChatKitWrapper 
        title="AI Parenting Assistant"
        subtitle="Ask any question for parenting guidance, meal prep, food safety, and general baby care knowledge"
        currentBaby={currentBaby}
      />

      {/* Page Ad */}
      <div className="mt-6">
        <PageAd position="bottom" />
      </div>
    </div>
  );
};

export default Research;