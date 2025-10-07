// Vercel API Route - Login
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  const { email, password } = req.body;

  // Basic validation
  if (!email || !password) {
    return res.status(422).json({ detail: 'Email and password are required' });
  }

  // Check test user
  if (email === 'test@babysteps.com' && password === 'TestPassword123') {
    const token = Buffer.from(JSON.stringify({ 
      email, 
      name: 'Test User',
      exp: Date.now() + 24*60*60*1000 
    })).toString('base64');
    return res.status(200).json({ 
      access_token: token,
      token_type: 'bearer'
    });
  }

  // For demo: Accept any valid email/password combination that looks reasonable
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailRegex.test(email) && password.length >= 6) {
    // Generate token for any valid-looking credentials
    const token = Buffer.from(JSON.stringify({ 
      email: email,
      name: email.split('@')[0], // Use email username as name
      id: Date.now().toString(),
      exp: Date.now() + 24*60*60*1000 
    })).toString('base64');
    
    res.status(200).json({ 
      access_token: token,
      token_type: 'bearer'
    });
  } else {
    res.status(401).json({ detail: 'Invalid credentials' });
  }
}