// Complete Standalone App Mode - Primary Operation Mode
// This allows the app to work fully without server connection

import { v4 as uuidv4 } from 'uuid';
import aiService from './aiService';

// Standalone app mode - this is now the PRIMARY mode
export const shouldUseOfflineMode = () => {
  // Always use standalone mode as primary - server connection is optional
  return true;
};

// Enable offline mode
export const enableOfflineMode = () => {
  localStorage.setItem('babysteps_app_mode', 'standalone');
  localStorage.setItem('babysteps_offline_mode', 'true');
  console.log('🏠 Standalone app mode active - All features available locally');
};

// Storage helpers
const getOfflineData = (key, defaultValue = {}) => {
  try {
    const data = localStorage.getItem(`babysteps_offline_${key}`);
    return data ? JSON.parse(data) : defaultValue;
  } catch (error) {
    console.error(`Error reading offline ${key}:`, error);
    return defaultValue;
  }
};

const saveOfflineData = (key, data) => {
  try {
    localStorage.setItem(`babysteps_offline_${key}`, JSON.stringify(data));
    return true;
  } catch (error) {
    console.error(`Error saving offline ${key}:`, error);
    return false;
  }
};

// Initialize offline data
export const initializeOfflineMode = () => {
  console.log('🚀 Initializing offline mode...');
  
  const users = getOfflineData('users', {});
  
  // Create demo user if no users exist
  if (Object.keys(users).length === 0) {
    const demoUserId = uuidv4();
    users['demo@babysteps.com'] = {
      id: demoUserId,
      email: 'demo@babysteps.com',
      name: 'Demo Parent',
      password: 'demo123', // In real app, this would be hashed
      createdAt: new Date().toISOString()
    };
    saveOfflineData('users', users);
    
    // Create demo baby
    const demoBaby = {
      id: uuidv4(),
      name: 'Emma',
      birth_date: '2024-01-15',
      gender: 'girl',
      profile_image: null,
      user_id: demoUserId,
      createdAt: new Date().toISOString()
    };
    
    const babies = {};
    babies[demoUserId] = [demoBaby]; // Store babies by user ID
    saveOfflineData('babies', babies);
    
    // Create demo activities
    const activities = {};
    const demoActivities = [
      {
        id: uuidv4(),
        type: 'feeding',
        notes: 'Formula feeding - 4oz',
        baby_id: demoBaby.id,
        user_id: demoUserId,
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString()
      },
      {
        id: uuidv4(),
        type: 'sleep', 
        notes: 'Nap time - 2 hours',
        baby_id: demoBaby.id,
        user_id: demoUserId,
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
      },
      {
        id: uuidv4(),
        type: 'diaper',
        notes: 'Wet diaper changed',
        baby_id: demoBaby.id,
        user_id: demoUserId,
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString()
      }
    ];
    
    activities[demoUserId] = demoActivities; // Store activities by user ID
    saveOfflineData('activities', activities);
    
    console.log('✅ Offline demo data initialized');
  }
};

