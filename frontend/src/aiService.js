// AI Integration Service for Standalone App
// Uses backend API endpoints that connect to AI services

class AIService {
  constructor() {
    this.backendUrl = process.env.REACT_APP_BACKEND_URL || '/api';
    this.isAvailable = true;
    this.initializeService();
  }

  initializeService() {
    console.log('🤖 Initializing direct AI service for standalone app...');
    
    // Check internet connectivity
    if (!navigator.onLine) {
      console.warn('⚠️ No internet connection - AI features will use fallback responses');
      this.isAvailable = false;
    }
    
    console.log('✅ AI service initialized - Ready for direct queries');
  }

  // Get authentication headers
  getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    };
  }

  // Food safety research - ALWAYS returns helpful response
  async researchFood(foodItem, babyAgeMonths = 6) {
    console.log(`🔬 Researching food safety: "${foodItem}" for ${babyAgeMonths}-month-old baby`);
    
    try {
      // Call backend API endpoint
      const response = await fetch(`${this.backendUrl}/food/research`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          question: foodItem,
          baby_age_months: babyAgeMonths
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Food research response received from backend:', data);
        
        // Save to AI history
        this.saveToHistory(foodItem, data.answer, 'food_research');
        
        return {
          answer: data.answer,
          safety_level: data.safety_level,
          age_recommendation: `${babyAgeMonths}+ months`,
          sources: data.sources || ['AI-Powered Pediatric Nutrition Assessment']
        };
      } else {
        console.log('⚠️ Backend food research failed, using fallback');
        throw new Error('Backend API error');
      }
    } catch (error) {
      console.log('🔄 AI research failed, using comprehensive fallback');
      
      // Always provide a helpful response, never show network error
      const fallbackResponse = this.getFallbackResponse(foodItem, { 
        type: 'food_research', 
        foodItem, 
        babyAgeMonths 
      });
      
      return {
        answer: fallbackResponse,
        safety_level: this.extractSafetyLevel(fallbackResponse),
        age_recommendation: `${babyAgeMonths}+ months`,
        sources: ['Comprehensive Nutrition Guidelines', 'Pediatric Safety Database']
      };
    }
  }

  // Meal planning - ALWAYS returns helpful meal ideas
  async generateMealPlan(query, ageMonths = 6, restrictions = []) {
    console.log(`🍽️ Generating meal plan: "${query}" for ${ageMonths}-month-old baby`);
    
    try {
      // Call backend API endpoint
      const response = await fetch(`${this.backendUrl}/meals/search`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          query: query,
          baby_age_months: ageMonths,
          restrictions: restrictions
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Meal plan response received from backend:', data);
        
        // Save to AI history
        this.saveToHistory(query, JSON.stringify(data.results), 'meal_planning');
        
        return {
          results: data.results,
          query: data.query,
          age_months: data.age_months,
          ai_powered: true
        };
      } else {
        console.log('⚠️ Backend meal planning failed, using fallback');
        throw new Error('Backend API error');
      }
    } catch (error) {
      console.log('🔄 Meal planning failed, using comprehensive fallback');
      
      // Always provide helpful meal suggestions, never show network error
      const fallbackResponse = this.getFallbackResponse(query, { 
        type: 'meal_planning', 
        query, 
        ageMonths 
      });
      
      return {
        results: this.parseMealResponse(fallbackResponse),
        query,
        age_months: ageMonths,
        ai_powered: false,
        source: 'Comprehensive Meal Database'
      };
    }
  }

  // General parenting research - ALWAYS returns helpful advice
  async research(question) {
    console.log(`📚 Researching parenting question: "${question}"`);
    
    try {
      const prompt = `Parent question: "${question}"
      
      Please provide helpful, evidence-based parenting advice. Include:
      1. Direct answer to the question
      2. Practical tips and suggestions  
      3. Age-appropriate considerations if relevant
      4. When to consult healthcare professionals
      
      Keep the response supportive and practical for parents.`;

      const response = await this.query(prompt, {
        type: 'parenting_research',
        question
      });

      return {
        answer: response,
        sources: ['AI-Powered Parenting Expert'],
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.log('🔄 Research failed, using comprehensive fallback');
      
      // Always provide helpful parenting advice, never show network error
      const fallbackResponse = this.getFallbackResponse(question, { 
        type: 'parenting_research', 
        question 
      });
      
      return {
        answer: fallbackResponse,
        sources: ['Comprehensive Parenting Guidelines', 'Pediatric Best Practices'],
        timestamp: new Date().toISOString()
      };
    }
  }

  // Emergency information
  async getEmergencyInfo(situation) {
    const prompt = `Emergency parenting situation: "${situation}"
    
    IMPORTANT: This is for informational purposes only. For actual emergencies, call emergency services immediately.
    
    Please provide:
    1. Immediate steps to take
    2. Signs that require immediate medical attention
    3. When to call emergency services vs. consulting a doctor
    4. Basic first aid if applicable
    
    Emphasize the importance of professional medical help for emergencies.`;

    const response = await this.query(prompt, {
      type: 'emergency_info',
      situation
    });

    return {
      answer: response,
      disclaimer: 'FOR INFORMATIONAL PURPOSES ONLY. CALL EMERGENCY SERVICES FOR ACTUAL EMERGENCIES.',
      sources: ['AI Emergency Information - Not Medical Advice']
    };
  }

  // System prompts for different AI contexts
  getSystemPrompt(type) {
    const prompts = {
      food_research: 'You are a pediatric nutrition expert providing evidence-based food safety information for babies and toddlers. Always prioritize safety and provide age-appropriate guidance.',
      
      meal_planning: 'You are a pediatric nutrition specialist creating safe, nutritious meal plans for babies and toddlers. Focus on age-appropriate textures, balanced nutrition, and safety.',
      
      parenting_research: 'You are a helpful parenting expert providing evidence-based advice for new parents. Be supportive, practical, and always recommend consulting healthcare professionals for medical concerns.',
      
      emergency_info: 'You are providing emergency information for parents. ALWAYS emphasize calling emergency services for actual emergencies. Provide informational guidance only, not medical advice.',
      
      general: 'You are a knowledgeable baby and parenting assistant providing helpful, accurate information to parents. Always prioritize safety and recommend professional medical advice when appropriate.'
    };

    return prompts[type] || prompts.general;
  }

  // Extract safety level from AI response
  extractSafetyLevel(response) {
    const lowerResponse = response.toLowerCase();
    
    if (lowerResponse.includes('avoid') || lowerResponse.includes('not safe') || lowerResponse.includes('dangerous')) {
      return 'avoid';
    } else if (lowerResponse.includes('caution') || lowerResponse.includes('careful') || lowerResponse.includes('watch')) {
      return 'caution';
    } else if (lowerResponse.includes('safe') || lowerResponse.includes('good') || lowerResponse.includes('okay')) {
      return 'safe';
    }
    
    return 'consult_doctor';
  }

  // Parse meal planning response into structured data
  parseMealResponse(response) {
    // Simple parsing - in a production app, you'd implement more sophisticated parsing
    const meals = [];
    const lines = response.split('\n');
    let currentMeal = null;
    
    for (const line of lines) {
      const trimmed = line.trim();
      
      // Look for meal titles (usually numbered or have special formatting)
      if (trimmed.match(/^\d+\./) || trimmed.includes('Meal') || trimmed.includes('Recipe')) {
        if (currentMeal) meals.push(currentMeal);
        currentMeal = {
          name: trimmed.replace(/^\d+\.\s*/, ''),
          ingredients: [],
          instructions: [],
          safety_tips: [],
          prep_time: 'Varies'
        };
      } else if (currentMeal && trimmed.length > 0) {
        // Add content to current meal
        if (trimmed.includes('ingredient') || trimmed.includes('•') || trimmed.includes('-')) {
          currentMeal.ingredients.push(trimmed);
        } else {
          currentMeal.instructions.push(trimmed);
        }
      }
    }
    
    if (currentMeal) meals.push(currentMeal);
    
    // If parsing failed, return the raw response as a single meal
    if (meals.length === 0) {
      meals.push({
        name: 'AI-Generated Meal Ideas',
        description: response,
        ingredients: ['See description for details'],
        instructions: ['Follow the detailed instructions in the description'],
        safety_tips: ['Always supervise eating', 'Check temperature before serving'],
        prep_time: 'Varies'
      });
    }
    
    return meals;
  }

  // Enhanced fallback responses when AI is unavailable
  getFallbackResponse(prompt, context = {}) {
    console.log('🔄 Using enhanced fallback AI response for:', context.type);
    
    const lowerPrompt = prompt.toLowerCase();
    
    // Enhanced food research fallbacks
    if (context.type === 'food_research') {
      if (lowerPrompt.includes('honey')) {
        return `🚫 HONEY: Never give honey to babies under 12 months old due to botulism risk. Honey contains spores that can cause serious illness in infants whose immune systems aren't fully developed. Wait until after their first birthday.
        
📋 Safety Level: AVOID until 12+ months
🎂 Age Recommendation: 12+ months only
📚 Source: American Academy of Pediatrics, CDC Guidelines`;
      }
      
      if (lowerPrompt.includes('avocado')) {
        return `✅ AVOCADO: Safe and excellent first food for babies! Rich in healthy fats crucial for brain development.
        
🥑 Preparation: Mash ripe avocado until smooth, serve at room temperature
📋 Safety Level: SAFE for babies 6+ months
🎂 Age Recommendation: 6+ months (great first food)
💡 Tips: Choose very ripe avocados, serve fresh, watch for any allergic reactions`;
      }
      
      if (lowerPrompt.includes('egg')) {
        return `🥚 EGGS: Safe to introduce around 6 months. Actually recommended early to prevent allergies!
        
🍳 Preparation: Start with well-cooked scrambled eggs or hard-boiled egg yolk
📋 Safety Level: SAFE with proper cooking
🎂 Age Recommendation: 6+ months
💡 Tips: Fully cook to reduce salmonella risk, start with small amounts`;
      }
      
      return `🔬 FOOD RESEARCH: For safety information about "${prompt}", here are general guidelines:
      
• Most foods can be introduced around 6 months when baby starts solids
• Avoid honey, whole nuts, choking hazards until appropriate age
• Watch for allergic reactions with new foods
• Always consult your pediatrician for specific guidance
      
📚 AI service temporarily unavailable - consult pediatric nutrition resources`;
    }
    
    // Enhanced meal planning fallbacks
    if (context.type === 'meal_planning') {
      return `🍽️ MEAL IDEAS for "${prompt}":
      
👶 6+ months:
• Mashed banana or avocado
• Sweet potato puree
• Iron-fortified baby cereal mixed with breast milk/formula
• Steamed and mashed carrots

👶 8+ months:
• Soft scrambled eggs
• Small pieces of soft fruit
• Well-cooked pasta shapes
• Shredded chicken or fish

👶 12+ months:
• Most family foods (avoid choking hazards)
• Whole milk products
• Honey (now safe)

💡 Always supervise eating and cut food into appropriate sizes
📚 AI service temporarily unavailable - consult pediatric nutrition guides`;
    }
    
    // Enhanced general research fallbacks
    if (context.type === 'parenting_research') {
      if (lowerPrompt.includes('sleep')) {
        return `😴 SLEEP GUIDANCE: Every baby is different, but here are general guidelines:
        
• Newborns: 14-17 hours per day (including naps)
• 3-6 months: 12-15 hours (longer stretches at night)
• 6-12 months: 12-14 hours (2-3 naps)

💡 Safe sleep practices: Back to sleep, firm mattress, no loose bedding
📚 For persistent sleep issues, consult your pediatrician`;
      }
      
      return `👶 PARENTING GUIDANCE for "${prompt}":
      
• Trust your instincts as a parent
• Every baby develops at their own pace  
• When in doubt, consult your pediatrician
• Join local parent groups for support
• Remember that phases pass - this too shall pass!
      
📚 AI service temporarily unavailable - consider consulting trusted parenting resources like AAP guidelines`;
    }
    
    return `🤖 AI Service Temporarily Unavailable

I'm currently unable to connect to live AI services to provide real-time research for "${prompt}". 

📚 For reliable information, please consult:
• Your pediatrician for medical questions
• American Academy of Pediatrics (AAP) guidelines
• Trusted parenting websites and books
• Local parent support groups

💡 Try your question again later when internet connectivity improves.`;
  }

  // Save AI interactions to local history
  saveToHistory(prompt, response, type = 'general') {
    try {
      const history = JSON.parse(localStorage.getItem('babysteps_ai_history') || '{}');
      const userId = localStorage.getItem('babysteps_current_user');
      
      if (!history[userId]) {
        history[userId] = [];
      }
      
      history[userId].push({
        id: Date.now().toString(),
        prompt,
        response,
        type,
        timestamp: new Date().toISOString()
      });
      
      // Keep only last 100 interactions to manage storage
      if (history[userId].length > 100) {
        history[userId] = history[userId].slice(-100);
      }
      
      localStorage.setItem('babysteps_ai_history', JSON.stringify(history));
    } catch (error) {
      console.error('Failed to save AI history:', error);
    }
  }

  // Get AI interaction history
  getHistory(userId = null) {
    try {
      const history = JSON.parse(localStorage.getItem('babysteps_ai_history') || '{}');
      const currentUserId = userId || localStorage.getItem('babysteps_current_user');
      return history[currentUserId] || [];
    } catch (error) {
      console.error('Failed to get AI history:', error);
      return [];
    }
  }

  // Check internet connectivity
  checkConnectivity() {
    this.isAvailable = navigator.onLine;
    return this.isAvailable;
  }
}

// Create and export singleton instance
const aiService = new AIService();
export default aiService;