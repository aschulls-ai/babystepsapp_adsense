// Vercel API Route - Individual Reminder Operations
let reminders = []; // Shared with /api/reminders.js

export default async function handler(req, res) {
  const { id } = req.query;
  
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'PATCH') {
    // Update reminder
    const reminderIndex = reminders.findIndex(r => r.id === id);
    if (reminderIndex === -1) {
      return res.status(404).json({ detail: 'Reminder not found' });
    }

    // Update fields
    reminders[reminderIndex] = { 
      ...reminders[reminderIndex], 
      ...req.body 
    };
    
    res.status(200).json({ message: 'Reminder updated successfully' });
  }
  else if (req.method === 'DELETE') {
    // Delete reminder (mark as inactive)
    const reminderIndex = reminders.findIndex(r => r.id === id);
    if (reminderIndex === -1) {
      return res.status(404).json({ detail: 'Reminder not found' });
    }

    reminders[reminderIndex].is_active = false;
    res.status(200).json({ message: 'Reminder deleted successfully' });
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}