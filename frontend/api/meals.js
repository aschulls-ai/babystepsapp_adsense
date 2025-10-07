// Vercel API Route - Meals CRUD operations
export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  // For now, return empty array since we're using this primarily for meal search
  // In a real implementation, this would connect to a database
  
  if (req.method === 'GET') {
    // Get saved meal plans
    const { baby_id } = req.query;
    
    if (!baby_id) {
      return res.status(422).json({ detail: 'Baby ID is required' });
    }
    
    // Return empty array for now - saved meals functionality can be implemented later
    return res.status(200).json([]);
    
  } else if (req.method === 'POST') {
    // Save a meal plan
    const { baby_id, meal_name, ingredients, instructions, nutrition_notes, age_months } = req.body;
    
    if (!baby_id || !meal_name) {
      return res.status(422).json({ detail: 'Baby ID and meal name are required' });
    }
    
    // Mock successful save response
    const savedMeal = {
      id: Date.now().toString(),
      baby_id,
      meal_name,
      ingredients: ingredients || [],
      instructions: instructions || [],
      nutrition_notes: nutrition_notes || '',
      age_months: age_months || 6,
      created_at: new Date().toISOString()
    };
    
    return res.status(200).json(savedMeal);
    
  } else {
    return res.status(405).json({ detail: 'Method not allowed' });
  }
}