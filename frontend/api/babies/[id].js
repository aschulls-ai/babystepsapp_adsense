// Vercel API Route - Individual Baby Operations
export default async function handler(req, res) {
  // Add CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const { id } = req.query;
  
  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  if (req.method === 'GET') {
    // Get individual baby
    const baby = {
      id: id,
      name: 'Emma Johnson',
      birth_date: '2024-03-15',
      gender: 'female',
      birth_weight: 7.2,
      birth_length: 20.5
    };
    res.status(200).json(baby);
  }
  else if (req.method === 'PUT') {
    try {
      const babyData = req.body;
      console.log('Updating baby ID:', id, 'with data:', JSON.stringify(babyData, null, 2));
      
      // Validate required fields
      if (!babyData.name) {
        return res.status(422).json({ detail: 'Baby name is required' });
      }

      // Format birth_date - handle various formats
      let formattedBirthDate = babyData.birth_date;
      if (babyData.birth_date) {
        try {
          const date = new Date(babyData.birth_date);
          if (!isNaN(date.getTime())) {
            formattedBirthDate = date.toISOString().split('T')[0]; // YYYY-MM-DD format
          }
        } catch (error) {
          console.error('Date formatting error:', error);
          formattedBirthDate = babyData.birth_date; // Keep original if formatting fails
        }
      }
      
      // Return the updated baby data
      const updatedBaby = {
        id: id,
        name: babyData.name,
        birth_date: formattedBirthDate || '2024-03-15',
        gender: babyData.gender || 'girl',
        profilePicture: babyData.profilePicture || null,
        birth_weight: babyData.birth_weight || 7.2,
        birth_length: babyData.birth_length || 20.5,
        updated_at: new Date().toISOString()
      };
      
      console.log('Successfully updated baby:', updatedBaby);
      res.status(200).json(updatedBaby);
      
    } catch (error) {
      console.error('Error updating baby:', error);
      res.status(500).json({ 
        detail: 'Internal server error',
        error: error.message 
      });
    }
  }
  else if (req.method === 'DELETE') {
    // Delete baby
    console.log('Deleting baby ID:', id);
    res.status(200).json({ message: 'Baby deleted successfully' });
  }
  else {
    res.status(405).json({ detail: 'Method not allowed' });
  }
}