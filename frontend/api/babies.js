// Vercel API Route - Babies
export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Mock baby data - 18 months old for realistic demo
    const eighteenMonthsAgo = new Date();
    eighteenMonthsAgo.setMonth(eighteenMonthsAgo.getMonth() - 18);
    
    const babies = [
      {
        id: '1',
        name: 'Emma Johnson',
        birth_date: eighteenMonthsAgo.toISOString().split('T')[0], // 18 months ago
        gender: 'girl',
        profilePicture: null,
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
    const eighteenMonthsAgo = new Date();
    eighteenMonthsAgo.setMonth(eighteenMonthsAgo.getMonth() - 18);
    
    const updatedBaby = {
      id: '1', // In a real app, this would come from the URL parameter
      name: babyData.name || 'Emma Johnson',
      birth_date: babyData.birth_date || eighteenMonthsAgo.toISOString().split('T')[0],
      gender: babyData.gender || 'girl',
      profilePicture: babyData.profilePicture || null,
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