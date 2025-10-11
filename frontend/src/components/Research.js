import React from 'react';
import ChatKitWrapper from './ChatKitWrapper';
import PageAd from './ads/PageAd';

const Research = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-6 fade-in">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold font-display text-gray-900 dark:text-white mb-4" data-testid="research-title">
          Research & Parenting Tips
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Ask questions and get reliable parenting guidance
        </p>
      </div>

      {/* ChatKit Integration */}
      <ChatKitWrapper 
        mode="research"
        title="AI Parenting Assistant"
        placeholder="Ask about feeding, sleep, development..."
        knowledgeBase="ai_assistant"
      />

      {/* Page Ad */}
      <PageAd position="bottom" />
    </div>
  );
};

// Helper components removed - now using ChatKitWrapper

export default Research;