import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { 
  BookOpen, 
  Send, 
  Bot, 
  User, 
  Lightbulb,
  Heart,
  Baby,
  Stethoscope,
  Moon,
  Milk,
  Clock
} from 'lucide-react';
import { toast } from 'sonner';
import PageAd from './ads/PageAd';

const Research = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const quickQuestions = [
    {
      icon: <Milk className="w-5 h-5" />,
      question: "How often should I feed my newborn?",
      category: "Feeding"
    },
    {
      icon: <Moon className="w-5 h-5" />,
      question: "What are normal sleep patterns for a 2-month-old?",
      category: "Sleep"
    },
    {
      icon: <Baby className="w-5 h-5" />,
      question: "When do babies typically start rolling over?",
      category: "Development"
    },
    {
      icon: <Stethoscope className="w-5 h-5" />,
      question: "What temperature is considered a fever in infants?",
      category: "Health"
    }
  ];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await axios.post('/research', {
        question: userMessage.content
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.answer,
        sources: response.data.sources || [],
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      toast.error('Failed to get research answer. Please try again.');
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I'm sorry, I'm having trouble accessing the research database right now. Please try again later, or consult your pediatrician for specific medical questions.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 fade-in">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold font-display text-gray-900 mb-4" data-testid="research-title">
          Research & Parenting Tips
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Get evidence-based answers to your parenting questions from our AI assistant trained on reliable medical sources
        </p>
      </div>

      {/* Hero Image */}
      <div className="relative h-64 rounded-2xl overflow-hidden mb-8">
        <img 
          src="https://images.unsplash.com/photo-1635770608350-0636bd391ea7"
          alt="Parent researching baby care"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-rose-600/80 to-pink-600/80 flex items-center justify-center">
          <div className="text-center text-white">
            <BookOpen className="w-16 h-16 mx-auto mb-4 opacity-90" />
            <h2 className="text-2xl font-bold mb-2">Trusted Parenting Guidance</h2>
            <p className="text-rose-100">Ask questions, get reliable answers</p>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Chat Interface */}
        <div className="lg:col-span-2">
          <Card className="glass-strong border-0 h-[600px] flex flex-col">
            <CardHeader className="flex-shrink-0">
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Bot className="w-5 h-5 text-rose-500" />
                AI Parenting Assistant
              </CardTitle>
            </CardHeader>
            
            <CardContent className="flex-1 flex flex-col p-0 min-h-0">
              {/* Messages Container - Fixed Height with Scroll */}
              <div className="flex-1 overflow-y-auto overflow-x-hidden px-6 pb-2 min-h-0">
                {messages.length === 0 ? (
                  <div className="flex items-center justify-center h-full text-center">
                    <div className="max-w-md">
                      <div className="w-20 h-20 bg-gradient-to-br from-rose-400 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                        <Lightbulb className="w-10 h-10 text-white" />
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">
                        Ask me anything about baby care!
                      </h3>
                      <p className="text-gray-600 text-sm">
                        I can help with feeding, sleep, development, health concerns, and more.
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4 py-4 min-w-0">
                    {messages.map((message) => (
                      <MessageBubble key={message.id} message={message} />
                    ))}
                    {loading && (
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-rose-500 rounded-full flex items-center justify-center">
                          <Bot className="w-4 h-4 text-white" />
                        </div>
                        <div className="bg-gray-100 rounded-lg px-4 py-2">
                          <div className="flex space-x-2">
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                            <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
                          </div>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>

              {/* Input Form */}
              <div className="border-t border-gray-200 p-6">
                <form onSubmit={handleSubmit} className="flex gap-3">
                  <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Ask about feeding, sleep, development..."
                    disabled={loading}
                    className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition-all duration-200"
                    data-testid="research-question-input"
                  />
                  <Button
                    type="submit"
                    disabled={loading || !inputValue.trim()}
                    className="bg-gradient-to-r from-rose-500 to-pink-500 hover:from-rose-600 hover:to-pink-600 text-white px-6 py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50"
                    data-testid="send-question-btn"
                  >
                    <Send className="w-5 h-5" />
                  </Button>
                </form>
                <p className="text-xs text-gray-500 mt-2 flex items-center">
                  <Clock className="w-3 h-3 mr-1" />
                  Response may take up to a minute due to AI processing and research
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Questions */}
        <div className="space-y-6">
          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Lightbulb className="w-5 h-5 text-amber-500" />
                Common Questions
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {quickQuestions.map((item, index) => (
                <QuickQuestionButton
                  key={index}
                  icon={item.icon}
                  question={item.question}
                  category={item.category}
                  onClick={() => handleQuickQuestion(item.question)}
                />
              ))}
            </CardContent>
          </Card>

          <Card className="glass border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-gray-800">
                <Heart className="w-5 h-5 text-rose-500" />
                Parenting Tips
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <TipCard
                  title="Safe Sleep"
                  content="Always place babies on their backs to sleep, use a firm sleep surface, and keep the crib bare."
                  icon={<Moon className="w-5 h-5 text-purple-500" />}
                />
                <TipCard
                  title="Feeding Cues"
                  content="Look for early hunger cues like rooting, hand-to-mouth movements, or sucking motions."
                  icon={<Milk className="w-5 h-5 text-blue-500" />}
                />
                <TipCard
                  title="Tummy Time"
                  content="Start with short periods while baby is awake and supervised to strengthen neck and shoulder muscles."
                  icon={<Baby className="w-5 h-5 text-green-500" />}
                />
              </div>
            </CardContent>
          </Card>

          <Card className="glass border-0 bg-gradient-to-br from-rose-50 to-pink-50">
            <CardContent className="p-4 text-center">
              <Stethoscope className="w-8 h-8 text-rose-500 mx-auto mb-2" />
              <p className="text-sm text-gray-700 font-medium">
                Always consult your pediatrician for specific medical concerns
              </p>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Page Ad */}
      <PageAd position="bottom" />
    </div>
  );
};

// Helper Components
const MessageBubble = ({ message }) => {
  const isBot = message.type === 'bot';

  return (
    <div className={`flex items-start gap-3 ${isBot ? '' : 'flex-row-reverse'} w-full`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        isBot 
          ? 'bg-rose-500 text-white' 
          : 'bg-blue-500 text-white'
      }`}>
        {isBot ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
      </div>
      
      <div className={`flex-1 max-w-[calc(100%-3rem)] ${isBot ? '' : 'text-right'}`}>
        <div className={`inline-block px-4 py-3 rounded-lg w-full max-w-full ${
          isBot 
            ? 'bg-gray-100 text-gray-900' 
            : 'bg-blue-500 text-white'
        }`}>
          <p className="whitespace-pre-wrap break-words word-wrap break-all hyphens-auto">{message.content}</p>
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
        <div className="text-sm text-gray-900 font-medium">{question}</div>
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
        <h4 className="font-medium text-gray-900 text-sm mb-1">{title}</h4>
        <p className="text-xs text-gray-600">{content}</p>
      </div>
    </div>
  </div>
);

export default Research;