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
      'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with'
    ]);

    const textLower = text.toLowerCase();
    
    // Extract base keywords (keep important question words now)
    let keywords = textLower
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2 && !stopWords.has(word));

    // Add important context keywords based on patterns
    const contextKeywords = [];
    
    // Comprehensive food patterns with variations
    const foodPatterns = {
      'avocado': /\b(avocado|avocados)\b/i,
      'honey': /\b(honey|honeys)\b/i,
      'egg': /\b(egg|eggs)\b/i,
      'peanut': /\b(peanut|peanuts|nut|nuts)\b/i,
      'almond': /\b(almond|almonds)\b/i,
      'fish': /\b(fish|salmon|tuna|cod|seafood)\b/i,
      'strawberry': /\b(strawberr\w*|berr\w+)\b/i,
      'blueberry': /\b(blueberr\w*)\b/i,
      'grape': /\b(grape|grapes)\b/i,
      'banana': /\b(banana|bananas)\b/i,
      'apple': /\b(apple|apples)\b/i,
      'pear': /\b(pear|pears)\b/i,
      'orange': /\b(orange|oranges|citrus)\b/i,
      'peach': /\b(peach|peaches)\b/i,
      'mango': /\b(mango|mangos|mangoes)\b/i,
      'watermelon': /\b(watermelon)\b/i,
      'melon': /\b(melon)\b/i,
      'milk': /\b(milk|dairy)\b/i,
      'cheese': /\b(cheese)\b/i,
      'yogurt': /\b(yogurt|yoghurt)\b/i,
      'butter': /\b(butter)\b/i,
      'meat': /\b(meat|beef|pork)\b/i,
      'chicken': /\b(chicken|poultry)\b/i,
      'turkey': /\b(turkey)\b/i,
      'carrot': /\b(carrot|carrots)\b/i,
      'broccoli': /\b(broccoli)\b/i,
      'spinach': /\b(spinach)\b/i,
      'peas': /\b(pea|peas)\b/i,
      'corn': /\b(corn)\b/i,
      'potato': /\b(potato|potatoes)\b/i,
      'tomato': /\b(tomato|tomatoes)\b/i,
      'rice': /\b(rice)\b/i,
      'oat': /\b(oat|oats|oatmeal)\b/i,
      'bread': /\b(bread|toast)\b/i,
      'pasta': /\b(pasta|noodle|noodles)\b/i,
      'cereal': /\b(cereal)\b/i,
      'quinoa': /\b(quinoa)\b/i,
      'bean': /\b(bean|beans)\b/i,
      'lentil': /\b(lentil|lentils)\b/i,
      'tofu': /\b(tofu)\b/i,
      'formula': /\b(formula)\b/i,
      'water': /\b(water)\b/i,
      'juice': /\b(juice)\b/i
    };

    Object.entries(foodPatterns).forEach(([food, pattern]) => {
      if (pattern.test(text)) {
        contextKeywords.push(food);
      }
    });

    // Action/intent keywords that shouldn't be filtered
    if (/\b(can|safe|okay|ok)\b/i.test(text)) contextKeywords.push('safety');
    if (/\b(eat|eating|feed|feeding|give|serve)\b/i.test(text)) contextKeywords.push('eating');
    if (/\b(when|age|old|month|months)\b/i.test(text)) contextKeywords.push('timing');
    if (/\b(sleep|sleeping|nap|napping|bedtime)\b/i.test(text)) contextKeywords.push('sleep');
    if (/\b(cry|crying|fuss|fussy|upset)\b/i.test(text)) contextKeywords.push('behavior');
    if (/\b(milk|breast|breastfeed|bottle)\b/i.test(text)) contextKeywords.push('feeding');
    if (/\b(develop|development|milestone|growth)\b/i.test(text)) contextKeywords.push('development');
    if (/\b(recipe|meal|cook|prepare)\b/i.test(text)) contextKeywords.push('cooking');
    
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
      
      // Advanced scoring system with improved question variation matching
      const scoredQuestions = kb.map(question => {
        let score = 0;
        const questionLower = question.question.toLowerCase();
        let answerLower = '';
        
        // Handle both string and array answers
        if (typeof question.answer === 'string') {
          answerLower = question.answer.toLowerCase();
        } else if (Array.isArray(question.answer)) {
          // For recipes, search in names and ingredients
          answerLower = question.answer.map(recipe => 
            (recipe.name || '') + ' ' + (recipe.ingredients || []).join(' ')
          ).join(' ').toLowerCase();
        }
        
        const categoryLower = (question.category || '').toLowerCase();
        
        // 1. Exact phrase matching (highest priority)
        if (questionLower.includes(queryLower)) {
          score += 200;
        }
        
        // 2. Question structure variation matching
        // Match "can my baby eat X" with "can babies eat X" or "is X safe"
        const normalizedQuery = queryLower
          .replace(/\b(my|your|our|the)\b/gi, '')
          .replace(/\bbaby\b/gi, 'babies')
          .replace(/\bcan\b.*\beat\b/i, 'eat')
          .replace(/\bis\b.*\bsafe\b/i, 'safe')
          .trim();
        
        const normalizedQuestion = questionLower
          .replace(/\b(my|your|our|the)\b/gi, '')
          .replace(/\bbaby\b/gi, 'babies')
          .replace(/\bcan\b.*\beat\b/i, 'eat')
          .replace(/\bis\b.*\bsafe\b/i, 'safe')
          .trim();
        
        // Check if normalized versions match
        if (normalizedQuery.length > 5 && normalizedQuestion.includes(normalizedQuery)) {
          score += 150;
        }
        
        // 3. Food name exact matching (critical for food research)
        smartKeywords.forEach(keyword => {
          // Very high score for exact food name matches in question
          const foodNamePattern = new RegExp(`\\b${keyword}\\b`, 'i');
          if (foodNamePattern.test(questionLower)) {
            score += 100;
          }
          
          // High score for food name in answer
          if (foodNamePattern.test(answerLower)) {
            score += 60;
          }
          
          // Category matches
          if (foodNamePattern.test(categoryLower)) {
            score += 40;
          }
          
          // General keyword matches
          if (questionLower.includes(keyword)) {
            score += 30;
          }
          
          if (answerLower.includes(keyword)) {
            score += 15;
          }
          
          // Partial matches for longer keywords
          if (keyword.length > 4) {
            const partial = keyword.slice(0, -2);
            if (questionLower.includes(partial)) {
              score += 20;
            }
          }
        });
        
        // 4. Intent matching - understand what user is asking
        const intentPatterns = {
          safety: /\b(safe|safety|okay|ok|dangerous|danger|harm)\b/i,
          timing: /\b(when|age|old|month|months|start|introduce|begin)\b/i,
          preparation: /\b(how|prepare|cook|make|recipe|serve)\b/i,
          general: /\b(can|could|should|may|is|are)\b/i
        };
        
        Object.entries(intentPatterns).forEach(([intent, pattern]) => {
          if (pattern.test(queryLower) && pattern.test(questionLower)) {
            score += 25;
          }
        });
        
        // 5. Question word matching
        const questionWords = ['what', 'when', 'how', 'why', 'can', 'is', 'are', 'should'];
        questionWords.forEach(word => {
          if (queryLower.includes(word) && questionLower.includes(word)) {
            score += 10;
          }
        });
        
        // 6. Age relevance
        if (question.age_range && /\b\d+\b/.test(queryLower)) {
          score += 15;
        }
        
        // 7. Type-specific scoring
        if (knowledgeBaseType === 'food_research') {
          // Heavily boost food safety questions that match food items
          if (/\b(eat|food|feed|safe|allergy)\b/i.test(queryLower) && 
              /\b(eat|food|feed|safe|allergy)\b/i.test(questionLower)) {
            score += 30;
          }
        } else if (knowledgeBaseType === 'meal_planner') {
          // Boost recipe/meal questions
          if (/\b(recipe|meal|breakfast|lunch|dinner|snack|cook)\b/i.test(queryLower)) {
            score += 30;
          }
        } else if (knowledgeBaseType === 'ai_assistant') {
          // Boost parenting advice questions
          if (/\b(sleep|cry|feed|develop|milestone|help|problem)\b/i.test(queryLower)) {
            score += 20;
          }
        }
        
        return { question, score };
      });

      // Filter, sort and return top suggestions with lower threshold for better recall
      return scoredQuestions
        .filter(item => item.score > 15) // Lower threshold to catch more variations
        .sort((a, b) => b.score - a.score)
        .slice(0, 20) // Top 20 most relevant for better selection
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
    <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-2xl max-h-96 overflow-y-auto" style={{ zIndex: 99999, position: 'absolute' }}>
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