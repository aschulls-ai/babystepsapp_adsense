import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Send, Bot, User, Wifi, WifiOff } from 'lucide-react';
import { toast } from 'sonner';
import PageAd from './ads/PageAd';
import { androidFetch } from '../App';

const AIAssistant = ({ currentBaby }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Monitor online/offline status
  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      toast.success('Connected to internet');
    };
    
    const handleOffline = () => {
      setIsOnline(false);
      toast.error('No internet connection - AI Assistant requires internet');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim()) return;
    
    if (!isOnline) {
      toast.error('No internet connection. AI Assistant requires internet to work.');
      return;
    }

    const userMessage = {
      id: `user-${Date.now()}`,
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      // Get auth token with validation
      let token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Not authenticated - please login again');
      }
      
      // Validate token format (basic check)
      if (!token.includes('.') || token.split('.').length !== 3) {
        console.log('🔑 Invalid token format detected, clearing token');
        localStorage.removeItem('token');
        throw new Error('Invalid authentication token - please login again');
      }

      // Add baby context to the message
      let contextMessage = userMessage.content;
      if (currentBaby) {
        const babyAgeMonths = Math.floor(
          (new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44)
        );
        contextMessage = `[Baby: ${currentBaby.name}, Age: ${babyAgeMonths} months] ${userMessage.content}`;
      }

      // Call backend API using Android-optimized fetch
      const response = await androidFetch(`${process.env.REACT_APP_BACKEND_URL}/api/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: contextMessage,
          baby_age_months: currentBaby ? Math.floor(
            (new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44)
          ) : null
        })
      });

      if (!response.ok) {
        // Handle authentication errors specifically
        if (response.status === 401) {
          console.log('🔑 Authentication failed (401), clearing token and requesting re-login');
          localStorage.removeItem('token');
          throw new Error('Your session has expired. Please logout and login again to use the AI Assistant.');
        }
        
        let errorMessage = 'Failed to get response';
        try {
          const error = await response.json();
          errorMessage = error.detail || errorMessage;
        } catch (e) {
          console.log('Could not parse error response');
        }
        
        throw new Error(errorMessage);
      }

      const data = await response.json();

      const aiMessage = {
        id: `assistant-${Date.now()}`,
        type: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, aiMessage]);
      
    } catch (error) {
      console.error('AI Assistant error:', error);
      
      const errorMessage = {
        id: `error-${Date.now()}`,
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure you have an internet connection and try again.',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      toast.error('Failed to get AI response');
    } finally {
      setLoading(false);
    }
  };

  const MessageBubble = ({ message }) => {
    const isBot = message.type === 'assistant' || message.type === 'bot';

    return (
      <div className={`flex items-start gap-3 ${isBot ? '' : 'flex-row-reverse'} w-full mb-4`}>
        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
          isBot ? 'bg-rose-500 text-white' : 'bg-blue-500 text-white'
        }`}>
          {isBot ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5" />}
        </div>
        
        <div className={`flex-1 max-w-[80%] ${isBot ? '' : 'text-right'}`}>
          <div className={`px-4 py-3 rounded-lg ${
            isBot 
              ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100' 
              : 'bg-blue-500 dark:bg-blue-600 text-white'
          }`}>
            <p className="whitespace-pre-wrap break-words">{message.content}</p>
          </div>
        </div>
      </div>
    );
  };

  const quickQuestions = [
    "Can my baby eat strawberries?",
    "What breakfast ideas for my baby?",
    "How much should my baby sleep?",
    "When can babies start walking?"
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-6 fade-in">
      {/* Header */}
      <div className="text-center mb-6">
        <div className="flex items-center justify-center gap-2 mb-2">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
            AI Parenting Assistant
          </h1>
          {isOnline ? (
            <Wifi className="w-6 h-6 text-green-500" title="Online - AI Active" />
          ) : (
            <WifiOff className="w-6 h-6 text-red-500" title="Offline - AI Unavailable" />
          )}
        </div>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          Ask any question for parenting guidance, meal prep, food safety, and general baby care knowledge
        </p>
        {currentBaby && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Getting personalized guidance for <span className="font-semibold text-rose-600">{currentBaby.name}</span>
          </p>
        )}
        <div className="flex items-center justify-center gap-2 mt-2">
          <div className="flex items-center gap-1 text-sm text-blue-600 dark:text-blue-400">
            <Wifi className="w-4 h-4" />
            <span>Powered by OpenAI - Internet Required</span>
          </div>
        </div>
      </div>

      {/* Chat Container */}
      <Card className="border-2 border-rose-200 dark:border-rose-800 shadow-xl">
        <CardContent className="p-6">
          {/* Messages Area */}
          <div className="h-[500px] overflow-y-auto mb-4 space-y-4 scroll-smooth">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <Bot className="w-16 h-16 mx-auto mb-4 text-rose-500" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  Welcome to AI Parenting Assistant!
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Ask me anything about baby care, food safety, meals, sleep, or development.
                </p>
                
                {/* Quick Questions */}
                <div className="max-w-2xl mx-auto">
                  <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">Quick questions to try:</p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {quickQuestions.map((question, idx) => (
                      <button
                        key={idx}
                        onClick={() => setInputValue(question)}
                        className="text-left px-4 py-2 bg-rose-50 dark:bg-rose-900/20 hover:bg-rose-100 dark:hover:bg-rose-900/40 rounded-lg text-sm text-gray-700 dark:text-gray-300 transition-colors"
                      >
                        {question}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <MessageBubble key={message.id} message={message} />
                ))}
                {loading && (
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-rose-500 flex items-center justify-center">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-rose-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="flex gap-3">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={isOnline ? "Ask me anything about your baby..." : "No internet connection"}
              disabled={loading || !isOnline}
              className="flex-1 px-4 py-3 border-2 border-gray-200 dark:border-gray-600 rounded-xl focus:border-rose-400 focus:ring-2 focus:ring-rose-100"
            />
            <Button
              type="submit"
              disabled={loading || !inputValue.trim() || !isOnline}
              className="bg-gradient-to-r from-rose-500 to-pink-500 hover:from-rose-600 hover:to-pink-600 text-white px-6 py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <Send className="w-5 h-5" />
              )}
            </Button>
          </form>

          {/* Disclaimer */}
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-4 text-center">
            💡 AI-powered responses are for educational purposes only. Always consult your pediatrician for medical advice.
          </p>
        </CardContent>
      </Card>

      {/* Page Ad */}
      <div className="mt-6">
        <PageAd position="bottom" />
      </div>
    </div>
  );
};

export default AIAssistant;