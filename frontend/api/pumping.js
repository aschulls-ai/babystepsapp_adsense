// Vercel API Route - Pumping Sessions
export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Mock pumping data
    const pumpingSessions = [
      {
        id: '1',
        baby_id: '1',
        duration: 20, // minutes
        left_breast: 2.5, // oz
        right_breast: 2.0, // oz
        total_amount: 4.5,
        timestamp: new Date(Date.now() - 2*60*60*1000).toISOString()
      },
      {
        id: '2',
        baby_id: '1',
        duration: 15,
        left_breast: 1.5,
        right_breast: 2.5,
        total_amount: 4.0,
        timestamp: new Date(Date.now() - 6*60*60*1000).toISOString()
      }
    ];
    res.status(200).json(pumpingSessions);
  }
  else if (req.method === 'POST') {
    // Mock pumping session creation
    const pumpingData = req.body;
    
    // Calculate total if left and right breast amounts are provided
    const leftBreast = pumpingData.leftBreast || pumpingData.left_breast || 0;
    const rightBreast = pumpingData.rightBreast || pumpingData.right_breast || 0;
    const totalAmount = leftBreast + rightBreast;
    
    const newPumping = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      left_breast: leftBreast,
      right_breast: rightBreast,
      total_amount: totalAmount,
      duration: pumpingData.duration || 0,
      ...pumpingData
    };
    
    res.status(201).json(newPumping);
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}