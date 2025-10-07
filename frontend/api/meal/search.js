// Vercel API Route - Meal Search
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  const { query, baby_age_months } = req.body;

  if (!query) {
    return res.status(422).json({ detail: 'Search query is required' });
  }

  // Mock meal suggestions based on age and query
  const mealSuggestions = {
    'breakfast': {
      '4-6': ['Iron-fortified baby cereal mixed with breast milk or formula', 'Mashed banana', 'Pureed sweet potato'],
      '6-9': ['Oatmeal with mashed berries', 'Scrambled egg yolk', 'Toast strips with avocado', 'Banana pancakes (no honey)'],
      '9-12': ['Mini egg muffins', 'French toast sticks', 'Yogurt with soft fruit pieces', 'Whole grain cereal with milk'],
      '12+': ['Whole grain toast with nut butter', 'Scrambled eggs with cheese', 'Whole milk with cereal', 'Fresh fruit slices']
    },
    'lunch': {
      '4-6': ['Pureed chicken or beef', 'Steamed and mashed vegetables', 'Pureed fruit'],
      '6-9': ['Soft cooked pasta pieces', 'Shredded cheese', 'Soft steamed broccoli', 'Small pieces of soft meat'],
      '9-12': ['Mini sandwiches cut into small pieces', 'Cooked beans', 'Soft vegetables', 'Small pasta shapes'],
      '12+': ['Cut-up sandwiches', 'Soup with soft vegetables', 'Quesadilla pieces', 'Steamed vegetables']
    },
    'dinner': {
      '4-6': ['Pureed vegetables', 'Mashed potatoes (no butter/salt)', 'Pureed meat or beans'],
      '6-9': ['Soft cooked rice', 'Steamed carrot sticks', 'Soft meatballs', 'Mashed beans'],
      '9-12': ['Small pieces of family meal', 'Soft cooked vegetables', 'Ground meat', 'Soft pasta'],
      '12+': ['Modified family meals', 'Cut vegetables', 'Whole grains', 'Protein portions appropriate for toddlers']
    },
    'snack': {
      '4-6': ['Breast milk or formula only'],
      '6-9': ['Banana slices', 'Soft pear pieces', 'Baby puffs', 'Teething biscuits'],
      '9-12': ['Cheerios', 'Small pieces of cheese', 'Soft fruit', 'Crackers'],
      '12+': ['Fresh fruit', 'Whole grain crackers', 'Yogurt', 'Small portions of nuts (if no allergies)']
    }
  };

  // Determine age group
  let ageGroup = '6-9';
  if (baby_age_months < 6) ageGroup = '4-6';
  else if (baby_age_months < 9) ageGroup = '6-9';
  else if (baby_age_months < 12) ageGroup = '9-12';
  else ageGroup = '12+';

  // Find meal type from query
  const queryLower = query.toLowerCase();
  let mealType = 'lunch'; // default
  
  if (queryLower.includes('breakfast') || queryLower.includes('morning')) mealType = 'breakfast';
  else if (queryLower.includes('lunch') || queryLower.includes('midday')) mealType = 'lunch';
  else if (queryLower.includes('dinner') || queryLower.includes('evening')) mealType = 'dinner';
  else if (queryLower.includes('snack')) mealType = 'snack';

  const suggestions = mealSuggestions[mealType][ageGroup] || mealSuggestions['lunch'][ageGroup];

  const response = `Here are some ${mealType} ideas for your ${baby_age_months} month old baby:\n\n` +
    suggestions.map((item, index) => `${index + 1}. ${item}`).join('\n') +
    `\n\n**Age-Appropriate Notes for ${baby_age_months} months:**\n` +
    (baby_age_months < 6 ? '- Focus on single-ingredient purees\n- Introduce one new food at a time\n- Watch for allergic reactions' :
     baby_age_months < 9 ? '- Foods should be soft and mashable\n- Cut foods smaller than your baby\'s thumbnail\n- Encourage self-feeding with finger foods' :
     baby_age_months < 12 ? '- Continue offering variety\n- Foods can be chunkier but still soft\n- Always supervise during meals' :
     '- Can eat most family foods with modifications\n- Continue to cut foods appropriately\n- Encourage trying new flavors and textures');

  res.status(200).json({ 
    results: response
  });
}