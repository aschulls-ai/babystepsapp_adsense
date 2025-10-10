// Knowledge Base Service for Baby Steps AI Search Engines
// Handles JSON-based preset answers for Meal Planner, AI Assistant, and Food Research

class KnowledgeBaseService {
  constructor() {
    this.knowledgeBases = {
      meal_planner: null,
      ai_assistant: null,
      food_research: null
    };
    this.isLoaded = {
      meal_planner: false,
      ai_assistant: false,
      food_research: false
    };
    this.initializeKnowledgeBase();
  }

  async initializeKnowledgeBase() {
    console.log('🔄 Initializing Knowledge Base Service...');
    
    try {
      // Load all three knowledge bases
      await this.loadKnowledgeBase('meal_planner');
      await this.loadKnowledgeBase('ai_assistant');
      await this.loadKnowledgeBase('food_research');
      
      console.log('✅ Knowledge Base Service initialized successfully');
    } catch (error) {
      console.log('⚠️ Knowledge Base initialization failed, will use fallback AI:', error.message);
    }
  }

  async loadKnowledgeBase(type) {
    try {
      // Try to load from public folder first, then from local storage cache
      const response = await fetch(`/knowledge-base/${type}.json`);
      
      if (response.ok) {
        const data = await response.json();
        this.knowledgeBases[type] = data;
        this.isLoaded[type] = true;
        console.log(`✅ Loaded ${type} knowledge base: ${Array.isArray(data) ? data.length : 0} questions`);
        
        // Cache in localStorage for offline access
        localStorage.setItem(`kb_${type}`, JSON.stringify(data));
      } else {
        // Try loading from localStorage cache
        await this.loadFromCache(type);
      }
    } catch (error) {
      console.log(`⚠️ Failed to load ${type} knowledge base from server, trying cache...`);
      await this.loadFromCache(type);
    }
  }

  async loadFromCache(type) {
    try {
      const cachedData = localStorage.getItem(`kb_${type}`);
      if (cachedData) {
        this.knowledgeBases[type] = JSON.parse(cachedData);
        this.isLoaded[type] = true;
        console.log(`✅ Loaded ${type} from cache`);
      } else {
        console.log(`⚠️ No cache found for ${type}`);
      }
    } catch (error) {
      console.log(`❌ Failed to load ${type} from cache:`, error.message);
    }
  }

  // Main search function - finds the best matching question
  searchKnowledgeBase(query, type, context = {}) {
    try {
      if (!this.isLoaded[type] || !this.knowledgeBases[type]) {
        console.log(`⚠️ ${type} knowledge base not loaded, using fallback`);
        return null;
      }

      const questions = Array.isArray(this.knowledgeBases[type]) ? this.knowledgeBases[type] : [];
      
      if (questions.length === 0) {
        console.log(`⚠️ No questions found in ${type} knowledge base`);
        return null;
      }

      console.log(`🔍 Searching ${questions.length} questions in ${type} knowledge base for: "${query}"`);

      // Find the best match
      const bestMatch = this.findBestMatch(query, questions, context);
      
      if (bestMatch && bestMatch.similarity >= 0.3) { // 30% minimum similarity threshold
        console.log(`✅ Found match in ${type} (${Math.round(bestMatch.similarity * 100)}% similarity): ${bestMatch.question.question}`);
        return bestMatch;
      } else {
        console.log(`⚠️ No good match found in ${type} (best: ${bestMatch ? Math.round(bestMatch.similarity * 100) : 0}%), using fallback`);
        return null;
      }
    } catch (error) {
      console.log(`❌ Error searching ${type} knowledge base:`, error.message);
      return null;
    }
  }

  // Advanced matching algorithm with multiple scoring factors
  findBestMatch(query, questions, context = {}) {
    const queryLower = query.toLowerCase();
    const queryWords = this.extractKeywords(queryLower);
    const babyAge = context.babyAgeMonths || context.ageMonths || 12;

    let bestMatch = null;
    let bestSimilarity = 0;

    questions.forEach(questionObj => {
      const similarity = this.calculateSimilarity(queryLower, queryWords, questionObj, babyAge);
      
      if (similarity > bestSimilarity) {
        bestSimilarity = similarity;
        bestMatch = {
          question: questionObj,
          similarity: similarity,
          matchType: this.getMatchType(similarity)
        };
      }
    });

    return bestMatch;
  }

