import React from 'react';
import ChatKitWrapper from './ChatKitWrapper';
import PageAd from './ads/PageAd';

const Research = ({ currentBaby }) => {
  return (
    <div className="space-y-6 fade-in">
      {/* ChatKit Integration */}
      <ChatKitWrapper 
        title="AI Parenting Assistant"
        subtitle="Ask questions and get reliable, evidence-based parenting guidance"
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