// Vercel API Route - Login
export default async function handler(req, res) {
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  try {
    const { email, password } = req.body;
    
    console.log('Login attempt:', { email, passwordLength: password?.length });

    // Basic validation
    if (!email || !password) {
      console.log('Missing email or password');
      return res.status(422).json({ detail: 'Email and password are required' });
    }

    // Check demo user for AdSense verification
    if (email === 'demo@babysteps.com' && password === 'DemoPassword123') {
      console.log('Demo user login successful for AdSense verification');
      const token = Buffer.from(JSON.stringify({ 
        email, 
        name: 'Demo Parent',
        exp: Date.now() + 24*60*60*1000 
      })).toString('base64');
      return res.status(200).json({ 
        access_token: token,
        token_type: 'bearer'
      });
    }

    // Check test user
    if (email === 'test@babysteps.com' && password === 'TestPassword123') {
      console.log('Test user login successful');
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
      console.log('Valid email/password format, generating token');
      // Generate token for any valid-looking credentials
      const token = Buffer.from(JSON.stringify({ 
        email: email,
        name: email.split('@')[0], // Use email username as name
        id: Date.now().toString(),
        exp: Date.now() + 24*60*60*1000 
      })).toString('base64');
      
      return res.status(200).json({ 
        access_token: token,
        token_type: 'bearer'
      });
    } else {
      console.log('Invalid credentials format');
      return res.status(401).json({ detail: 'Invalid credentials' });
    }
  } catch (error) {
    console.error('Login error:', error);
    return res.status(500).json({ detail: 'Internal server error' });
  }
}