  // Comprehensive similarity calculation for user's JSON format
  calculateSimilarity(queryLower, queryWords, questionObj, babyAge) {
    let similarity = 0;
    const weights = {
      exact: 1.0,          // Exact question match
      keywords: 0.8,       // Keyword match (higher weight for simpler structure)
      semantic: 0.6,       // Semantic similarity
      category: 0.4,       // Category match
      partial: 0.3         // Partial question match
    };

    // 1. Exact question match
    if (queryLower === questionObj.question.toLowerCase()) {
      similarity += weights.exact;
    }

    // 2. Partial question match (contains most of the query)
    const questionLower = questionObj.question.toLowerCase();
    const queryInQuestion = queryWords.filter(word => questionLower.includes(word)).length;
    const questionWordsInQuery = this.extractKeywords(questionLower).filter(word => queryLower.includes(word)).length;
    
    const partialScore = Math.max(
      queryInQuestion / Math.max(queryWords.length, 1),
      questionWordsInQuery / Math.max(this.extractKeywords(questionLower).length, 1)
    );
    similarity += partialScore * weights.partial;

    // 3. Keyword matching from question text
    const questionKeywords = this.extractKeywords(questionLower);
    const keywordMatches = queryWords.filter(word => 
      questionKeywords.some(keyword => 
        keyword.includes(word) || word.includes(keyword) || this.areSimilar(word, keyword)
      )
    ).length;

    const keywordScore = Math.min(keywordMatches / Math.max(queryWords.length, 1), 1.0);
    similarity += keywordScore * weights.keywords;

    // 4. Semantic similarity
    const semanticScore = this.calculateSemanticSimilarity(queryLower, questionObj);
    similarity += semanticScore * weights.semantic;

    // 5. Category bonus (if query contains category-related terms)
    if (questionObj.category) {
      const categoryTerms = {
        'Feeding': ['feed', 'feeding', 'eat', 'eating', 'milk', 'bottle', 'breast', 'formula', 'solid', 'food'],
        'Sleep': ['sleep', 'sleeping', 'nap', 'napping', 'bedtime', 'night', 'tired'],
        'Development': ['develop', 'development', 'milestone', 'growth', 'crawl', 'walk', 'talk', 'sit'],
        'Health': ['health', 'sick', 'fever', 'cough', 'doctor', 'medicine', 'symptom'],
        'Safety': ['safe', 'safety', 'dangerous', 'danger', 'avoid', 'careful', 'protect'],
        'Behavior': ['behavior', 'cry', 'crying', 'fussy', 'calm', 'soothe', 'tantrum'],
        'Recipes': ['recipe', 'cook', 'prepare', 'meal', 'breakfast', 'lunch', 'dinner', 'ingredient'],
        'Nutrition': ['nutrition', 'vitamin', 'healthy', 'diet', 'nutrients', 'iron', 'calcium']
      };

      const categoryWords = categoryTerms[questionObj.category] || [questionObj.category.toLowerCase()];
      const categoryMatch = categoryWords.some(term => queryLower.includes(term.toLowerCase()));
      if (categoryMatch) {
        similarity += weights.category;
      }
    }

    return Math.min(similarity, 1.0); // Cap at 1.0
  }

