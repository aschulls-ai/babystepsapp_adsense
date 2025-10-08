// Vercel API Route - Food Research
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  // Simple auth check - Accept demo tokens
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  // Validate demo tokens (base64 encoded JSON)
  try {
    const decoded = Buffer.from(token, 'base64').toString('utf8');
    const tokenData = JSON.parse(decoded);
    
    // Check if token is valid (demo tokens or test tokens)
    if (!tokenData.email || (!tokenData.email.includes('demo@babysteps.com') && !tokenData.email.includes('test@babysteps.com'))) {
      return res.status(401).json({ detail: 'Invalid token' });
    }
  } catch (error) {
    console.error('Token validation error:', error);
    return res.status(401).json({ detail: 'Invalid token format' });
  }

  const { question, baby_age_months } = req.body;

  if (!question) {
    return res.status(422).json({ detail: 'Question is required' });
  }

  // Comprehensive food safety responses with proper safety levels
  const mockResponses = {
    'honey': {
      answer: baby_age_months < 12 
        ? `**NEVER give honey to babies under 12 months old.** Honey can contain spores of Clostridium botulinum, which can cause infant botulism, a serious condition.\n\n**For your ${baby_age_months} month old baby:**\n• Wait until after 12 months to introduce honey\n• This includes raw honey, cooked honey, and foods containing honey\n• Use pureed fruits for natural sweetness instead\n\n**Why it's dangerous:** Young babies' digestive systems cannot handle botulism spores that may be present in honey.`
        : `**Honey is generally safe for babies over 12 months old.** Your ${baby_age_months} month old baby can have honey in moderation.\n\n**Safe introduction tips:**\n• Start with small amounts\n• Choose pasteurized honey when possible\n• Watch for any allergic reactions\n• Avoid giving large amounts as it's high in sugar\n\n**Remember:** Honey should supplement, not replace, nutritious foods.`,
      safety_level: baby_age_months < 12 ? 'avoid' : 'safe',
      age_recommendation: baby_age_months < 12 ? 'Wait until 12+ months' : 'Safe for current age',
      sources: ['AAP guidelines', 'FDA recommendations', 'Pediatric botulism prevention guidelines']
    },
    
    'strawberries': {
      answer: baby_age_months >= 6 
        ? `**Strawberries are generally safe for babies around ${baby_age_months} months old.** They're nutritious and most babies enjoy them!\n\n**Safe preparation:**\n• Wash thoroughly before serving\n• Remove stems and cut into small pieces (smaller than baby's thumbnail)\n• For younger babies: mash or cut into very small pieces\n• Start with small amounts to watch for reactions\n\n**Allergy considerations:**\n• Strawberries can cause allergic reactions in some babies\n• Watch for rash around mouth, hives, or digestive upset\n• Introduce gradually and one at a time`
        : `**Wait until around 6 months to introduce strawberries.** Your ${baby_age_months} month old baby should focus on breast milk or formula for now.\n\n**When to introduce (around 6 months):**\n• Start with single-ingredient purees first\n• Strawberries can be one of the first fruits to try\n• Always supervise and watch for allergic reactions\n\n**Current recommendations:** Focus on iron-rich foods and single-ingredient introductions when ready.`,
      safety_level: baby_age_months >= 6 ? 'safe' : 'caution',
      age_recommendation: baby_age_months >= 6 ? 'Appropriate for current age' : 'Wait until 6+ months',
      sources: ['Pediatric nutrition guidelines', 'Food allergy research', 'AAP feeding recommendations']
    },
    
    'eggs': {
      answer: baby_age_months >= 6
        ? `**Eggs are excellent for babies ${baby_age_months} months and older!** They're packed with protein and nutrients.\n\n**Safe preparation:**\n• Always cook eggs thoroughly (no runny parts)\n• Start with scrambled eggs or hard-boiled egg yolk\n• Cut into appropriate pieces for baby's age\n• Introduce egg whites and yolks together (recent research shows this may help prevent allergies)\n\n**Allergy considerations:**\n• Eggs are a common allergen - watch for reactions\n• Signs to watch: rash, vomiting, diarrhea, or breathing issues\n• If family history of allergies, consult pediatrician first`
        : `**Wait until around 6 months to introduce eggs.** Your ${baby_age_months} month old baby isn't ready for solid foods yet.\n\n**When ready (around 6 months):**\n• Eggs are actually one of the recommended early foods\n• Early introduction may help prevent egg allergies\n• Always cook thoroughly when you do introduce them\n\n**Current focus:** Breast milk or formula provides all nutrition needed right now.`,
      safety_level: baby_age_months >= 6 ? 'safe' : 'caution',
      age_recommendation: baby_age_months >= 6 ? 'Great choice for current age' : 'Wait until 6+ months',
      sources: ['NIAID allergy prevention guidelines', 'AAP nutrition recommendations', 'Recent egg allergy research']
    },
    
    'peanut': {
      answer: baby_age_months >= 6
        ? `**Peanut products can be introduced around ${baby_age_months} months, but preparation is crucial!**\n\n**NEVER give whole peanuts or chunky peanut butter** - choking hazard until age 4.\n\n**Safe ways to introduce:**\n• Smooth peanut butter thinned with breast milk/formula\n• Peanut butter spread very thinly on toast\n• Peanut powder mixed into purees\n• Puffed peanut snacks designed for babies\n\n**Important:** Early introduction (4-6 months) may actually help prevent peanut allergies. Consult pediatrician first, especially if family history of allergies.`
        : `**Consult your pediatrician about peanut introduction timing.** For babies under 6 months, focus on breast milk/formula.\n\n**Recent guidelines suggest:**\n• Early introduction (4-6 months) may prevent allergies\n• Especially important if high risk for allergies\n• Must be in safe, age-appropriate forms\n\n**Never safe:** Whole peanuts or chunky peanut butter (choking hazard until age 4)`,
      safety_level: baby_age_months >= 6 ? 'caution' : 'consult_doctor',
      age_recommendation: baby_age_months >= 6 ? 'Consult pediatrician first' : 'Discuss timing with pediatrician',
      sources: ['NIAID peanut allergy prevention guidelines', 'Learning Early About Peanut Allergy (LEAP) study', 'AAP recommendations']
    },
    
    'water': {
      answer: baby_age_months < 6
        ? `**Generally, babies under 6 months don't need water.** Your ${baby_age_months} month old baby gets all necessary hydration from breast milk or formula.\n\n**Why water isn't needed yet:**\n• Breast milk/formula provides perfect hydration\n• Water can interfere with nutrition\n• Risk of water intoxication in young babies\n\n**Exceptions (consult pediatrician):**\n• Very hot weather\n• Baby seems dehydrated\n• Doctor specifically recommends it`
        : baby_age_months < 12
        ? `**Small amounts of water are okay for your ${baby_age_months} month old baby.** But breast milk/formula should still be the main source of hydration.\n\n**Guidelines for ${baby_age_months} months:**\n• 2-4 oz of water per day is plenty\n• Offer water with meals\n• Don't replace milk feedings with water\n• Use clean, safe drinking water\n\n**Signs baby needs more fluids:** Dark urine, fewer wet diapers, lethargy`
        : `**Your ${baby_age_months} month old can drink water more freely now!** Water becomes more important as milk intake naturally decreases.\n\n**At ${baby_age_months} months:**\n• Offer water throughout the day\n• Continue breast milk or transition to whole milk\n• 4-6 oz of water per day is typical\n• Teach cup drinking skills\n\n**Always use:** Clean, safe drinking water appropriate for your area`,
      safety_level: baby_age_months < 6 ? 'caution' : 'safe',
      age_recommendation: baby_age_months < 6 ? 'Not needed until 6+ months' : 'Small amounts appropriate',
      sources: ['AAP hydration guidelines', 'WHO infant feeding recommendations', 'Pediatric nutrition standards']
    }
  };

  // Find relevant response
  let responseData = null;
  const questionLower = question.toLowerCase();
  
  // Check for specific food keywords
  for (const [keyword, data] of Object.entries(mockResponses)) {
    if (questionLower.includes(keyword)) {
      responseData = data;
      break;
    }
  }

  // Default response if no match found
  if (!responseData) {
    responseData = {
      answer: `**CONSULT PEDIATRICIAN** for personalized guidance about "${question}"\n\n**General guidelines for ${baby_age_months || 6} month old babies:**\n• Focus on introducing single ingredient foods one at a time\n• Watch carefully for allergic reactions\n• Ensure foods are properly prepared for age and developmental stage\n• Always supervise during meals\n• Cut foods appropriately to prevent choking\n\n**Safety reminders:**\n• Introduce new foods gradually\n• Wait 3-5 days between new foods\n• Trust your instincts - if something seems wrong, contact your pediatrician`,
      safety_level: 'consult_doctor',
      age_recommendation: 'Consult pediatrician for guidance',
      sources: ['General pediatric guidelines', 'AAP food safety recommendations', 'WHO infant feeding guidelines']
    };
  }

  // Add general safety reminder to all responses
  responseData.answer += '\n\n**⚠️ Important Safety Reminder:**\nThis information is for educational purposes only. Always consult your pediatrician before introducing new foods, especially if your baby has allergies or medical conditions. Every baby develops at their own pace.';

  res.status(200).json(responseData);
}