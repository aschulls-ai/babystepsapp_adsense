// Vercel API Route - Register
// For demo purposes, accept any valid registration
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  const { name, email, password } = req.body;

  if (!name || !email || !password) {
    return res.status(422).json({ detail: 'Missing required fields' });
  }

  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(422).json({ detail: 'Invalid email format' });
  }

  // Password validation
  if (password.length < 6) {
    return res.status(422).json({ detail: 'Password must be at least 6 characters' });
  }

  // For demo: Always successful registration
  // In production, this would save to a real database
  res.status(201).json({ 
    message: 'User created successfully',
    email: email,
    name: name
  });
}