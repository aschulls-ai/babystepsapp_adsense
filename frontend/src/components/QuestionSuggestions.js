import React, { useState, useEffect, useMemo } from 'react';
import { Search, ChevronDown, MessageCircle, Shield } from 'lucide-react';
import knowledgeBaseService from '../knowledgeBase';

const QuestionSuggestions = ({ 
  query, 
  onSelectQuestion, 
  type, // 'ai_assistant' or 'food_research'
  isOpen, 
  onToggle,
  placeholder = "Type your question..."
}) => {
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Get relevant questions based on user input
  const findRelevantQuestions = useMemo(() => {
    return (searchQuery, knowledgeBaseType) => {
      if (!searchQuery || searchQuery.length < 2) return [];
      
      const kb = knowledgeBaseService.knowledgeBases[knowledgeBaseType];
      if (!kb || !Array.isArray(kb)) return [];

      const queryLower = searchQuery.toLowerCase();
      const queryWords = searchQuery.toLowerCase().split(' ').filter(word => word.length > 2);
      
      // Score and rank questions
      const scoredQuestions = kb.map(question => {
        let score = 0;
        const questionLower = question.question.toLowerCase();
        const answerLower = (question.answer || '').toLowerCase();
        
        // Exact phrase match (highest priority)
        if (questionLower.includes(queryLower)) {
          score += 100;
        }
        
        // Word matching
        queryWords.forEach(word => {
          if (questionLower.includes(word)) score += 20;
          if (answerLower.includes(word)) score += 10;
          if (question.category && question.category.toLowerCase().includes(word)) score += 15;
        });
        
        // Boost for question starts with similar pattern
        if (questionLower.startsWith(queryWords[0])) {
          score += 30;
        }
        
        // Category relevance for food research
        if (knowledgeBaseType === 'food_research') {
          const foodWords = ['safe', 'eat', 'food', 'baby', 'month', 'age'];
          foodWords.forEach(foodWord => {
            if (queryLower.includes(foodWord)) score += 5;
          });
        }
        
        return { question, score };
      });

      // Filter and sort by score
      return scoredQuestions
        .filter(item => item.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 6) // Limit to top 6 suggestions
        .map(item => item.question);
    };
  }, []);

  // Update suggestions when query changes
  useEffect(() => {
    if (!query || query.length < 2) {
      setSuggestions([]);
      return;
    }

    const timeoutId = setTimeout(() => {
      setIsLoading(true);
      const relevantQuestions = findRelevantQuestions(query, type);
      setSuggestions(relevantQuestions);
      setIsLoading(false);
    }, 300); // Debounce for 300ms

    return () => clearTimeout(timeoutId);
  }, [query, type, findRelevantQuestions]);

  const handleSelectQuestion = (question) => {
    onSelectQuestion(question);
    onToggle(false); // Close dropdown
  };

  const getIconForType = (type) => {
    return type === 'food_research' ? Shield : MessageCircle;
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Feeding': 'bg-blue-100 text-blue-800',
      'Safety': 'bg-red-100 text-red-800',
      'Sleep': 'bg-purple-100 text-purple-800',
      'Development': 'bg-green-100 text-green-800',
      'Health': 'bg-orange-100 text-orange-800',
      'Behavior': 'bg-yellow-100 text-yellow-800',
      'Nutrition': 'bg-emerald-100 text-emerald-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  if (!isOpen || suggestions.length === 0) {
    return null;
  }

  const Icon = getIconForType(type);

  return (
    <div className="absolute top-full left-0 right-0 z-50 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg max-h-96 overflow-y-auto">
      {isLoading ? (
        <div className="p-4 text-center">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Finding relevant questions...</p>
        </div>
      ) : (
        <>
          <div className="p-3 border-b border-gray-100 dark:border-gray-700">
            <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <Icon className="w-4 h-4" />
              <span>Suggested questions ({suggestions.length})</span>
            </div>
          </div>
          
          <div className="max-h-80 overflow-y-auto">
            {suggestions.map((question, index) => (
              <div
                key={question.id || index}
                onClick={() => handleSelectQuestion(question)}
                className="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer border-b border-gray-50 dark:border-gray-700 last:border-b-0 transition-colors duration-150"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-1 leading-5">
                      {question.question}
                    </h4>
                    
                    <div className="flex items-center gap-2 mb-2">
                      {question.category && (
                        <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(question.category)}`}>
                          {question.category}
                        </span>
                      )}
                      {question.age_range && (
                        <span className="inline-block px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 dark:bg-gray-600 dark:text-gray-300">
                          {question.age_range}
                        </span>
                      )}
                    </div>
                    
                    <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">
                      {typeof question.answer === 'string' 
                        ? question.answer.substring(0, 120) + (question.answer.length > 120 ? '...' : '')
                        : 'Click to see detailed information'
                      }
                    </p>
                  </div>
                  
                  <ChevronDown className="w-4 h-4 text-gray-400 transform -rotate-90 flex-shrink-0" />
                </div>
              </div>
            ))}
          </div>
          
          <div className="p-3 border-t border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-750">
            <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
              Click on a question to get the full answer, or continue typing for AI search
            </p>
          </div>
        </>
      )}
    </div>
  );
};

export default QuestionSuggestions;