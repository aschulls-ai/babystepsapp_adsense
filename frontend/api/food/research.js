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

  // Mock responses based on common food safety questions
  const mockResponses = {
    'honey': `Honey should not be given to babies under 12 months old due to the risk of botulism. After 12 months, honey is generally safe in small amounts. For your ${baby_age_months || 'baby'} month old baby, ${baby_age_months < 12 ? 'please wait until after 12 months' : 'honey can be introduced gradually'}.`,
    
    'nuts': `Tree nuts and peanuts can be introduced around 6 months, but should be given in age-appropriate forms. Whole nuts are a choking hazard until age 4. For your ${baby_age_months || 'baby'} month old baby, ${baby_age_months < 6 ? 'wait until 6 months for nut introduction' : 'try smooth nut butters or finely ground nuts mixed into other foods'}.`,
    
    'eggs': `Eggs can be introduced around 6 months. Make sure they are fully cooked to avoid salmonella risk. For your ${baby_age_months || 'baby'} month old baby, ${baby_age_months < 6 ? 'wait until 6 months' : 'try scrambled eggs or hard-boiled egg yolk as a finger food'}.`,
    
    'fish': `Fish is an excellent source of protein and omega-3 fatty acids. Low-mercury fish can be introduced around 6 months. Avoid high-mercury fish like shark, swordfish, and king mackerel. For your ${baby_age_months || 'baby'} month old baby, try salmon, cod, or tilapia in small, flaked pieces.`,
    
    'dairy': `Cow's milk should not be introduced as a drink until 12 months, but dairy products like cheese and yogurt can be introduced around 6 months. For your ${baby_age_months || 'baby'} month old baby, ${baby_age_months < 6 ? 'stick to breast milk or formula' : baby_age_months < 12 ? 'try small amounts of plain yogurt or soft cheese' : 'you can now introduce whole milk'}.`
  };

  // Find relevant response
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
    response = `Based on your question about "${question}", I recommend consulting with your pediatrician for personalized advice. For babies around ${baby_age_months || 6} months old, focus on introducing single ingredient foods one at a time, watching for allergic reactions, and ensuring foods are properly prepared for their age and developmental stage.`;
  }

  // Add general safety reminder
  response += '\n\n**Safety Reminder**: Always supervise your baby during meals, cut foods appropriately to prevent choking, and introduce new foods gradually while watching for allergic reactions.';

  res.status(200).json({ 
    answer: response,
    safety_level: 'consult_pediatrician',
    sources: ['General pediatric guidelines', 'Food safety recommendations']
  });
}