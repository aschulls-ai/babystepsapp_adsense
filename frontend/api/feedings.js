// Vercel API Route - Feedings
export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Mock feeding data
    const feedings = [
      {
        id: '1',
        baby_id: '1',
        type: 'bottle',
        amount: 4,
        timestamp: new Date(Date.now() - 2*60*60*1000).toISOString()
      },
      {
        id: '2', 
        baby_id: '1',
        type: 'breast',
        duration: 25,
        timestamp: new Date(Date.now() - 5*60*60*1000).toISOString()
      }
    ];
    res.status(200).json(feedings);
  }
  else if (req.method === 'POST') {
    // Mock feeding creation
    const feedingData = req.body;
    const newFeeding = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      ...feedingData
    };
    res.status(201).json(newFeeding);
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}