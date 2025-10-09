// Direct AI Integration Service for Standalone App
// Uses device internet connection for AI responses

class AIService {
  constructor() {
    this.apiKey = 'sk-emergent-41bA272B05dA9709c3'; // Emergent LLM key
    this.baseUrl = 'https://api.openai.com/v1'; // Direct OpenAI API
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

  // Generic AI query method
  async query(prompt, context = {}) {
    try {
      if (!this.isAvailable || !navigator.onLine) {
        return this.getFallbackResponse(prompt, context);
      }

      console.log('🔍 AI Query:', prompt);

      // Use direct API call to OpenAI through Emergent LLM key
      console.log('🔗 Making direct AI API call...');
      
      const requestBody = {
        model: 'gpt-4o-mini',
        messages: [
          {
            role: 'system',
            content: this.getSystemPrompt(context.type || 'general')
          },
          {
            role: 'user', 
            content: prompt
          }
        ],
        max_tokens: 500,
        temperature: 0.7
      };

      // Try direct OpenAI API call with Emergent key
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify(requestBody)
      });

      if (response.ok) {
        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        
        // Save to AI history
        this.saveToHistory(prompt, aiResponse, context.type);
        
        console.log('✅ AI response received');
        return aiResponse;
      } else {
        throw new Error(`AI API error: ${response.status}`);
      }
    } catch (error) {
      console.error('❌ AI query failed:', error);
      return this.getFallbackResponse(prompt, context);
    }
  }

  // Food safety research
  async researchFood(foodItem, babyAgeMonths = 6) {
    const prompt = `Is "${foodItem}" safe for a ${babyAgeMonths}-month-old baby? Please provide:
    1. Safety assessment (safe/caution/avoid)
    2. Recommended age for introduction
    3. Preparation tips
    4. Potential risks or allergies
    5. Nutritional benefits
    
    Keep the response practical and parent-friendly.`;

    const response = await this.query(prompt, { 
      type: 'food_research',
      foodItem,
      babyAgeMonths 
    });

    return {
      answer: response,
      safety_level: this.extractSafetyLevel(response),
      age_recommendation: `${babyAgeMonths}+ months`,
      sources: ['AI-Powered Pediatric Nutrition Assessment']
    };
  }

  // Meal planning
  async generateMealPlan(query, ageMonths = 6, restrictions = []) {
    const prompt = `Create meal ideas for: "${query}" suitable for a ${ageMonths}-month-old baby.
    ${restrictions.length > 0 ? `Dietary restrictions: ${restrictions.join(', ')}` : ''}
    
    Please provide:
    1. 3-5 specific meal suggestions
    2. Ingredients for each meal
    3. Step-by-step preparation instructions
    4. Age appropriateness and safety tips
    5. Estimated preparation time
    
    Focus on nutrition, safety, and development-appropriate textures.`;

    const response = await this.query(prompt, {
      type: 'meal_planning',
      query,
      ageMonths,
      restrictions
    });

    return {
      results: this.parseMealResponse(response),
      query,
      age_months: ageMonths,
      ai_powered: true
    };
  }

  // General parenting research
  async research(question) {
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

  // Fallback responses when AI is unavailable
  getFallbackResponse(prompt, context = {}) {
    console.log('🔄 Using fallback AI response');
    
    const fallbacks = {
      food_research: `I'm unable to access live AI services right now. For food safety information about "${prompt}", please consult your pediatrician or refer to trusted pediatric nutrition resources like the American Academy of Pediatrics guidelines.`,
      
      meal_planning: `I'm unable to access live AI services right now. For meal planning ideas, consider age-appropriate options like mashed fruits and vegetables for babies 6+ months. Always consult your pediatrician for specific dietary guidance.`,
      
      parenting_research: `I'm unable to access live AI services right now. For parenting questions, please consult your pediatrician, local parenting resources, or trusted parenting websites like the American Academy of Pediatrics.`,
      
      general: `I'm unable to access live AI services right now. For important parenting and baby care questions, please consult your healthcare provider for personalized advice.`
    };
    
    return fallbacks[context.type] || fallbacks.general;
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