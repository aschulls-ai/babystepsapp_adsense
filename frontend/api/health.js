// Vercel API Route - Health Check
export default function handler(req, res) {
  res.status(200).json({ 
    status: "healthy", 
    service: "Baby Steps API", 
    timestamp: new Date().toISOString() 
  });
}