// Offline API simulation
export const offlineAPI = {
  // Authentication
  // Enhanced user login with improved validation and tracking
  login: async (email, password) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          // Input validation
          if (!email || !password) {
            reject(new Error('Email and password are required'));
            return;
          }

          const users = getOfflineData('users', {});
          const emailKey = email.toLowerCase().trim();
          const user = users[emailKey];
          
          if (!user || user.password !== password) {
            reject(new Error('Invalid email or password'));
            return;
          }
          
          // Update last login time
          user.lastLoginAt = new Date().toISOString();
          users[emailKey] = user;
          saveOfflineData('users', users);
          
          // Set current user (just the ID for consistency with registration)
          localStorage.setItem('babysteps_current_user', user.id);
          
          // Generate access token
          const token = `standalone_token_${user.id}_${Date.now()}`;
          
          console.log('✅ User logged in successfully in standalone mode:', emailKey);
          resolve({
            data: {
              access_token: token,
              user: {
                id: user.id,
                email: user.email,
                name: user.name
              }
            }
          });
        } catch (error) {
          reject(error);
        }
      }, 300); // Faster response for standalone app
    });
  },

  // Enhanced user registration with comprehensive validation
  register: async (name, email, password) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          // Comprehensive input validation
          if (!name || name.trim().length < 2) {
            reject(new Error('Name must be at least 2 characters long'));
            return;
          }
          
          if (!email || !email.includes('@') || !email.includes('.')) {
            reject(new Error('Please enter a valid email address'));
            return;
          }
          
          if (!password || password.length < 6) {
            reject(new Error('Password must be at least 6 characters long'));
            return;
          }

          const users = getOfflineData('users', {});
          
          // Check if user already exists
          const emailKey = email.toLowerCase().trim();
          if (users[emailKey]) {
            reject(new Error('An account with this email already exists'));
            return;
          }

          // Create comprehensive user profile
          const userId = uuidv4();
          const now = new Date().toISOString();
          const newUser = {
            id: userId,
            name: name.trim(),
            email: emailKey,
            password: password, // In a real app, this should be hashed
            createdAt: now,
            lastLoginAt: now,
            settings: {
              theme: 'light',
              notifications: true,
              reminders: true,
              measurementUnit: 'imperial',
              language: 'en',
              dataBackup: true
            },
            profile: {
              isComplete: false,
              hasCompletedOnboarding: false
            }
          };

          users[emailKey] = newUser;
          saveOfflineData('users', users);
          
          // Set current user
          localStorage.setItem('babysteps_current_user', userId);
          
          // Generate access token
          const token = `standalone_token_${userId}_${Date.now()}`;
          
          console.log('✅ User registered successfully in standalone mode:', emailKey);
          resolve({
            data: {
              access_token: token,
              user: {
                id: userId,
                name: newUser.name,
                email: newUser.email
              }
            }
          });
        } catch (error) {
          reject(error);
        }
      }, 300); // Faster response for standalone app
    });
  },

  // Babies management
  getBabies: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const currentUserId = localStorage.getItem('babysteps_current_user');
        const babies = getOfflineData('babies', {});
        
        // Babies are stored as babies[userId] = [array of babies]
        const userBabies = babies[currentUserId] || [];
        
        console.log('👶 Retrieved babies for user:', currentUserId, userBabies);
        resolve({
          data: userBabies
        });
      }, 300);
    });
  },

  // Enhanced baby management with comprehensive customization
  createBaby: async (babyData) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const currentUserId = localStorage.getItem('babysteps_current_user');
          
          if (!currentUserId) {
            reject(new Error('No authenticated user found'));
            return;
          }

          // Comprehensive validation
          if (!babyData.name || babyData.name.trim().length < 1) {
            reject(new Error('Baby name is required'));
            return;
          }

          if (!babyData.birth_date) {
            reject(new Error('Birth date is required'));
            return;
          }

          const babyId = uuidv4();
          const now = new Date().toISOString();
          
          // Create comprehensive baby profile
          const newBaby = {
            id: babyId,
            name: babyData.name.trim(),
            birth_date: babyData.birth_date,
            gender: babyData.gender || 'not_specified',
            profile_image: babyData.profile_image || null,
            user_id: currentUserId,
            createdAt: now,
            updatedAt: now,
            
            // Enhanced profile data
            details: {
              birth_time: babyData.birth_time || null,
              birth_weight: babyData.birth_weight || null,
              birth_length: babyData.birth_length || null,
              blood_type: babyData.blood_type || null,
              allergies: babyData.allergies || [],
              medical_conditions: babyData.medical_conditions || [],
              pediatrician: babyData.pediatrician || null,
              insurance_info: babyData.insurance_info || null
            },
            
            // Customization options
            preferences: {
              feeding_schedule: babyData.feeding_schedule || 'flexible',
              sleep_routine: babyData.sleep_routine || 'flexible',
              measurement_unit: babyData.measurement_unit || 'imperial',
              temperature_unit: babyData.temperature_unit || 'fahrenheit'
            },
            
            // Tracking settings
            tracking: {
              growth_tracking: true,
              milestone_tracking: true,
              feeding_tracking: true,
              sleep_tracking: true,
              diaper_tracking: true,
              mood_tracking: false,
              photo_timeline: true
            },
            
            // Statistics
            stats: {
              total_activities: 0,
              last_activity: null,
              milestones_reached: 0
            }
          };

          const babies = getOfflineData('babies', {});
          if (!babies[currentUserId]) {
            babies[currentUserId] = [];
          }
          babies[currentUserId].push(newBaby);
          saveOfflineData('babies', babies);

          // Initialize related data structures
          this.initializeBabyData(babyId, currentUserId);

          console.log('✅ Baby profile created successfully:', newBaby.name);
          resolve({ data: newBaby });
        } catch (error) {
          reject(error);
        }
      }, 300);
    });
  },

  // Initialize related data for new baby
  initializeBabyData: (babyId, userId) => {
    // Initialize milestones
    const milestones = getOfflineData('milestones', {});
    if (!milestones[babyId]) {
      milestones[babyId] = this.getDefaultMilestones();
      saveOfflineData('milestones', milestones);
    }

    // Initialize growth data
    const growthData = getOfflineData('growth_data', {});
    if (!growthData[babyId]) {
      growthData[babyId] = [];
      saveOfflineData('growth_data', growthData);
    }

    // Initialize photo timeline
    const photos = getOfflineData('photos', {});
    if (!photos[babyId]) {
      photos[babyId] = [];
      saveOfflineData('photos', photos);
    }

    console.log('✅ Baby data structures initialized for', babyId);
  },

  // Get default milestones template
  getDefaultMilestones: () => ({
    motor_skills: [
      { name: 'Holds head up', expected_age_months: 2, achieved: false, date_achieved: null },
      { name: 'Rolls over', expected_age_months: 4, achieved: false, date_achieved: null },
      { name: 'Sits without support', expected_age_months: 6, achieved: false, date_achieved: null },
      { name: 'Crawls', expected_age_months: 8, achieved: false, date_achieved: null },
      { name: 'Walks independently', expected_age_months: 12, achieved: false, date_achieved: null }
    ],
    social_skills: [
      { name: 'First smile', expected_age_months: 2, achieved: false, date_achieved: null },
      { name: 'Laughs', expected_age_months: 4, achieved: false, date_achieved: null },
      { name: 'Responds to name', expected_age_months: 6, achieved: false, date_achieved: null },
      { name: 'Plays peek-a-boo', expected_age_months: 8, achieved: false, date_achieved: null },
      { name: 'Waves bye-bye', expected_age_months: 10, achieved: false, date_achieved: null }
    ],
    communication: [
      { name: 'Coos and babbles', expected_age_months: 3, achieved: false, date_achieved: null },
      { name: 'Says "mama" or "dada"', expected_age_months: 8, achieved: false, date_achieved: null },
      { name: 'First word', expected_age_months: 12, achieved: false, date_achieved: null },
      { name: 'Follows simple instructions', expected_age_months: 12, achieved: false, date_achieved: null }
    ]
  }),

  updateBaby: async (babyId, updates) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const currentUserId = localStorage.getItem('babysteps_current_user');
          
          if (!currentUserId) {
            reject(new Error('No authenticated user found'));
            return;
          }

          const babies = getOfflineData('babies', {});
          const userBabies = babies[currentUserId] || [];
          
          const babyIndex = userBabies.findIndex(baby => baby.id === babyId);
          if (babyIndex === -1) {
            reject(new Error('Baby not found'));
            return;
          }
          
          // Update the baby in the array
          userBabies[babyIndex] = { 
            ...userBabies[babyIndex], 
            ...updates,
            updatedAt: new Date().toISOString()
          };
          
          // Save the updated babies array
          babies[currentUserId] = userBabies;
          saveOfflineData('babies', babies);
          
          console.log('✅ Baby updated successfully:', userBabies[babyIndex].name);
          resolve({
            data: userBabies[babyIndex]
          });
        } catch (error) {
          reject(error);
        }
      }, 300);
    });
  },

  // Enhanced activity tracking with comprehensive logging
  logActivity: async (activityData) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const currentUserId = localStorage.getItem('babysteps_current_user');
          
          if (!currentUserId) {
            reject(new Error('No authenticated user found'));
            return;
          }

          // Validation
          if (!activityData.type) {
            reject(new Error('Activity type is required'));
            return;
          }

          if (!activityData.baby_id) {
            reject(new Error('Baby ID is required'));
            return;
          }

          const activityId = uuidv4();
          const now = new Date().toISOString();
          
          // Create comprehensive activity record
          const newActivity = {
            id: activityId,
            type: activityData.type,
            baby_id: activityData.baby_id,
            user_id: currentUserId,
            timestamp: activityData.timestamp || now,
            createdAt: now,
            
            // Core activity data
            notes: activityData.notes || '',
            duration: activityData.duration || null,
            amount: activityData.amount || null,
            unit: activityData.unit || null,
            
            // Enhanced tracking data
            details: {
              mood: activityData.mood || null,
              temperature: activityData.temperature || null,
              medication: activityData.medication || null,
              location: activityData.location || 'home',
              weather: activityData.weather || null,
              photos: activityData.photos || [],
              tags: activityData.tags || []
            },
            
            // Type-specific data
            type_data: offlineAPI.getTypeSpecificData(activityData.type, activityData),
            
            // Metadata
            metadata: {
              app_version: '1.0.0',
              device: navigator.userAgent || 'unknown',
              timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
            }
          };

          // Save activity
          const activities = getOfflineData('activities', {});
          if (!activities[currentUserId]) {
            activities[currentUserId] = [];
          }
          activities[currentUserId].push(newActivity);
          saveOfflineData('activities', activities);

          // Update baby statistics
          this.updateBabyStats(activityData.baby_id, newActivity);

          // Check for milestone triggers
          this.checkMilestoneTriggers(activityData.baby_id, newActivity);

          console.log('✅ Activity logged successfully:', activityData.type);
          resolve({ data: newActivity });
        } catch (error) {
          reject(error);
        }
      }, 200);
    });
  },

  // Get type-specific data structure
  getTypeSpecificData: (type, activityData) => {
    const typeData = {};
    
    switch (type) {
      case 'feeding':
        typeData.method = activityData.feeding_method || 'bottle';
        typeData.breast_side = activityData.breast_side || null;
        typeData.formula_type = activityData.formula_type || null;
        typeData.solid_food = activityData.solid_food || null;
        break;
        
      case 'sleep':
        typeData.sleep_type = activityData.sleep_type || 'nap';
        typeData.sleep_quality = activityData.sleep_quality || null;
        typeData.sleep_location = activityData.sleep_location || 'crib';
        break;
        
      case 'diaper':
        typeData.diaper_type = activityData.diaper_type || 'wet';
        typeData.color = activityData.color || null;
        typeData.consistency = activityData.consistency || null;
        break;
        
      case 'growth':
        typeData.measurement_type = activityData.measurement_type || 'weight';
        typeData.value = activityData.value || null;
        typeData.percentile = activityData.percentile || null;
        break;
        
      case 'milestone':
        typeData.milestone_category = activityData.milestone_category || 'motor';
        typeData.milestone_name = activityData.milestone_name || '';
        break;
        
      case 'medical':
        typeData.appointment_type = activityData.appointment_type || 'checkup';
        typeData.provider = activityData.provider || null;
        typeData.diagnosis = activityData.diagnosis || null;
        typeData.treatment = activityData.treatment || null;
        break;
    }
    
    return typeData;
  },

  // Update baby statistics after activity logging
  updateBabyStats: (babyId, activity) => {
    try {
      const currentUserId = localStorage.getItem('babysteps_current_user');
      const babies = getOfflineData('babies', {});
      
      if (babies[currentUserId]) {
        const babyIndex = babies[currentUserId].findIndex(baby => baby.id === babyId);
        if (babyIndex !== -1) {
          babies[currentUserId][babyIndex].stats.total_activities += 1;
          babies[currentUserId][babyIndex].stats.last_activity = activity.timestamp;
          babies[currentUserId][babyIndex].updatedAt = new Date().toISOString();
          
          saveOfflineData('babies', babies);
        }
      }
    } catch (error) {
      console.error('Failed to update baby stats:', error);
    }
  },

  // Check for milestone triggers
  checkMilestoneTriggers: (babyId, activity) => {
    try {
      // This would contain logic to automatically detect milestones
      // based on activities (e.g., first solid food, first sleep through night)
      if (activity.type === 'milestone') {
        const milestones = getOfflineData('milestones', {});
        if (milestones[babyId] && activity.type_data.milestone_name) {
          // Mark milestone as achieved
          // Implementation would depend on milestone structure
          console.log('🎉 Milestone achieved:', activity.type_data.milestone_name);
        }
      }
    } catch (error) {
      console.error('Failed to check milestones:', error);
    }
  },

  // Enhanced activity retrieval with filtering and sorting
  getActivities: async (babyId = null, filters = {}) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        try {
          const currentUserId = localStorage.getItem('babysteps_current_user');
          const activities = getOfflineData('activities', {});
          
          let userActivities = activities[currentUserId] || [];
          
          // Filter by baby ID
          if (babyId) {
            userActivities = userActivities.filter(activity => activity.baby_id === babyId);
          }
          
          // Apply additional filters
          if (filters.type) {
            userActivities = userActivities.filter(activity => activity.type === filters.type);
          }
          
          if (filters.startDate) {
            userActivities = userActivities.filter(activity => 
              new Date(activity.timestamp) >= new Date(filters.startDate)
            );
          }
          
          if (filters.endDate) {
            userActivities = userActivities.filter(activity => 
              new Date(activity.timestamp) <= new Date(filters.endDate)
            );
          }
          
          // Sort by timestamp (newest first)
          userActivities.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
          
          // Limit results if specified
          if (filters.limit) {
            userActivities = userActivities.slice(0, filters.limit);
          }
          
          resolve({ data: userActivities });
        } catch (error) {
          resolve({ data: [] });
        }
      }, 200);
    });
  },

  // Get activity statistics
  getActivityStats: async (babyId, period = 'week') => {
    return new Promise((resolve) => {
      setTimeout(() => {
        try {
          const activities = offlineAPI.getActivities(babyId);
          
          // Calculate statistics based on period
          const stats = {
            total_activities: activities.data.length,
            by_type: {},
            by_day: {},
            trends: {}
          };
          
          activities.data.forEach(activity => {
            // Count by type
            stats.by_type[activity.type] = (stats.by_type[activity.type] || 0) + 1;
            
            // Count by day
            const day = activity.timestamp.split('T')[0];
            stats.by_day[day] = (stats.by_day[day] || 0) + 1;
          });
          
          resolve({ data: stats });
        } catch (error) {
          resolve({ data: null });
        }
      }, 100);
    });
  },

  // Legacy createActivity function for backward compatibility
  createActivity: async (activityData) => {
    return offlineAPI.logActivity(activityData);
  },

  // Food research (with direct AI integration via device internet)
  foodResearch: async (query, babyAgeMonths = 6) => {
    try {
      console.log('🔬 Standalone mode: Using direct AI for food research:', query);
      
      // Use direct AI service via device internet connection
      const response = await aiService.researchFood(query, babyAgeMonths);
      console.log('✅ Direct AI food research successful');
      return { data: response };
    } catch (error) {
      console.log('⚠️ Direct AI failed, using enhanced fallback responses');
      
      // Fallback to mock responses if AI fails
      return new Promise((resolve) => {
        setTimeout(() => {
          const responses = {
            honey: {
              answer: "🚫 Honey should NOT be given to babies under 12 months old due to the risk of infant botulism. Botulism spores can be found in honey and can cause serious illness in infants whose immune systems aren't fully developed.",
              safety_level: "avoid",
              age_recommendation: "12+ months only",
              sources: ["American Academy of Pediatrics", "CDC Guidelines"]
            },
            strawberries: {
              answer: "🍓 Fresh strawberries can be introduced around 6 months when baby starts solids. Cut into small, age-appropriate pieces to prevent choking. Start with small amounts and watch for allergic reactions.",
              safety_level: "safe", 
              age_recommendation: "6+ months",
              sources: ["Pediatric Nutrition Guidelines", "AAP Feeding Guidelines"]
            },
            nuts: {
              answer: "🥜 Whole nuts are a choking hazard for babies. Nut butters can be introduced around 6 months but should be thinned with water or breast milk. Watch carefully for allergic reactions.",
              safety_level: "caution",
              age_recommendation: "6+ months (as nut butter only)",
              sources: ["Food Allergy Research Guidelines"]
            }
          };
          
          // Simple keyword matching
          let response = null;
          for (const [keyword, resp] of Object.entries(responses)) {
            if (query.toLowerCase().includes(keyword)) {
              response = resp;
              break;
            }
          }
          
          if (!response) {
            response = {
              answer: `For safety information about "${query}", please consult your pediatrician. AI service is temporarily unavailable.`,
              safety_level: "consult_doctor",
              age_recommendation: "Ask your doctor",
              sources: ["Offline Mode Fallback"]
            };
          }
          
          resolve({ data: response });
        }, 800);
      });
    }
  },

  // Meal planning (with direct AI integration via device internet)
  mealSearch: async (query, ageMonths = 6) => {
    try {
      console.log('🍽️ Standalone mode: Using direct AI for meal planning:', query);
      
      // Use direct AI service via device internet connection
      const response = await aiService.generateMealPlan(query, ageMonths);
      console.log('✅ Direct AI meal planning successful');
      return { data: response };
    } catch (error) {
      console.log('⚠️ Direct AI failed, using enhanced fallback meal suggestions');
      
      // Fallback to mock responses if AI fails
      return new Promise((resolve) => {
        setTimeout(() => {
          const meals = [
            {
              name: "Mashed Banana",
              ingredients: ["1 ripe banana"],
              instructions: ["Mash banana with fork until smooth", "Ensure no lumps for younger babies", "Serve at room temperature"],
              age_appropriate: "6+ months",
              prep_time: "2 minutes",
              safety_tips: ["Always test temperature", "Supervise eating"]
            },
            {
              name: "Sweet Potato Puree",
              ingredients: ["1 sweet potato", "Water or breast milk"],
              instructions: ["Steam sweet potato until very soft (15-20 min)", "Mash with liquid to desired consistency", "Cool before serving"],
              age_appropriate: "6+ months", 
              prep_time: "25 minutes",
              safety_tips: ["Check temperature", "Start with thin consistency"]
            },
            {
              name: "Avocado Mash",
              ingredients: ["1/2 ripe avocado"],
              instructions: ["Mash avocado until smooth", "Add breast milk if needed for consistency", "Serve immediately"],
              age_appropriate: "6+ months",
              prep_time: "1 minute", 
              safety_tips: ["Use very ripe avocado", "Serve fresh"]
            },
            {
              name: "Soft Scrambled Eggs",
              ingredients: ["1 egg", "1 tbsp milk", "Small amount of butter"],
              instructions: ["Whisk egg with milk", "Cook on very low heat, stirring constantly", "Ensure very soft texture", "Cool before serving"],
              age_appropriate: "8+ months",
              prep_time: "5 minutes",
              safety_tips: ["Cook thoroughly", "Cool to room temperature", "Watch for allergies"]
            }
          ];
          
          resolve({
            data: {
              results: meals,
              query,
              age_months: ageMonths,
              source: "Offline Mode Fallback"
            }
          });
        }, 600);
      });
    }
  },

  // General research (with direct AI integration via device internet)
  research: async (query) => {
    try {
      console.log('📚 Standalone mode: Using direct AI for research:', query);
      
      // Use direct AI service via device internet connection
      const response = await aiService.research(query);
      console.log('✅ Direct AI research successful');
      return { data: response };
    } catch (error) {
      console.log('⚠️ Direct AI failed, using enhanced fallback response');
      
      // Fallback response if AI fails
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            data: {
              answer: `I'm currently in offline mode with limited AI capabilities. For comprehensive information about "${query}", please try again when you have an internet connection or consult your pediatrician for medical advice.`,
              source: "Offline Mode - Limited AI",
              suggestions: [
                "Check your internet connection",
                "Try again later",
                "Consult your pediatrician for medical questions",
                "Use the app's other features while offline"
              ]
            }
          });
        }, 500);
      });
    }
  }
};

// Export flag to check if offline mode is active
export const isOfflineMode = () => {
  return shouldUseOfflineMode();
};