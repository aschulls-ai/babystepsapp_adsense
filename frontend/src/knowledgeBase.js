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
      
      // Set different thresholds based on type - food research needs higher precision
      const minThreshold = type === 'food_research' ? 0.6 : 0.3; // 60% for food safety, 30% for others
      
      if (bestMatch && bestMatch.similarity >= minThreshold) {
        console.log(`✅ Found match in ${type} (${Math.round(bestMatch.similarity * 100)}% similarity): ${bestMatch.question.question}`);
        return bestMatch;
      } else {
        console.log(`⚠️ No good match found in ${type} (best: ${bestMatch ? Math.round(bestMatch.similarity * 100) : 0}%), threshold: ${Math.round(minThreshold * 100)}%, using fallback`);
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
      let similarity = this.calculateSimilarity(queryLower, queryWords, questionObj, babyAge);
      
      // Special handling for food research - boost exact food name matches
      if (context.type === 'food_research') {
        similarity = this.enhanceFoodSafetyMatching(queryLower, questionObj, similarity);
      }
      
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

  // Enhanced matching specifically for food safety queries
  enhanceFoodSafetyMatching(queryLower, questionObj, baseSimilarity) {
    const questionLower = questionObj.question.toLowerCase();
    const answerLower = (questionObj.answer || '').toLowerCase();
    
    // Extract food names from common query patterns
    const foodPatterns = [
      /is\s+(.+?)\s+safe/i,           // "is honey safe"
      /can\s+.*\s+eat\s+(.+?)[\s\?]/i, // "can baby eat eggs"
      /(.+?)\s+for\s+bab/i,           // "avocados for babies"
      /when\s+.*\s+(.+?)[\s\?]/i,     // "when can babies have nuts"
      /(.+?)\s+bab/i                  // "honey baby"
    ];
    
    let extractedFood = '';
    for (const pattern of foodPatterns) {
      const match = queryLower.match(pattern);
      if (match && match[1]) {
        extractedFood = match[1].trim();
        break;
      }
    }
    
    // If no pattern matched, try simple extraction
    if (!extractedFood) {
      const queryWords = queryLower.split(' ').filter(word => 
        !['is', 'are', 'can', 'safe', 'baby', 'babies', 'for', 'my', 'eat', 'have', 'when', 'the', 'a', 'an'].includes(word)
      );
      if (queryWords.length > 0) {
        extractedFood = queryWords[0];
      }
    }
    
    if (extractedFood) {
      // Check for exact food matches in question or answer
      const foodVariations = this.getFoodVariations(extractedFood);
      
      for (const foodVar of foodVariations) {
        if (questionLower.includes(foodVar) || answerLower.includes(foodVar)) {
          console.log(`🎯 Food safety match detected: "${foodVar}" in question about ${questionObj.question}`);
          return Math.min(baseSimilarity + 0.4, 1.0); // Significant boost for food matches
        }
      }
      
      // Check for partial food matches (e.g., "egg" matches "eggs")
      for (const foodVar of foodVariations) {
        const partial = questionLower.includes(foodVar.slice(0, -1)) || 
                       answerLower.includes(foodVar.slice(0, -1)) ||
                       questionLower.includes(foodVar + 's') ||
                       answerLower.includes(foodVar + 's');
        
        if (partial) {
          console.log(`🎯 Partial food safety match: "${foodVar}" partial match in ${questionObj.question}`);
          return Math.min(baseSimilarity + 0.25, 1.0); // Moderate boost for partial matches
        }
      }
    }
    
    return baseSimilarity;
  }

  // Generate food variations for better matching
  getFoodVariations(food) {
    const variations = [food];
    
    // Add plural/singular variations
    if (food.endsWith('s')) {
      variations.push(food.slice(0, -1)); // Remove 's'
    } else {
      variations.push(food + 's'); // Add 's'
    }
    
    // Add common food aliases
    const aliases = {
      'avocado': ['avocados'],
      'honey': ['honeys'],
      'egg': ['eggs'],
      'nut': ['nuts', 'peanut', 'peanuts'],
      'fish': ['salmon', 'tuna'],
      'strawberry': ['strawberries', 'berry', 'berries'],
      'grape': ['grapes'],
      'carrot': ['carrots'],
      'apple': ['apples'],
      'banana': ['bananas'],
      'peanut': ['peanuts', 'nut', 'nuts'],
      'shellfish': ['shrimp', 'crab', 'lobster'],
      'dairy': ['milk', 'cheese', 'yogurt'],
      'gluten': ['wheat', 'bread']
    };
    
    if (aliases[food]) {
      variations.push(...aliases[food]);
    }
    
    // Find reverse aliases
    Object.entries(aliases).forEach(([key, values]) => {
      if (values.includes(food)) {
        variations.push(key);
        variations.push(...values);
      }
    });
    
    return [...new Set(variations)]; // Remove duplicates
  }

  // Comprehensive similarity calculation for user's JSON format
  calculateSimilarity(queryLower, queryWords, questionObj, babyAge) {
    let similarity = 0;
    const weights = {
      exact: 1.0,          // Exact question match
      keywords: 0.8,       // Keyword match (higher weight for simpler structure)
      semantic: 0.6,       // Semantic similarity
      category: 0.4,       // Category match
      age: 0.5,           // Age appropriateness (important for baby-related content)
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

    // 5. Age appropriateness (parse age_range string like "6–9 months")
    if (questionObj.age_range && babyAge) {
      const ageScore = this.calculateAgeCompatibility(questionObj.age_range, babyAge);
      similarity += ageScore * weights.age;
    }

    // 6. Category bonus (if query contains category-related terms)
    if (questionObj.category) {
      const categoryTerms = {
        'Feeding': ['feed', 'feeding', 'eat', 'eating', 'milk', 'bottle', 'breast', 'formula', 'solid', 'food', 'meal', 'nutrition'],
        'Sleep': ['sleep', 'sleeping', 'nap', 'napping', 'bedtime', 'night', 'tired', 'rest', 'wake'],
        'Development': ['develop', 'development', 'milestone', 'growth', 'crawl', 'walk', 'talk', 'sit', 'roll', 'stand'],
        'Health': ['health', 'sick', 'fever', 'cough', 'doctor', 'medicine', 'symptom', 'illness', 'temperature'],
        'Safety': ['safe', 'safety', 'dangerous', 'danger', 'avoid', 'careful', 'protect', 'choke', 'allergy'],
        'Behavior': ['behavior', 'cry', 'crying', 'fussy', 'calm', 'soothe', 'tantrum', 'comfort', 'mood'],
        'Recipes': ['recipe', 'cook', 'prepare', 'meal', 'breakfast', 'lunch', 'dinner', 'ingredient', 'cooking'],
        'Nutrition': ['nutrition', 'vitamin', 'healthy', 'diet', 'nutrients', 'iron', 'calcium', 'protein'],
        'Bathing': ['bath', 'bathing', 'clean', 'wash', 'hygiene', 'soap', 'water', 'dry'],
        'Diaper': ['diaper', 'change', 'changing', 'wet', 'dirty', 'rash', 'clean'],
        'Toys': ['toy', 'toys', 'play', 'playing', 'game', 'activity', 'fun', 'entertainment']
      };

      const categoryWords = categoryTerms[questionObj.category] || [questionObj.category.toLowerCase()];
      const categoryMatch = categoryWords.some(term => queryLower.includes(term.toLowerCase()));
      if (categoryMatch) {
        similarity += weights.category;
      }
    }

    return Math.min(similarity, 1.0); // Cap at 1.0
  }

  // Parse age range and calculate compatibility with baby's age
  calculateAgeCompatibility(ageRangeStr, babyAge) {
    try {
      // Handle different age range formats: "6–9 months", "0-3 months", "12+ months", etc.
      const ageStr = ageRangeStr.toLowerCase();
      
      // Extract numbers from age range string
      const numbers = ageStr.match(/\d+/g);
      if (!numbers || numbers.length === 0) return 0;

      const nums = numbers.map(n => parseInt(n));
      
      // Handle different formats
      if (ageStr.includes('+')) {
        // "12+ months" format
        const minAge = nums[0];
        if (babyAge >= minAge) return 1.0;
        if (babyAge >= minAge - 2) return 0.7; // Close to range
        return 0;
      } else if (nums.length >= 2) {
        // "6–9 months" or "6-9 months" format
        const [minAge, maxAge] = [Math.min(nums[0], nums[1]), Math.max(nums[0], nums[1])];
        
        if (babyAge >= minAge && babyAge <= maxAge) {
          return 1.0; // Perfect match
        } else {
          // Partial score for near matches
          const distanceFromRange = Math.min(
            Math.abs(babyAge - minAge),
            Math.abs(babyAge - maxAge)
          );
          
          if (distanceFromRange <= 1) return 0.8; // Within 1 month
          if (distanceFromRange <= 2) return 0.6; // Within 2 months
          if (distanceFromRange <= 3) return 0.4; // Within 3 months
          return 0;
        }
      } else if (nums.length === 1) {
        // Single age like "6 months"
        const targetAge = nums[0];
        const ageDiff = Math.abs(babyAge - targetAge);
        
        if (ageDiff === 0) return 1.0;
        if (ageDiff <= 1) return 0.8;
        if (ageDiff <= 2) return 0.6;
        if (ageDiff <= 3) return 0.4;
        return 0;
      }
      
      return 0;
    } catch (error) {
      console.log('Error parsing age range:', ageRangeStr, error);
      return 0;
    }
  }

  // Extract meaningful keywords from query with food and parenting focus
  extractKeywords(text) {
    const stopWords = new Set([
      'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 
      'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
      'me', 'you', 'your', 'what', 'when', 'where', 'how', 'why', 'should', 'would', 'could'
    ]);

    // Extract base keywords
    let keywords = text
      .toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 2 && !stopWords.has(word))
      .filter(word => !/^\d+$/.test(word));

    // Add important context words that help with matching
    const importantWords = [];
    
    // Food safety context words
    if (text.toLowerCase().includes('safe')) importantWords.push('safe', 'safety');
    if (text.toLowerCase().includes('eat')) importantWords.push('eat', 'eating');
    if (text.toLowerCase().includes('feed')) importantWords.push('feed', 'feeding');
    if (text.toLowerCase().includes('baby')) importantWords.push('baby', 'babies');
    if (text.toLowerCase().includes('month')) importantWords.push('month', 'months', 'age');
    
    // Parenting context words  
    if (text.toLowerCase().includes('sleep')) importantWords.push('sleep', 'sleeping', 'nap');
    if (text.toLowerCase().includes('cry')) importantWords.push('cry', 'crying', 'fussy');
    if (text.toLowerCase().includes('milk')) importantWords.push('milk', 'breast', 'formula');
    
    // Extract food names more aggressively
    const foodPatterns = [
      /\b(avocado|avocados)\b/i,
      /\b(honey)\b/i,
      /\b(egg|eggs)\b/i,
      /\b(nut|nuts|peanut|peanuts)\b/i,
      /\b(fish|salmon|tuna)\b/i,
      /\b(strawberr(?:y|ies)|berr(?:y|ies))\b/i,
      /\b(grape|grapes)\b/i,
      /\b(apple|apples)\b/i,
      /\b(banana|bananas)\b/i,
      /\b(carrot|carrots)\b/i,
      /\b(dairy|milk|cheese|yogurt)\b/i
    ];
    
    foodPatterns.forEach(pattern => {
      const match = text.match(pattern);
      if (match) {
        importantWords.push(match[1].toLowerCase());
      }
    });

    return [...new Set([...keywords, ...importantWords])];
  }

  // Enhanced semantic similarity with better food and parenting term matching
  calculateSemanticSimilarity(query, questionObj) {
    const semanticGroups = {
      // Food safety and introduction
      food_safety: ['safe', 'safety', 'dangerous', 'danger', 'avoid', 'careful', 'protect', 'choke', 'allergy', 'allergic', 'reaction'],
      food_introduction: ['introduce', 'start', 'begin', 'first', 'new', 'try', 'give', 'offer'],
      food_timing: ['when', 'age', 'month', 'months', 'old', 'ready', 'appropriate'],
      
      // Specific foods (expanded)
      fruits: ['apple', 'apples', 'banana', 'bananas', 'strawberry', 'strawberries', 'berry', 'berries', 'grape', 'grapes', 'pear', 'pears', 'orange', 'oranges'],
      vegetables: ['avocado', 'avocados', 'carrot', 'carrots', 'sweet potato', 'potato', 'broccoli', 'peas', 'spinach', 'corn'],
      proteins: ['egg', 'eggs', 'fish', 'salmon', 'chicken', 'meat', 'beef', 'turkey', 'beans', 'lentils', 'tofu'],
      allergens: ['nut', 'nuts', 'peanut', 'peanuts', 'shellfish', 'dairy', 'milk', 'cheese', 'wheat', 'gluten', 'soy'],
      sweeteners: ['honey', 'sugar', 'syrup', 'sweet', 'sweetener'],
      
      // Feeding and eating
      feeding: ['feed', 'feeding', 'eat', 'eating', 'meal', 'meals', 'food', 'solid', 'solids', 'bite', 'chew'],
      breastfeeding: ['breast', 'breastfeed', 'breastfeeding', 'nursing', 'nurse', 'latch'],
      bottle_feeding: ['bottle', 'formula', 'milk'],
      eating_skills: ['finger', 'self', 'spoon', 'cup', 'drink', 'sip', 'swallow'],
      
      // Sleep and rest
      sleep: ['sleep', 'sleeping', 'nap', 'napping', 'bedtime', 'night', 'tired', 'wake', 'rest', 'drowsy'],
      sleep_training: ['train', 'training', 'routine', 'schedule', 'cry', 'soothe', 'comfort'],
      
      // Development and milestones
      development: ['develop', 'development', 'milestone', 'growth', 'crawl', 'walk', 'talk', 'sit', 'roll', 'stand'],
      motor_skills: ['grasp', 'grab', 'hold', 'reach', 'kick', 'move', 'coordinate'],
      
      // Health and wellness  
      health: ['health', 'sick', 'fever', 'cough', 'doctor', 'medicine', 'symptom', 'temperature', 'illness', 'well'],
      digestion: ['digest', 'stomach', 'tummy', 'gas', 'burp', 'spit', 'vomit', 'poop', 'constipat'],
      
      // Behavior and temperament
      behavior: ['behavior', 'cry', 'crying', 'fussy', 'calm', 'soothe', 'tantrum', 'comfort', 'mood', 'happy', 'sad'],
      
      // Care and hygiene
      care: ['diaper', 'change', 'bath', 'bathing', 'clean', 'wash', 'hygiene', 'soap', 'lotion'],
      
      // Cooking and preparation
      recipes: ['recipe', 'cook', 'cooking', 'prepare', 'ingredient', 'instructions', 'bake', 'steam', 'boil', 'mash'],
      meal_types: ['breakfast', 'lunch', 'dinner', 'snack', 'puree']
    };

    let matchCount = 0;
    let totalGroups = 0;

    // Build comprehensive searchable text
    let questionText = questionObj.question.toLowerCase();
    
    // Add category for context
    if (questionObj.category) {
      questionText += ' ' + questionObj.category.toLowerCase();
    }
    
    // Handle different answer formats
    if (Array.isArray(questionObj.answer)) {
      questionObj.answer.forEach(recipe => {
        if (recipe.name) questionText += ' ' + recipe.name.toLowerCase();
        if (recipe.ingredients && Array.isArray(recipe.ingredients)) {
          questionText += ' ' + recipe.ingredients.join(' ').toLowerCase();
        }
        if (recipe.instructions) questionText += ' ' + recipe.instructions.toLowerCase();
      });
    } else if (typeof questionObj.answer === 'string') {
      questionText += ' ' + questionObj.answer.toLowerCase();
    }

    // Calculate semantic overlap
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
      this.knowledgeBases[type] = newQuestions; // Direct array format
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
      if (!this.isLoaded[type] || !Array.isArray(this.knowledgeBases[type])) return false;

      // Get the next ID by finding the highest existing ID
      const maxId = this.knowledgeBases[type].length > 0 ? 
        Math.max(...this.knowledgeBases[type].map(q => q.id || 0)) : 0;

      const newQuestion = {
        id: maxId + 1,
        category: this.detectCategory(query, type),
        question: query.trim(),
        answer: answer
      };

      this.knowledgeBases[type].push(newQuestion);
      localStorage.setItem(`kb_${type}`, JSON.stringify(this.knowledgeBases[type]));

      console.log(`✅ Added new question to ${type} knowledge base: "${query}"`);
      return true;
    } catch (error) {
      console.log(`❌ Failed to add question to ${type} knowledge base:`, error.message);
      return false;
    }
  }

  // Category detection matching user's format
  detectCategory(query, type) {
    const queryLower = query.toLowerCase();
    
    // Common categories across all types
    if (queryLower.includes('feed') || queryLower.includes('eat') || queryLower.includes('milk') || queryLower.includes('bottle')) return 'Feeding';
    if (queryLower.includes('sleep') || queryLower.includes('nap') || queryLower.includes('bedtime')) return 'Sleep';
    if (queryLower.includes('develop') || queryLower.includes('milestone') || queryLower.includes('growth')) return 'Development';
    if (queryLower.includes('health') || queryLower.includes('sick') || queryLower.includes('fever')) return 'Health';
    if (queryLower.includes('safe') || queryLower.includes('danger') || queryLower.includes('avoid')) return 'Safety';
    if (queryLower.includes('cry') || queryLower.includes('fussy') || queryLower.includes('behavior')) return 'Behavior';
    
    // Type-specific categories
    if (type === 'meal_planner') {
      if (queryLower.includes('recipe') || queryLower.includes('cook') || queryLower.includes('prepare')) return 'Recipes';
      if (queryLower.includes('nutrition') || queryLower.includes('vitamin') || queryLower.includes('healthy')) return 'Nutrition';
    }
    
    if (type === 'food_research') {
      if (queryLower.includes('allerg') || queryLower.includes('reaction')) return 'Safety';
      if (queryLower.includes('nutrition') || queryLower.includes('vitamin')) return 'Nutrition';
    }

    return 'General';
  }

  // Get statistics about knowledge base
  getStats(type = null) {
    const stats = {};

    const types = type ? [type] : ['meal_planner', 'ai_assistant', 'food_research'];
    
    types.forEach(t => {
      const kb = this.knowledgeBases[t];
      stats[t] = {
        loaded: this.isLoaded[t],
        questionCount: Array.isArray(kb) ? kb.length : 0,
        categories: Array.isArray(kb) ? this.getCategoryStats(kb) : {}
      };
    });

    return type ? stats[type] : stats;
  }

  getCategoryStats(questions) {
    const categories = {};
    questions.forEach(q => {
      const cat = q.category || 'General';
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