// Vercel API Route - Babies
export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Mock baby data
    const babies = [
      {
        id: '1',
        name: 'Emma Johnson',
        birth_date: '2024-03-15',
        gender: 'female',
        birth_weight: 7.2,
        birth_length: 20.5
      }
    ];
    res.status(200).json(babies);
  } 
  else if (req.method === 'POST') {
    // Mock baby creation
    const babyData = req.body;
    const newBaby = {
      id: Date.now().toString(),
      ...babyData
    };
    res.status(201).json(newBaby);
  }
  else if (req.method === 'PUT') {
    // Mock baby update
    const babyData = req.body;
    console.log('Updating baby with data:', babyData);
    
    // Return the updated baby data (merge with existing data)
    const updatedBaby = {
      id: '1', // In a real app, this would come from the URL parameter
      name: babyData.name || 'Emma Johnson',
      birth_date: babyData.birth_date || '2024-03-15',
      gender: babyData.gender || 'female',
      birth_weight: babyData.birth_weight || 7.2,
      birth_length: babyData.birth_length || 20.5,
      ...babyData // Include any additional fields
    };
    
    console.log('Returning updated baby:', updatedBaby);
    res.status(200).json(updatedBaby);
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}