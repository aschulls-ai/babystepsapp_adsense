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

  // Comprehensive meal recipes with step-by-step instructions
  const mealRecipes = {
    'breakfast': {
      '4-6': [
        {
          name: 'Iron-Fortified Baby Cereal',
          ingredients: ['2 tbsp iron-fortified baby cereal', '4-6 tbsp breast milk or formula'],
          steps: [
            'Start with 1 tablespoon of cereal',
            'Gradually add breast milk or formula until smooth, thin consistency',
            'Mix well to avoid lumps',
            'Serve immediately at room temperature',
            'Start with 1-2 teaspoons, increase gradually as baby accepts'
          ],
          safety: 'Always supervise feeding. Never add honey to baby cereal.',
          servings: '1-2 tablespoons'
        },
        {
          name: 'Mashed Banana',
          ingredients: ['1/2 ripe banana'],
          steps: [
            'Choose a very ripe banana with brown spots',
            'Peel and mash with fork until completely smooth',
            'Check for any lumps that could cause choking',
            'Serve immediately to prevent browning',
            'Offer 1-2 teaspoons initially'
          ],
          safety: 'Ensure completely smooth texture for babies under 6 months.',
          servings: '2-3 teaspoons'
        }
      ],
      '6-9': [
        {
          name: 'Baby Banana Pancakes',
          ingredients: ['1 ripe banana', '1 egg', '2 tbsp oat flour (optional)'],
          steps: [
            'Mash banana thoroughly in a bowl',
            'Crack egg and whisk with banana until well combined',
            'Add oat flour if desired for thickness',
            'Heat non-stick pan over low-medium heat',
            'Pour small amounts (2 tbsp) to make mini pancakes',
            'Cook 2-3 minutes until bubbles form, flip carefully',
            'Cook another 1-2 minutes until golden',
            'Cool and cut into finger-sized strips'
          ],
          safety: 'Ensure pancakes are cooked through. Cool completely before serving. NO HONEY.',
          servings: '4-6 small pancakes'
        }
      ],
      '9-12': [
        {
          name: 'Mini Egg Muffins',
          ingredients: ['3 eggs', '1/4 cup shredded cheese', '1/4 cup finely diced vegetables', 'cooking spray'],
          steps: [
            'Preheat oven to 350°F (175°C)',
            'Spray mini muffin tin with cooking spray',
            'Whisk eggs in a bowl',
            'Add cheese and diced vegetables (carrots, spinach, peppers)',
            'Mix well and pour into muffin cups, filling 3/4 full',
            'Bake 12-15 minutes until eggs are set',
            'Cool completely before serving',
            'Store in refrigerator up to 3 days'
          ],
          safety: 'Ensure vegetables are very finely diced. Check temperature before serving.',
          servings: '12 mini muffins'
        }
      ],
      '12+': [
        {
          name: 'Whole Grain French Toast Sticks',
          ingredients: ['2 slices whole grain bread', '1 egg', '2 tbsp whole milk', '1/4 tsp cinnamon', 'butter for cooking'],
          steps: [
            'Cut bread into thick finger-width strips',
            'Whisk egg, milk, and cinnamon in shallow dish',
            'Dip each bread strip in egg mixture, coating both sides',
            'Heat small amount of butter in non-stick pan over medium heat',
            'Cook strips 2-3 minutes per side until golden',
            'Cool slightly and check temperature',
            'Serve with mashed fruit if desired'
          ],
          safety: 'Ensure strips are cool enough to handle. Always supervise eating.',
          servings: '8-10 sticks'
        }
      ]
    },
    'lunch': {
      '6-9': [
        {
          name: 'Soft Pasta with Cheese',
          ingredients: ['1/2 cup small pasta (like stelline)', '2 tbsp shredded mild cheese', '1 tbsp butter'],
          steps: [
            'Cook pasta according to package directions until very soft',
            'Drain and let cool slightly',
            'Add butter and cheese while pasta is warm',
            'Mash slightly with fork if needed for younger babies',
            'Ensure pieces are appropriate size for baby\'s age',
            'Cool to safe temperature before serving'
          ],
          safety: 'Check pasta is soft enough to mash with tongue. Supervise eating.',
          servings: '1/2 cup'
        }
      ]
    },
    'dinner': {
      '9-12': [
        {
          name: 'Mini Turkey Meatballs',
          ingredients: ['1/4 lb ground turkey', '1 slice bread, crumbled', '1 egg yolk', '2 tbsp finely grated cheese'],
          steps: [
            'Preheat oven to 375°F (190°C)',
            'Mix all ingredients in a bowl',
            'Form into small, baby-finger-sized balls',
            'Place on lined baking sheet',
            'Bake 15-20 minutes until cooked through (165°F internal temp)',
            'Cool completely before serving',
            'Ensure meatballs are soft and easy to chew'
          ],
          safety: 'Check internal temperature with meat thermometer. Cut larger pieces if needed.',
          servings: '12-15 mini meatballs'
        }
      ]
    },
    'snack': {
      '12+': [
        {
          name: 'Homemade Teething Biscuits',
          ingredients: ['1 cup whole wheat flour', '2 tbsp coconut oil', '1/4 cup water', '1 mashed banana'],
          steps: [
            'Preheat oven to 350°F (175°C)',
            'Mix flour and coconut oil until crumbly',
            'Add mashed banana and water gradually',
            'Form dough and roll to 1/2 inch thickness',
            'Cut into finger-sized rectangles',
            'Place on parchment-lined baking sheet',
            'Bake 15-20 minutes until lightly golden',
            'Cool completely before giving to baby'
          ],
          safety: 'Supervise closely during eating. Soften in milk if too hard.',
          servings: '8-10 biscuits'
        }
      ]
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

  const recipes = mealRecipes[mealType]?.[ageGroup] || mealRecipes['lunch']?.[ageGroup] || [];

  if (recipes.length === 0) {
    // Fallback for age groups without detailed recipes
    const basicSuggestions = [
      'Age-appropriate soft foods',
      'Properly sized portions',
      'Safe temperature foods'
    ];
    return res.status(200).json({ 
      results: `Here are some ${mealType} ideas for your ${baby_age_months} month old baby:\n\n` +
        basicSuggestions.map((item, index) => `${index + 1}. ${item}`).join('\n')
    });
  }

  let response = `# ${mealType.charAt(0).toUpperCase() + mealType.slice(1)} Recipes for ${baby_age_months} Month Old\n\n`;
  
  recipes.forEach((recipe, index) => {
    response += `## ${index + 1}. ${recipe.name}\n\n`;
    
    response += `**Ingredients:**\n`;
    recipe.ingredients.forEach(ingredient => {
      response += `• ${ingredient}\n`;
    });
    
    response += `\n**Instructions:**\n`;
    recipe.steps.forEach((step, stepIndex) => {
      response += `${stepIndex + 1}. ${step}\n`;
    });
    
    response += `\n**Safety Notes:** ${recipe.safety}\n`;
    response += `**Servings:** ${recipe.servings}\n\n`;
    response += `---\n\n`;
  });

  response += `## Age-Appropriate Guidelines for ${baby_age_months} months:\n\n`;
  response += (baby_age_months < 6 ? 
    '• Focus on single-ingredient purees\n• Introduce one new food at a time\n• Watch for allergic reactions\n• No honey, salt, or sugar' :
    baby_age_months < 9 ? 
    '• Foods should be soft and mashable\n• Cut foods smaller than baby\'s thumbnail\n• Encourage self-feeding with finger foods\n• Continue breastfeeding or formula' :
    baby_age_months < 12 ? 
    '• Continue offering variety\n• Foods can be chunkier but still soft\n• Always supervise during meals\n• Introduce cup drinking' :
    '• Can eat most family foods with modifications\n• Continue to cut foods appropriately\n• Encourage trying new flavors and textures\n• Transition to whole milk at 12 months'
  );

  res.status(200).json({ 
    results: response
  });
}