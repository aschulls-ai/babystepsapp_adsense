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

  // Enhanced keyword extraction and matching system
  const extractSmartKeywords = (text) => {
    const stopWords = new Set([
      'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with', 'can', 'my', 'i', 'me', 'you', 'your', 'what', 'when', 'where', 'how', 'why', 'should', 'could', 'would', 'have'
    ]);

    // Extract base keywords
    let keywords = text.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2 && !stopWords.has(word));

    // Add important context keywords based on patterns
    const contextKeywords = [];
    
    // Food-specific keywords
    const foodPatterns = {
      'avocado': /\b(avocado|avocados)\b/i,
      'honey': /\b(honey)\b/i,
      'eggs': /\b(egg|eggs)\b/i,
      'nuts': /\b(nut|nuts|peanut|peanuts|almond|almonds)\b/i,
      'fish': /\b(fish|salmon|tuna|seafood)\b/i,
      'strawberries': /\b(strawberr\w+|berr\w+)\b/i,
      'milk': /\b(milk|dairy|cheese|yogurt)\b/i,
      'meat': /\b(meat|chicken|beef|turkey|pork)\b/i
    };

    Object.entries(foodPatterns).forEach(([food, pattern]) => {
      if (pattern.test(text)) {
        contextKeywords.push(food);
      }
    });

    // Action keywords
    if (text.includes('safe') || text.includes('okay')) contextKeywords.push('safety');
    if (text.includes('eat') || text.includes('feed')) contextKeywords.push('eating');
    if (text.includes('when') || text.includes('age')) contextKeywords.push('timing');
    if (text.includes('sleep') || text.includes('nap')) contextKeywords.push('sleep');
    if (text.includes('cry') || text.includes('fuss')) contextKeywords.push('behavior');
    
    return [...new Set([...keywords, ...contextKeywords])];
  };

  // Get relevant questions based on smart keyword matching
  const findRelevantQuestions = useMemo(() => {
    return (searchQuery, knowledgeBaseType) => {
      if (!searchQuery || searchQuery.length < 2) return [];
      
      const kb = knowledgeBaseService.knowledgeBases[knowledgeBaseType];
      if (!kb || !Array.isArray(kb)) return [];

      const queryLower = searchQuery.toLowerCase();
      const smartKeywords = extractSmartKeywords(searchQuery);
      
      // Advanced scoring system
      const scoredQuestions = kb.map(question => {
        let score = 0;
        const questionLower = question.question.toLowerCase();
        const answerLower = (question.answer || '').toLowerCase();
        const categoryLower = (question.category || '').toLowerCase();
        
        // 1. Exact phrase matching (highest priority)
        if (questionLower.includes(queryLower)) {
          score += 150;
        }
        
        // 2. Smart keyword matching with different weights
        smartKeywords.forEach(keyword => {
          // Question title matches (very high weight)
          if (questionLower.includes(keyword)) {
            score += 50;
          }
          
          // Answer content matches (medium weight)
          if (answerLower.includes(keyword)) {
            score += 25;
          }
          
          // Category matches (medium weight)
          if (categoryLower.includes(keyword)) {
            score += 30;
          }
          
          // Partial matches (lower weight)
          if (questionLower.includes(keyword.slice(0, -1)) && keyword.length > 3) {
            score += 15;
          }
        });
        
        // 3. Question pattern matching
        const questionPatterns = [
          /^(is|are|can|when|how|what|why)/i,
          /(safe|okay|good|bad|avoid)/i,
          /(baby|babies|infant|child)/i,
          /(eat|drink|have|give)/i
        ];
        
        questionPatterns.forEach(pattern => {
          if (pattern.test(queryLower) && pattern.test(questionLower)) {
            score += 20;
          }
        });
        
        // 4. Age relevance (for questions with age ranges)
        if (question.age_range) {
          // Boost questions that mention age-related terms
          if (queryLower.includes('month') || queryLower.includes('old') || /\d+/.test(queryLower)) {
            score += 15;
          }
        }
        
        // 5. Type-specific boosts
        if (knowledgeBaseType === 'food_research') {
          // Food safety context boost
          const safetyTerms = ['safe', 'safety', 'eat', 'food', 'okay', 'can', 'when', 'age'];
          safetyTerms.forEach(term => {
            if (queryLower.includes(term) && questionLower.includes(term)) {
              score += 10;
            }
          });
        } else if (knowledgeBaseType === 'ai_assistant') {
          // Parenting context boost
          const parentingTerms = ['sleep', 'feed', 'cry', 'baby', 'help', 'problem', 'why', 'how'];
          parentingTerms.forEach(term => {
            if (queryLower.includes(term) && questionLower.includes(term)) {
              score += 10;
            }
          });
        }
        
        // 6. Recency boost for shorter, more specific questions
        if (questionLower.length < 50 && score > 30) {
          score += 10;
        }
        
        return { question, score };
      });

      // Filter, sort and return top suggestions
      return scoredQuestions
        .filter(item => item.score > 20) // Higher minimum threshold
        .sort((a, b) => b.score - a.score)
        .slice(0, 6) // Top 6 most relevant
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