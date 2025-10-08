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

  // Mock responses for common parenting questions
  const mockResponses = {
    'sleep': 'Newborns typically sleep 14-17 hours per day, but this varies greatly. Establishing a bedtime routine around 3-4 months can help. Safe sleep practices include: back sleeping, firm mattress, no loose bedding, and room-sharing (but not bed-sharing) for the first 6 months.',
    
    'feeding': 'Breastfeeding is recommended exclusively for the first 6 months. Formula feeding is also nutritionally complete. Signs of hunger include rooting, sucking motions, and fussiness. Signs of fullness include turning away from bottle/breast and closing mouth.',
    
    'development': 'Every baby develops at their own pace. Typical milestones include: 2 months - social smiles, 4-6 months - rolling over, 6-9 months - sitting, 9-12 months - crawling/walking, 12+ months - first words. Consult your pediatrician if you have concerns.',
    
    'crying': 'Babies cry for many reasons: hunger, tiredness, overstimulation, dirty diaper, or need for comfort. The "Period of PURPLE Crying" (peak fussiness) often occurs between 2-5 months. Try the 5 S\'s: Swaddle, Side position, Shush, Swing, Suck.',
    
    'diaper': 'Newborns typically have 6-8 wet diapers per day and frequent bowel movements. Breastfed babies may have seedy, yellow stools, while formula-fed babies have firmer, tan-colored stools. Always clean from front to back and allow air-drying time.',
    
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