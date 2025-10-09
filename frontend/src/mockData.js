// Mock data for offline demo mode
export const mockUser = {
  id: "demo-user-123",
  email: "demo@babysteps.com",
  name: "Demo Parent"
};

export const mockBabies = [
  {
    id: "demo-baby-456",
    name: "Emma",
    birth_date: "2024-01-15",
    gender: "girl",
    profile_image: null,
    user_id: "demo-user-123"
  }
];

export const mockActivities = [
  {
    id: "activity-1",
    type: "feeding",
    notes: "Formula feeding - 4oz",
    baby_id: "demo-baby-456",
    timestamp: "2025-10-08T10:00:00Z"
  },
  {
    id: "activity-2", 
    type: "sleep",
    notes: "Nap time - 2 hours",
    baby_id: "demo-baby-456",
    timestamp: "2025-10-08T12:00:00Z"
  },
  {
    id: "activity-3",
    type: "diaper",
    notes: "Wet diaper changed",
    baby_id: "demo-baby-456",
    timestamp: "2025-10-08T14:30:00Z"
  },
  {
    id: "activity-4",
    type: "pumping",
    notes: "Breast pump session - 5oz",
    baby_id: "demo-baby-456",
    timestamp: "2025-10-08T16:15:00Z"
  }
];

export const mockFoodResearch = {
  "honey": {
    answer: "Honey should NOT be given to babies under 12 months old due to the risk of infant botulism. Botulism spores can be found in honey and can cause serious illness in infants.",
    safety_level: "avoid",
    age_recommendation: "12+ months only",
    sources: ["American Academy of Pediatrics", "CDC Guidelines"]
  },
  "strawberries": {
    answer: "Fresh strawberries can be introduced around 6 months when baby starts solids. Cut into small pieces to prevent choking. Watch for allergic reactions.",
    safety_level: "safe",
    age_recommendation: "6+ months",
    sources: ["Pediatric Nutrition Guidelines"]
  },
  "nuts": {
    answer: "Whole nuts are a choking hazard. Nut butters can be introduced around 6 months (thin consistency). Watch for allergic reactions.",
    safety_level: "caution", 
    age_recommendation: "6+ months (as nut butter only)",
    sources: ["Food Allergy Guidelines"]
  }
};

export const mockMealPlans = [
  {
    name: "Mashed Banana",
    ingredients: ["1 ripe banana"],
    instructions: ["Mash banana with fork until smooth", "Serve at room temperature"],
    age_appropriate: "6+ months",
    prep_time: "2 minutes"
  },
  {
    name: "Sweet Potato Puree", 
    ingredients: ["1 sweet potato", "Water as needed"],
    instructions: ["Steam sweet potato until soft (15-20 min)", "Mash with water to desired consistency", "Cool before serving"],
    age_appropriate: "6+ months",
    prep_time: "25 minutes"
  },
  {
    name: "Avocado Mash",
    ingredients: ["1/2 ripe avocado"],
    instructions: ["Mash avocado until smooth", "Serve immediately to prevent browning"],
    age_appropriate: "6+ months", 
    prep_time: "1 minute"
  },
  {
    name: "Soft Scrambled Eggs",
    ingredients: ["1 egg", "1 tbsp milk", "Butter"],
    instructions: ["Whisk egg with milk", "Scramble on low heat until very soft", "Cool before serving"],
    age_appropriate: "8+ months",
    prep_time: "5 minutes"
  }
];