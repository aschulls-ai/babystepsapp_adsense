// Vercel API Route - Reminders
let reminders = []; // In-memory storage (use database in production)

export default async function handler(req, res) {
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Return reminders filtered by baby_id if provided
    const { baby_id } = req.query;
    const filteredReminders = baby_id 
      ? reminders.filter(r => r.baby_id === baby_id && r.is_active)
      : reminders.filter(r => r.is_active);
    
    res.status(200).json(filteredReminders);
  }
  else if (req.method === 'POST') {
    // Create new reminder
    const reminderData = req.body;
    const newReminder = {
      id: Date.now().toString(),
      is_active: true,
      created_at: new Date().toISOString(),
      ...reminderData
    };
    
    reminders.push(newReminder);
    res.status(201).json(newReminder);
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}