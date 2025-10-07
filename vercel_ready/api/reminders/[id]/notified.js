// Vercel API Route - Mark Reminder as Notified
let reminders = []; // Shared with other reminder endpoints

export default async function handler(req, res) {
  const { id } = req.query;
  
  if (req.method !== 'PATCH') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  const reminderIndex = reminders.findIndex(r => r.id === id);
  if (reminderIndex === -1) {
    return res.status(404).json({ detail: 'Reminder not found' });
  }

  const reminder = reminders[reminderIndex];
  
  // Calculate next notification time based on interval_hours
  const currentNextDue = new Date(reminder.next_due);
  const intervalHours = reminder.interval_hours || 24; // Default to daily
  const nextDue = new Date(currentNextDue.getTime() + (intervalHours * 60 * 60 * 1000));
  
  // Update reminder
  reminders[reminderIndex] = {
    ...reminder,
    next_due: nextDue.toISOString()
  };
  
  res.status(200).json({ message: 'Reminder marked as notified and rescheduled' });
}