  // Extract meaningful keywords from query
  extractKeywords(text) {
    const stopWords = new Set([
      'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
      'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
      'can', 'my', 'i', 'me', 'you', 'your', 'what', 'when', 'where', 'how', 'why'
    ]);

    return text
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2 && !stopWords.has(word))
      .filter(word => !/^\d+$/.test(word)); // Remove pure numbers
  }

  // Semantic similarity for user's simpler JSON format
  calculateSemanticSimilarity(query, questionObj) {
    const semanticGroups = {
      feeding: ['feed', 'feeding', 'eat', 'eating', 'milk', 'bottle', 'breast', 'formula', 'solid', 'food', 'burp', 'hungry'],
      sleep: ['sleep', 'sleeping', 'nap', 'napping', 'bedtime', 'night', 'tired', 'wake', 'rest'],
      development: ['develop', 'development', 'milestone', 'growth', 'crawl', 'walk', 'talk', 'sit', 'roll', 'month', 'age'],
      health: ['health', 'sick', 'fever', 'cough', 'doctor', 'medicine', 'symptom', 'temperature', 'illness'],
      safety: ['safe', 'safety', 'dangerous', 'danger', 'avoid', 'careful', 'protect', 'choke', 'allergy'],
      behavior: ['behavior', 'cry', 'crying', 'fussy', 'calm', 'soothe', 'tantrum', 'comfort'],
      nutrition: ['nutrition', 'vitamin', 'healthy', 'diet', 'nutrients', 'iron', 'calcium', 'recipe', 'meal'],
      care: ['diaper', 'bath', 'bathing', 'clean', 'hygiene', 'care', 'routine', 'schedule']
    };

    let matchCount = 0;
    let totalGroups = 0;

    const questionText = questionObj.question.toLowerCase() + ' ' + (questionObj.answer?.toLowerCase() || '');

    Object.values(semanticGroups).forEach(group => {
      const queryHasGroup = group.some(term => query.includes(term));
      const questionHasGroup = group.some(term => questionText.includes(term));

      if (queryHasGroup || questionHasGroup) {
        totalGroups++;
        if (queryHasGroup && questionHasGroup) {
          matchCount++;
        }
      }
    });

    return totalGroups > 0 ? matchCount / totalGroups : 0;
  }

  // Check if two words are similar (simple fuzzy matching)
  areSimilar(word1, word2) {
    if (Math.abs(word1.length - word2.length) > 2) return false;
    
    // Check for common variations
    const variations = [
      [word1, word2],
      [word1 + 's', word2], [word1, word2 + 's'],
      [word1 + 'ing', word2], [word1, word2 + 'ing'],
      [word1.slice(0, -1), word2], [word1, word2.slice(0, -1)]
    ];

    return variations.some(([a, b]) => a === b);
  }

  // Determine match type for logging
  getMatchType(similarity) {
    if (similarity >= 0.8) return 'excellent';
    if (similarity >= 0.6) return 'good';
    if (similarity >= 0.4) return 'fair';
    if (similarity >= 0.3) return 'poor';
    return 'no_match';
  }

  // Update knowledge base (for admin functionality)
  async updateKnowledgeBase(type, newQuestions) {
    try {
      this.knowledgeBases[type] = { [`${type}_questions`]: newQuestions };
      localStorage.setItem(`kb_${type}`, JSON.stringify(this.knowledgeBases[type]));
      this.isLoaded[type] = true;
      
      console.log(`✅ Updated ${type} knowledge base with ${newQuestions.length} questions`);
      return true;
    } catch (error) {
      console.log(`❌ Failed to update ${type} knowledge base:`, error.message);
      return false;
    }
  }

  // Add new question to knowledge base (learning from AI responses)
  async addQuestionToKnowledgeBase(type, query, answer, context = {}) {
    try {
      if (!this.isLoaded[type]) return false;

      const newQuestion = {
        id: `${type}_${Date.now()}`,
        question: query.toLowerCase(),
        keywords: this.extractKeywords(query.toLowerCase()),
        category: this.detectCategory(query, type),
        age_range: context.babyAgeMonths ? [context.babyAgeMonths - 2, context.babyAgeMonths + 2] : [6, 24],
        answer: answer,
        tags: ["auto-generated"],
        difficulty: "moderate",
        created_at: new Date().toISOString()
      };

      const questionsKey = `${type}_questions`;
      if (!this.knowledgeBases[type][questionsKey]) {
        this.knowledgeBases[type][questionsKey] = [];
      }

      this.knowledgeBases[type][questionsKey].push(newQuestion);
      localStorage.setItem(`kb_${type}`, JSON.stringify(this.knowledgeBases[type]));

      console.log(`✅ Added new question to ${type} knowledge base: "${query}"`);
      return true;
    } catch (error) {
      console.log(`❌ Failed to add question to ${type} knowledge base:`, error.message);
      return false;
    }
  }

  // Simple category detection
  detectCategory(query, type) {
    const queryLower = query.toLowerCase();
    
    if (type === 'meal_planner') {
      if (queryLower.includes('breakfast') || queryLower.includes('morning')) return 'breakfast';
      if (queryLower.includes('lunch') || queryLower.includes('midday')) return 'lunch';
      if (queryLower.includes('dinner') || queryLower.includes('evening')) return 'dinner';
      if (queryLower.includes('snack') || queryLower.includes('finger')) return 'snack';
    } else if (type === 'food_research') {
      if (queryLower.includes('safe') || queryLower.includes('danger')) return 'safety';
      if (queryLower.includes('allerg') || queryLower.includes('reaction')) return 'allergy';
      if (queryLower.includes('nutrition') || queryLower.includes('vitamin')) return 'nutrition';
    } else if (type === 'ai_assistant') {
      if (queryLower.includes('sleep') || queryLower.includes('nap')) return 'sleep';
      if (queryLower.includes('develop') || queryLower.includes('milestone')) return 'development';
      if (queryLower.includes('cry') || queryLower.includes('fussy')) return 'behavior';
    }

    return 'general';
  }

  // Get statistics about knowledge base
  getStats(type = null) {
    const stats = {};

    const types = type ? [type] : ['meal_planner', 'ai_assistant', 'food_research'];
    
    types.forEach(t => {
      const kb = this.knowledgeBases[t];
      stats[t] = {
        loaded: this.isLoaded[t],
        questionCount: kb ? (kb[`${t}_questions`] || []).length : 0,
        categories: kb ? this.getCategoryStats(kb[`${t}_questions`] || []) : {}
      };
    });

    return type ? stats[type] : stats;
  }

  getCategoryStats(questions) {
    const categories = {};
    questions.forEach(q => {
      const cat = q.category || 'general';
      categories[cat] = (categories[cat] || 0) + 1;
    });
    return categories;
  }

  // Check if knowledge base is ready
  isReady(type = null) {
    if (type) {
      return this.isLoaded[type];
    }
    return Object.values(this.isLoaded).some(loaded => loaded);
  }
}

// Create and export singleton instance
const knowledgeBaseService = new KnowledgeBaseService();
export default knowledgeBaseService;