// Vercel API Route - Diapers
export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Mock diaper data
    const diapers = [
      {
        id: '1',
        baby_id: '1',
        type: 'wet',
        timestamp: new Date(Date.now() - 1*60*60*1000).toISOString()
      },
      {
        id: '2',
        baby_id: '1', 
        type: 'dirty',
        timestamp: new Date(Date.now() - 3*60*60*1000).toISOString()
      }
    ];
    res.status(200).json(diapers);
  }
  else if (req.method === 'POST') {
    // Mock diaper creation
    const diaperData = req.body;
    const newDiaper = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      ...diaperData
    };
    res.status(201).json(newDiaper);
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}