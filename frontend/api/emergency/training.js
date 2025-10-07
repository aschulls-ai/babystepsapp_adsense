// Vercel API Route - Emergency Training
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  // Simple auth check
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) {
    return res.status(401).json({ detail: 'Not authenticated' });
  }

  const { emergency_type, baby_age_months } = req.body;

  const trainingContent = {
    choking: {
      steps: [
        "Stay calm and assess the situation",
        "If baby can cry or cough, encourage them to continue",
        "If baby cannot make sounds, place them face-down on your forearm",
        "Support their head and neck with your hand",
        "Give 5 firm back blows between shoulder blades",
        "Turn baby face-up and give 5 chest thrusts with 2 fingers",
        "Repeat until object is expelled or baby becomes unconscious"
      ],
      important_notes: [
        "Never do blind finger sweeps",
        "Call 911 immediately if baby becomes unconscious",
        "Different techniques for infants vs toddlers"
      ],
      when_to_call_911: [
        "Baby cannot cry, cough, or breathe",
        "Baby turns blue",
        "Baby becomes unconscious",
        "You cannot remove the obstruction"
      ]
    },
    cpr: {
      steps: [
        "Check for responsiveness - tap shoulders gently",
        "Call 911 and request AED if available",
        "Place baby on firm surface, tilt head back slightly",
        "Place 2 fingers on breastbone, just below nipple line",
        "Push hard and fast at least 1.5 inches deep",
        "Allow complete chest recoil between compressions",
        "Give 30 compressions at 100-120 beats per minute",
        "If trained, give 2 rescue breaths, then continue cycles"
      ],
      important_notes: [
        "Use 2 fingers for infants under 1 year",
        "Use heel of one hand for children over 1 year",
        "Don't be afraid to push hard - ribs can heal"
      ],
      when_to_call_911: [
        "Baby is not breathing",
        "Baby has no pulse",
        "Baby is unconscious and unresponsive"
      ]
    },
    general: {
      steps: [
        "Assess the scene for safety",
        "Check baby's responsiveness",
        "Look for obvious injuries or distress",
        "Check breathing and circulation",
        "Call 911 if in doubt",
        "Provide basic care while waiting for help",
        "Stay with baby and monitor condition"
      ],
      important_notes: [
        "When in doubt, call 911",
        "Trust your instincts as a parent",
        "Keep emergency numbers easily accessible"
      ],
      when_to_call_911: [
        "Any time you're worried about baby's safety",
        "Difficulty breathing",
        "Unusual behavior or appearance",
        "High fever in babies under 3 months"
      ]
    }
  };

  const content = trainingContent[emergency_type] || trainingContent.general;
  
  // Add age-specific notes
  const ageSpecificNote = baby_age_months < 12 ? 
    "This content is tailored for infants under 12 months. Use 2-finger technique for chest compressions." :
    "This content includes techniques for toddlers over 12 months. Adjust techniques as baby grows.";

  res.status(200).json({
    ...content,
    disclaimer: `This is educational content only and does not replace proper first aid training. ${ageSpecificNote} Please take an official CPR/First Aid course for hands-on practice.`
  });
}