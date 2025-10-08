// Vercel API Route - General Research
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

  const { question } = req.body;

  if (!question) {
    return res.status(422).json({ detail: 'Question is required' });
  }

  // Comprehensive responses for common parenting and food safety questions
  const mockResponses = {
    'sleep': 'Newborns typically sleep 14-17 hours per day, but this varies greatly. Establishing a bedtime routine around 3-4 months can help. Safe sleep practices include: back sleeping, firm mattress, no loose bedding, and room-sharing (but not bed-sharing) for the first 6 months.',
    
    'feeding': 'Breastfeeding is recommended exclusively for the first 6 months. Formula feeding is also nutritionally complete. Signs of hunger include rooting, sucking motions, and fussiness. Signs of fullness include turning away from bottle/breast and closing mouth.',
    
    'development': 'Every baby develops at their own pace. Typical milestones include: 2 months - social smiles, 4-6 months - rolling over, 6-9 months - sitting, 9-12 months - crawling/walking, 12+ months - first words. Consult your pediatrician if you have concerns.',
    
    'crying': 'Babies cry for many reasons: hunger, tiredness, overstimulation, dirty diaper, or need for comfort. The "Period of PURPLE Crying" (peak fussiness) often occurs between 2-5 months. Try the 5 S\'s: Swaddle, Side position, Shush, Swing, Suck.',
    
    'diaper': 'Newborns typically have 6-8 wet diapers per day and frequent bowel movements. Breastfed babies may have seedy, yellow stools, while formula-fed babies have firmer, tan-colored stools. Always clean from front to back and allow air-drying time.',
    
    // Food Safety Responses
    'strawberries': '**CONSULT PEDIATRICIAN**\n\nStrawberries are generally safe for infants around 9 months old. When introducing strawberries:\n\n• **Age recommendation:** Around 9 months\n• **Introduction strategy:** Focus on single-ingredient foods, watch for reactions\n• **Preparation:** Cut into small pieces or mash for younger babies\n• **Allergy watch:** Strawberries can cause allergic reactions in some babies\n\n**Safety Reminder:**\n• Always supervise your baby during meals\n• Cut foods appropriately to prevent choking\n• Introduce new foods gradually while watching for allergic reactions\n\n*Sources: General pediatric guidelines, Food safety recommendations*',
    
    'honey': '**CONSULT PEDIATRICIAN**\n\n**NEVER give honey to babies under 12 months old.** Honey can contain spores of Clostridium botulinum, which can cause infant botulism, a serious condition.\n\n• **Safe age:** After 12 months\n• **Why dangerous:** Risk of infant botulism\n• **Includes:** Raw honey, cooked honey, and foods containing honey\n• **Alternative:** Use pureed fruits for sweetness\n\n**Safety Reminder:**\n• Always check ingredient labels for honey\n• This includes baked goods and cereals\n• Consult your pediatrician about sweetener alternatives\n\n*Sources: AAP guidelines, FDA recommendations*',
    
    'eggs': '**CONSULT PEDIATRICIAN**\n\nEggs can be introduced around 6 months old and are an excellent source of protein and nutrients.\n\n• **Age recommendation:** Around 6 months\n• **Preparation:** Fully cooked (no runny yolks or whites)\n• **Start with:** Small amounts of scrambled or hard-boiled egg\n• **Allergy considerations:** Eggs are a common allergen - watch for reactions\n\n**Safety Reminder:**\n• Always cook eggs thoroughly\n• Start with small amounts\n• Watch for signs of allergic reactions (rash, vomiting, diarrhea)\n• Store eggs properly and check expiration dates\n\n*Sources: General pediatric guidelines, Food allergy recommendations*',
    
    'avocado': '**CONSULT PEDIATRICIAN**\n\nAvocados are excellent first foods for babies and are generally safe from 6 months old.\n\n• **Age recommendation:** 6+ months\n• **Benefits:** Rich in healthy fats, fiber, and vitamins\n• **Preparation:** Mash well or cut into soft finger-food pieces\n• **Low allergy risk:** Avocados are considered low-allergen foods\n\n**Safety Reminder:**\n• Choose ripe, soft avocados\n• Remove pit and skin completely\n• Cut into appropriate sizes to prevent choking\n• Supervise eating and watch for any reactions\n\n*Sources: Pediatric nutrition guidelines*',
    
    'water': '**CONSULT PEDIATRICIAN**\n\nWater introduction depends on your baby\'s age and feeding method.\n\n• **0-6 months:** Generally not needed if breastfeeding or formula feeding\n• **6+ months:** Small amounts (2-4 oz) can be offered with meals\n• **12+ months:** Can drink water more freely\n• **Hot weather:** May need additional water - consult pediatrician\n\n**Safety Reminder:**\n• Use clean, safe drinking water\n• Don\'t replace breast milk or formula with water\n• Watch for signs of water intoxication in young babies\n• Consult your pediatrician about your baby\'s specific needs\n\n*Sources: AAP hydration guidelines*',
    
    'peanut butter': '**CONSULT PEDIATRICIAN**\n\nPeanut butter can be introduced early but requires careful preparation due to choking risk.\n\n• **Age recommendation:** 6+ months (consult pediatrician first)\n• **Preparation:** Thin with breast milk/formula or spread thinly on toast\n• **NEVER:** Give chunky peanut butter or whole peanuts to babies/toddlers\n• **Allergy considerations:** Early introduction may help prevent peanut allergies\n\n**Safety Reminder:**\n• Always thin peanut butter to prevent choking\n• Watch carefully for allergic reactions\n• Avoid if family history of severe peanut allergies\n• Choose smooth, natural peanut butter without added sugars\n\n*Sources: NIAID peanut allergy prevention guidelines*',
    
    'tummy time': 'Start tummy time from day one, beginning with 3-5 minutes several times per day. This helps develop neck and shoulder muscles and prevents flat spots on the head. Always supervise tummy time and stop if baby becomes fussy.',
    
    'vaccination': 'Vaccines are safe and important for protecting your baby from serious diseases. The CDC provides a recommended schedule starting at 2 months. Side effects are usually mild (fussiness, low fever). Discuss any concerns with your pediatrician.',
    
    'teething': 'Teething typically begins around 6 months but can start earlier or later. Signs include drooling, wanting to chew on things, irritability, and slightly raised temperature. Offer teething toys, cold washcloths, or discuss pain relief options with your doctor.'
  };

  // Find the most relevant response
  let response = '';
  const questionLower = question.toLowerCase();
  
  for (const [keyword, answer] of Object.entries(mockResponses)) {
    if (questionLower.includes(keyword)) {
      response = answer;
      break;
    }
  }

  // Default response if no match found
  if (!response) {
    response = `Thank you for your question: "${question}". While I can provide general information, every baby is unique. For personalized advice about your baby's health, development, or specific concerns, I recommend consulting with your pediatrician. They can provide guidance tailored to your baby's individual needs and circumstances.`;
  }

  // Add disclaimer
  response += '\n\n**Disclaimer**: This information is for educational purposes only and should not replace professional medical advice. Always consult with your baby\'s healthcare provider for specific concerns.';

  res.status(200).json({ 
    answer: response,
    sources: ['Pediatric guidelines', 'Child development research', 'Healthcare recommendations']
  });
}