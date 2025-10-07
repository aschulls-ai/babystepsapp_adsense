// Vercel API Route - Login
import { findUser } from '../utils/storage.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  const { email, password } = req.body;

  // Check test user first
  if (email === 'test@babysteps.com' && password === 'TestPassword123') {
    const token = Buffer.from(JSON.stringify({ email, exp: Date.now() + 24*60*60*1000 })).toString('base64');
    return res.status(200).json({ 
      access_token: token,
      token_type: 'bearer'
    });
  }

  // Check registered users
  const user = findUser(email);
  
  if (user && user.password === password) {
    // Generate a simple JWT-like token
    const token = Buffer.from(JSON.stringify({ 
      email: user.email, 
      name: user.name,
      id: user.id,
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