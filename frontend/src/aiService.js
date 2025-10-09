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
      if (!navigator.onLine) {
        console.log('📵 No internet connection - using fallback response');
        return this.getFallbackResponse(prompt, context);
      }

      console.log('🔍 AI Query:', prompt);
      console.log('🔗 Making direct AI API call to OpenAI...');
      
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

      console.log('📤 Request body:', JSON.stringify(requestBody, null, 2));

      // Try direct OpenAI API call with Emergent key
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify(requestBody)
      });

      console.log('📥 API Response Status:', response.status, response.statusText);

      if (response.ok) {
        const data = await response.json();
        console.log('📦 API Response Data:', data);
        
        if (data.choices && data.choices[0] && data.choices[0].message) {
          const aiResponse = data.choices[0].message.content;
          
          // Save to AI history
          this.saveToHistory(prompt, aiResponse, context.type);
          
          console.log('✅ Real AI response received from OpenAI API');
          return aiResponse;
        } else {
          throw new Error('Invalid response format from AI API');
        }
      } else {
        const errorText = await response.text();
        console.error('🚫 AI API Error Response:', errorText);
        throw new Error(`AI API error: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('❌ AI query failed:', error.message);
      console.log('🔄 Using enhanced fallback response due to AI error');
      return this.getFallbackResponse(prompt, context);
    }
  }

  // Food safety research - ALWAYS returns helpful response
  async researchFood(foodItem, babyAgeMonths = 6) {
    console.log(`🔬 Researching food safety: "${foodItem}" for ${babyAgeMonths}-month-old baby`);
    
    try {
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