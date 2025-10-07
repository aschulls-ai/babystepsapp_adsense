// Vercel API Route - Login
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  const { email, password } = req.body;

  // Mock authentication for now - replace with real logic
  if (email === 'test@babysteps.com' && password === 'TestPassword123') {
    // Generate a simple JWT-like token (in production, use proper JWT)
    const token = Buffer.from(JSON.stringify({ email, exp: Date.now() + 24*60*60*1000 })).toString('base64');
    
    res.status(200).json({ 
      access_token: token,
      token_type: 'bearer'
    });
  } else {
    res.status(401).json({ detail: 'Invalid credentials' });
  }
}