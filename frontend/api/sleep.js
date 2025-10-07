// Vercel API Route - Sleep Sessions
export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Mock sleep data
    const sleepSessions = [
      {
        id: '1',
        baby_id: '1',
        start_time: new Date(Date.now() - 4*60*60*1000).toISOString(),
        end_time: new Date(Date.now() - 2*60*60*1000).toISOString(),
        duration: 120 // minutes
      }
    ];
    res.status(200).json(sleepSessions);
  }
  else if (req.method === 'POST') {
    // Mock sleep session creation
    const sleepData = req.body;
    const newSleep = {
      id: Date.now().toString(),
      start_time: new Date().toISOString(),
      ...sleepData
    };
    res.status(201).json(newSleep);
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}