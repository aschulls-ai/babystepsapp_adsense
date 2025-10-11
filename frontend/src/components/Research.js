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

// Helper Components
const MessageBubble = ({ message }) => {
  if (!message || !message.content) {
    console.error('Invalid message:', message);
    return null;
  }

  const isBot = message.type === 'bot' || message.type === 'assistant';

  return (
    <div className={`flex items-start gap-3 ${isBot ? '' : 'flex-row-reverse'} w-full`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        isBot 
          ? 'bg-rose-500 text-white' 
          : 'bg-blue-500 text-white'
      }`}>
        {isBot ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
      </div>
      
      <div className={`flex-1 max-w-[calc(100%-3rem)] min-w-0 ${isBot ? '' : 'text-right'}`}>
        <div className={`px-4 py-3 rounded-lg max-w-full overflow-hidden ${
          isBot 
            ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100' 
            : 'bg-blue-500 dark:bg-blue-600 text-white'
        }`}>
          <p className="whitespace-pre-wrap break-words overflow-wrap-anywhere">{message.content || ''}</p>
          {message.sources && message.sources.length > 0 && (
            <div className="mt-2 pt-2 border-t border-gray-200">
              <p className="text-xs text-gray-500">Sources: {message.sources.join(', ')}</p>
            </div>
          )}
        </div>
        <p className="text-xs text-gray-400 mt-1">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
};

const QuickQuestionButton = ({ icon, question, category, onClick }) => (
  <button
    onClick={onClick}
    className="w-full text-left p-3 bg-white rounded-lg border border-gray-200 hover:border-rose-300 hover:bg-rose-50 transition-all duration-200 group"
    data-testid={`quick-question-${category.toLowerCase()}`}
  >
    <div className="flex items-start gap-3">
      <div className="p-2 bg-gray-100 rounded-lg group-hover:bg-rose-100 transition-colors duration-200">
        {icon}
      </div>
      <div className="flex-1">
        <div className="text-xs text-gray-500 font-medium mb-1">{category}</div>
        <div className="text-sm text-gray-900 dark:text-white font-medium">{question}</div>
      </div>
    </div>
  </button>
);

const TipCard = ({ title, content, icon }) => (
  <div className="p-3 bg-white rounded-lg border border-gray-200">
    <div className="flex items-start gap-3">
      <div className="p-2 bg-gray-100 rounded-lg">
        {icon}
      </div>
      <div className="flex-1">
        <h4 className="font-medium text-gray-900 dark:text-white text-sm mb-1">{title}</h4>
        <p className="text-xs text-gray-600">{content}</p>
      </div>
    </div>
  </div>
);

export default Research;