// Vercel API Route - Register
// Simple in-memory user storage (use database in production)
global.users = global.users || [];

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  const { name, email, password } = req.body;

  if (!name || !email || !password) {
    return res.status(422).json({ detail: 'Missing required fields' });
  }

  // Check if user already exists
  const existingUser = global.users.find(user => user.email === email);
  if (existingUser) {
    return res.status(400).json({ detail: 'User already exists' });
  }

  // Create new user
  const newUser = {
    id: Date.now().toString(),
    name,
    email,
    password, // In production, hash this password
    created_at: new Date().toISOString()
  };

  global.users.push(newUser);

  res.status(201).json({ 
    message: 'User created successfully',
    email: email,
    name: name
  });
}