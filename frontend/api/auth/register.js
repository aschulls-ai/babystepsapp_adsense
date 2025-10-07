// Vercel API Route - Register
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  const { name, email, password } = req.body;

  // Mock registration - replace with real database logic
  if (!name || !email || !password) {
    return res.status(422).json({ detail: 'Missing required fields' });
  }

  // Simulate successful registration
  res.status(201).json({ 
    message: 'User created successfully',
    email: email,
    name: name
  });
}