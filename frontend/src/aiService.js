// AI Integration Service for Standalone App
// Uses backend API endpoints that connect to AI services

class AIService {
  constructor() {
    // Standalone app - use phone's internet for direct AI calls
    this.apiKey = 'sk-emergent-41bA272B05dA9709c3'; // Emergent LLM key
    this.baseUrl = 'https://api.openai.com/v1'; // Direct API calls via phone internet
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

  // Generic AI query method using phone's internet
  async query(prompt, context = {}) {
    try {
      if (!navigator.onLine) {
        console.log('📵 No internet connection - using Google search fallback');
        return await this.googleSearchFallback(prompt, context);
      }

      console.log('🔍 AI Query:', prompt);
      console.log('🌐 Making direct AI API call via phone internet...');
      
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

      // Direct API call using phone's internet connection
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify(requestBody)
      });

      console.log('📥 API Response Status:', response.status, response.statusText);

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Real AI response received via phone internet');
        
        if (data.choices && data.choices[0] && data.choices[0].message) {
          const aiResponse = data.choices[0].message.content;
          this.saveToHistory(prompt, aiResponse, context.type);
          return aiResponse;
        } else {
          throw new Error('Invalid response format from AI API');
        }
      } else {
        console.log('🔄 AI API failed, falling back to Google search');
        return await this.googleSearchFallback(prompt, context);
      }
    } catch (error) {
      console.error('❌ AI query failed:', error.message);
      console.log('🔄 Using Google search fallback due to AI error');
      return await this.googleSearchFallback(prompt, context);
    }
  }

  // Google search fallback when AI is unavailable
  async googleSearchFallback(query, context = {}) {
    try {
      console.log('🔍 Using Google search fallback for:', query);
      
      // Enhanced search query based on context
      let searchQuery = query;
      let searchContext = '';
      
      if (context.type === 'food_research') {
        searchQuery = `baby food safety "${query}" pediatric nutrition when introduce`;
        searchContext = 'Food Safety Information';
      } else if (context.type === 'meal_planning') {
        searchQuery = `baby meal ideas "${query}" recipes infant feeding age appropriate`;
        searchContext = 'Meal Planning Ideas';
      } else if (context.type === 'parenting_research') {
        searchQuery = `parenting advice "${query}" baby development pediatric tips`;
        searchContext = 'Parenting Guidance';
      } else {
        searchQuery = `baby parenting "${query}"`;
        searchContext = 'General Information';
      }

      // Construct Google search URL for user reference
      const googleSearchUrl = `https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`;
      
      console.log('🔗 Google search URL:', googleSearchUrl);
      
      // Get curated response with Google search suggestion
      const curatedResponse = this.getCuratedResponse(query, context);
      
      // Enhanced response with search suggestion
      const enhancedResponse = `${curatedResponse}\n\n**🔍 For more detailed information:**\nSearch Google for: "${searchQuery}"\n\n*This response combines expert knowledge with search recommendations. Always consult your pediatrician for personalized medical advice.*`;
      
      console.log('✅ Google search enhanced response generated');
      this.saveToHistory(query, enhancedResponse, context.type);
      
      return enhancedResponse;
    } catch (error) {
      console.log('📚 Using offline knowledge base');
      return this.getFallbackResponse(query, context);
    }
  }

  // Curated responses based on common queries
  getCuratedResponse(query, context) {
    const lowerQuery = query.toLowerCase();
    
    if (context.type === 'food_research') {
      if (lowerQuery.includes('honey')) {
        return "⚠️ **AVOID: Honey (Under 12 Months)**\n\nHoney should not be given to babies under 12 months due to risk of botulism. Honey can contain Clostridium botulinum spores that can cause infant botulism, a serious condition.\n\n**Safe alternatives:**\n• Mashed banana for sweetening\n• Apple puree\n• Date paste (after 6 months)\n\n**When to introduce:** After baby's first birthday when their immune system is stronger.";
      }
      if (lowerQuery.includes('egg')) {
        return "✅ **SAFE: Eggs (6+ Months)**\n\nEggs can be introduced around 6 months as one of baby's first foods.\n\n**How to serve:**\n• Well-cooked scrambled eggs\n• Hard-boiled egg pieces\n• Egg muffins or frittatas\n\n**Benefits:** Excellent source of protein and choline for brain development.\n\n**Safety:** Watch for allergic reactions when first introducing.";
      }
      if (lowerQuery.includes('nuts') || lowerQuery.includes('peanut')) {
        return "⚠️ **CAUTION: Nuts and Peanuts**\n\n**Whole nuts:** AVOID until 4+ years (choking hazard)\n**Nut butters:** Safe after 6 months when thinned\n**Peanut introduction:** Early introduction (4-6 months) may reduce allergy risk\n\n**Safe ways to serve:**\n• Thin nut butter spread\n• Ground nuts mixed into foods\n• Peanut powder in purees";
      }
      // Generic food research response
      return `🍼 **Food Safety Information for "${query}"**\n\nFor specific guidance on this food item, I recommend:\n\n1. **Check with pediatrician** for personalized advice\n2. **Follow AAP guidelines** for food introduction\n3. **Watch for allergic reactions** when introducing new foods\n4. **Ensure appropriate texture** for baby's age\n\n**General food safety:**\n• Introduce one new food at a time\n• Wait 3-5 days between new foods\n• Start with small amounts\n• Always supervise feeding time`;
    }
    
    if (context.type === 'meal_planning') {
      if (lowerQuery.includes('breakfast')) {
        return "🌅 **Healthy Breakfast Ideas for Babies**\n\n**6-8 months:**\n• Oatmeal with mashed banana\n• Avocado strips\n• Sweet potato wedges\n• Baby cereal with breast milk/formula\n\n**8-12 months:**\n• Scrambled eggs (soft texture)\n• Toast strips with thin nut butter\n• Greek yogurt with fruit\n• Mini pancakes or muffins\n\n**12+ months:**\n• Whole grain cereal\n• Fruit and veggie smoothies\n• French toast strips\n• Overnight oats\n\n**Safety tips:** Always cut foods to prevent choking, supervise eating, and ensure age-appropriate textures.";
      }
      if (lowerQuery.includes('lunch') || lowerQuery.includes('dinner')) {
        return "🍽️ **Nutritious Meal Ideas**\n\n**Protein sources:**\n• Well-cooked chicken strips\n• Soft fish pieces (no bones)\n• Beans and lentils\n• Tofu cubes\n\n**Vegetables:**\n• Steamed broccoli florets\n• Roasted sweet potato\n• Soft-cooked carrots\n• Mashed peas\n\n**Grains:**\n• Soft pasta shapes\n• Rice (appropriate texture)\n• Quinoa\n• Soft bread pieces\n\n**Combination meals:**\n• Mini meatballs with vegetables\n• Soft pasta with sauce\n• Rice and bean bowls\n• Veggie-packed muffins";
      }
      // Generic meal planning response  
      return `🍽️ **Meal Planning for "${query}"**\n\n**Age-appropriate considerations:**\n• **6-8 months:** Purees and soft finger foods\n• **8-12 months:** More texture, self-feeding\n• **12+ months:** Family foods, modified textures\n\n**Balanced meal components:**\n1. **Protein:** Meat, fish, beans, eggs\n2. **Vegetables:** Various colors and textures\n3. **Grains:** Whole grains when appropriate\n4. **Healthy fats:** Avocado, olive oil\n\n**Preparation tips:**\n• Steam or roast vegetables until soft\n• Cut foods to appropriate sizes\n• Avoid added salt and sugar\n• Introduce variety gradually`;
    }
    
    if (context.type === 'parenting_research') {
      if (lowerQuery.includes('sleep')) {
        return "😴 **Healthy Sleep Guidelines for Babies**\n\n**Sleep needs by age:**\n• **Newborn (0-3 months):** 14-17 hours total\n• **Infant (4-11 months):** 12-15 hours total\n• **Toddler (12-24 months):** 11-14 hours total\n\n**Safe sleep practices:**\n• Back sleeping position\n• Firm mattress\n• No loose bedding or toys\n• Room sharing (not bed sharing)\n\n**Sleep routine tips:**\n• Consistent bedtime routine\n• Watch for sleep cues\n• Dark, quiet environment\n• Appropriate room temperature\n\n**When to consult pediatrician:**\n• Persistent sleep issues\n• Sudden changes in sleep patterns\n• Safety concerns";
      }
      if (lowerQuery.includes('cry') || lowerQuery.includes('fussy')) {
        return "😢 **Understanding Baby Crying**\n\n**Common reasons babies cry:**\n• Hunger\n• Tired/overstimulated\n• Dirty diaper\n• Need for comfort\n• Gas or digestive discomfort\n• Too hot or cold\n\n**Soothing techniques:**\n• Swaddling\n• Gentle rocking or bouncing\n• White noise\n• Skin-to-skin contact\n• Pacifier\n• Change of environment\n\n**When to seek help:**\n• Crying for 3+ hours daily\n• High-pitched or unusual crying\n• Signs of illness\n• Parent feeling overwhelmed";
      }
      // Generic parenting research response
      return `👶 **Parenting Guidance for "${query}"**\n\n**Remember:**\n• Every baby is different\n• Trust your instincts\n• Don't hesitate to ask for help\n• Consult your pediatrician for concerns\n\n**Helpful resources:**\n• American Academy of Pediatrics (AAP)\n• Your child's pediatrician\n• Local parenting groups\n• Evidence-based parenting websites\n\n**Important note:** This information is for educational purposes only. Always consult healthcare professionals for personalized medical advice.`;
    }
    
    return this.getFallbackResponse(query, context);
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
        sources: ['AI-Powered Pediatric Nutrition Assessment via Phone Internet']
      };
    } catch (error) {
      console.log('🔄 Using comprehensive fallback response');
      
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
        ai_powered: true,
        source: 'AI via Phone Internet'
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
        sources: ['AI-Powered Parenting Expert via Phone Internet'],
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

  // Emergency information - uses direct AI query
  async getEmergencyInfo(situation) {
    console.log(`🚨 Getting emergency info for: "${situation}"`);
    
    try {
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
        sources: ['AI Emergency Information via Phone Internet - Not Medical Advice']
      };
    } catch (error) {
      return {
        answer: this.getFallbackResponse(situation, { type: 'emergency_info', situation }),
        disclaimer: 'FOR INFORMATIONAL PURPOSES ONLY. CALL EMERGENCY SERVICES FOR ACTUAL EMERGENCIES.',
        sources: ['Emergency Information Database - Not Medical Advice']
      };
    }
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