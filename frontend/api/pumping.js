// Vercel API Route - Pumping Sessions
export default async function handler(req, res) {
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

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
    try {
      const pumpingData = req.body;
      
      console.log('Pumping data received:', JSON.stringify(pumpingData, null, 2));
      
      // Calculate total if left and right breast amounts are provided
      const leftBreast = pumpingData.leftBreast || pumpingData.left_breast || 0;
      const rightBreast = pumpingData.rightBreast || pumpingData.right_breast || 0;
      const totalAmount = leftBreast + rightBreast;
      
      // Validate required fields - be more flexible with baby_id
      if (!pumpingData.baby_id && !pumpingData.babyId) {
        console.log('Missing baby_id in pumping data');
        return res.status(422).json({ 
          detail: 'baby_id is required',
          received_data: pumpingData 
        });
      }

      // Use baby_id or generate a default one for demo
      const babyId = pumpingData.baby_id || pumpingData.babyId || '1';
      
      const newPumping = {
        id: Date.now().toString(),
        baby_id: babyId,
        timestamp: pumpingData.timestamp || new Date().toISOString(),
        left_breast: leftBreast,
        right_breast: rightBreast,
        total_amount: totalAmount,
        duration: pumpingData.duration || 0
      };
      
      console.log('Created pumping session:', newPumping);
      
      res.status(201).json(newPumping);
    } catch (error) {
      console.error('Error creating pumping session:', error);
      res.status(500).json({ 
        detail: 'Internal server error',
        error: error.message 
      });
    }
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}