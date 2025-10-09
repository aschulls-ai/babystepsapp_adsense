// Complete offline storage system for Baby Steps
import { v4 as uuidv4 } from 'uuid';

const STORAGE_KEYS = {
  USERS: 'babysteps_users',
  CURRENT_USER: 'babysteps_current_user',
  BABIES: 'babysteps_babies',
  ACTIVITIES: 'babysteps_activities',
  SETTINGS: 'babysteps_settings'
};

// Storage utilities
const getFromStorage = (key, defaultValue = null) => {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch (error) {
    console.error(`Error reading ${key} from storage:`, error);
    return defaultValue;
  }
};

const saveToStorage = (key, data) => {
  try {
    localStorage.setItem(key, JSON.stringify(data));
    return true;
  } catch (error) {
    console.error(`Error saving ${key} to storage:`, error);
    return false;
  }
};

// User management
export const offlineAuth = {
  register: (email, password, name) => {
    const users = getFromStorage(STORAGE_KEYS.USERS, {});
    
    if (users[email]) {
      throw new Error('Email already registered');
    }
    
    const user = {
      id: uuidv4(),
      email,
      name,
      password, // In production, this would be hashed
      createdAt: new Date().toISOString(),
      emailVerified: true
    };
    
    users[email] = user;
    saveToStorage(STORAGE_KEYS.USERS, users);
    
    return { user: { id: user.id, email: user.email, name: user.name } };
  },

  login: (email, password) => {
    const users = getFromStorage(STORAGE_KEYS.USERS, {});
    const user = users[email];
    
    if (!user || user.password !== password) {
      throw new Error('Invalid credentials');
    }
    
    const currentUser = { id: user.id, email: user.email, name: user.name };
    saveToStorage(STORAGE_KEYS.CURRENT_USER, currentUser);
    
    return { user: currentUser, token: `offline_token_${user.id}` };
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
    return true;
  },

  getCurrentUser: () => {
    return getFromStorage(STORAGE_KEYS.CURRENT_USER);
  },

  updateProfile: (userId, updates) => {
    const users = getFromStorage(STORAGE_KEYS.USERS, {});
    const currentUser = getFromStorage(STORAGE_KEYS.CURRENT_USER);
    
    if (!currentUser || currentUser.id !== userId) {
      throw new Error('Unauthorized');
    }
    
    // Find user by ID in users object
    for (const email in users) {
      if (users[email].id === userId) {
        users[email] = { ...users[email], ...updates };
        saveToStorage(STORAGE_KEYS.USERS, users);
        
        // Update current user session
        const updatedUser = { ...currentUser, ...updates };
        saveToStorage(STORAGE_KEYS.CURRENT_USER, updatedUser);
        return updatedUser;
      }
    }
    
    throw new Error('User not found');
  }
};

// Baby management
export const offlineBabies = {
  getAll: (userId) => {
    const babies = getFromStorage(STORAGE_KEYS.BABIES, {});
    return Object.values(babies).filter(baby => baby.userId === userId);
  },

  create: (userId, babyData) => {
    const babies = getFromStorage(STORAGE_KEYS.BABIES, {});
    const baby = {
      id: uuidv4(),
      ...babyData,
      userId,
      createdAt: new Date().toISOString()
    };
    
    babies[baby.id] = baby;
    saveToStorage(STORAGE_KEYS.BABIES, babies);
    return baby;
  },

  update: (userId, babyId, updates) => {
    const babies = getFromStorage(STORAGE_KEYS.BABIES, {});
    const baby = babies[babyId];
    
    if (!baby || baby.userId !== userId) {
      throw new Error('Baby not found or unauthorized');
    }
    
    babies[babyId] = { ...baby, ...updates, updatedAt: new Date().toISOString() };
    saveToStorage(STORAGE_KEYS.BABIES, babies);
    return babies[babyId];
  },

  delete: (userId, babyId) => {
    const babies = getFromStorage(STORAGE_KEYS.BABIES, {});
    const baby = babies[babyId];
    
    if (!baby || baby.userId !== userId) {
      throw new Error('Baby not found or unauthorized');
    }
    
    delete babies[babyId];
    saveToStorage(STORAGE_KEYS.BABIES, babies);
    
    // Also delete associated activities
    const activities = getFromStorage(STORAGE_KEYS.ACTIVITIES, {});
    Object.keys(activities).forEach(activityId => {
      if (activities[activityId].babyId === babyId) {
        delete activities[activityId];
      }
    });
    saveToStorage(STORAGE_KEYS.ACTIVITIES, activities);
    
    return true;
  }
};

// Activity management
export const offlineActivities = {
  getAll: (userId) => {
    const activities = getFromStorage(STORAGE_KEYS.ACTIVITIES, {});
    const userBabies = offlineBabies.getAll(userId);
    const userBabyIds = userBabies.map(baby => baby.id);
    
    return Object.values(activities)
      .filter(activity => userBabyIds.includes(activity.babyId))
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  },

  create: (userId, activityData) => {
    // Verify baby belongs to user
    const babies = getFromStorage(STORAGE_KEYS.BABIES, {});
    const baby = babies[activityData.babyId];
    
    if (!baby || baby.userId !== userId) {
      throw new Error('Invalid baby ID or unauthorized');
    }
    
    const activities = getFromStorage(STORAGE_KEYS.ACTIVITIES, {});
    const activity = {
      id: uuidv4(),
      ...activityData,
      timestamp: new Date().toISOString(),
      userId
    };
    
    activities[activity.id] = activity;
    saveToStorage(STORAGE_KEYS.ACTIVITIES, activities);
    return activity;
  },

  update: (userId, activityId, updates) => {
    const activities = getFromStorage(STORAGE_KEYS.ACTIVITIES, {});
    const activity = activities[activityId];
    
    if (!activity || activity.userId !== userId) {
      throw new Error('Activity not found or unauthorized');
    }
    
    activities[activityId] = { ...activity, ...updates, updatedAt: new Date().toISOString() };
    saveToStorage(STORAGE_KEYS.ACTIVITIES, activities);
    return activities[activityId];
  },

  delete: (userId, activityId) => {
    const activities = getFromStorage(STORAGE_KEYS.ACTIVITIES, {});
    const activity = activities[activityId];
    
    if (!activity || activity.userId !== userId) {
      throw new Error('Activity not found or unauthorized');
    }
    
    delete activities[activityId];
    saveToStorage(STORAGE_KEYS.ACTIVITIES, activities);
    return true;
  }
};

// Settings management
export const offlineSettings = {
  get: (userId) => {
    const allSettings = getFromStorage(STORAGE_KEYS.SETTINGS, {});
    return allSettings[userId] || {
      theme: 'light',
      notifications: true,
      language: 'en',
      units: 'metric'
    };
  },

  update: (userId, settings) => {
    const allSettings = getFromStorage(STORAGE_KEYS.SETTINGS, {});
    allSettings[userId] = { ...allSettings[userId], ...settings };
    saveToStorage(STORAGE_KEYS.SETTINGS, allSettings);
    return allSettings[userId];
  }
};

// Initialize demo data if first time
export const initializeDemoData = () => {
  const users = getFromStorage(STORAGE_KEYS.USERS, {});
  
  if (Object.keys(users).length === 0) {
    console.log('🚀 Initializing offline demo data...');
    
    // Create demo user
    try {
      const demoUser = offlineAuth.register('demo@babysteps.com', 'demo123', 'Demo Parent');
      
      // Create demo baby
      const demoBaby = offlineBabies.create(demoUser.user.id, {
        name: 'Emma',
        birth_date: '2024-01-15',
        gender: 'girl'
      });
      
      // Create demo activities
      const activities = [
        { type: 'feeding', notes: 'Formula feeding - 4oz', babyId: demoBaby.id },
        { type: 'sleep', notes: 'Nap time - 2 hours', babyId: demoBaby.id },
        { type: 'diaper', notes: 'Wet diaper changed', babyId: demoBaby.id },
        { type: 'pumping', notes: 'Breast pump session - 5oz', babyId: demoBaby.id }
      ];
      
      activities.forEach(activity => {
        offlineActivities.create(demoUser.user.id, activity);
      });
      
      console.log('✅ Demo data initialized successfully');
    } catch (error) {
      console.error('❌ Error initializing demo data:', error);
    }
  }
};

// Data export/import for backup
export const dataManagement = {
  exportData: (userId) => {
    const userData = {
      user: offlineAuth.getCurrentUser(),
      babies: offlineBabies.getAll(userId),
      activities: offlineActivities.getAll(userId),
      settings: offlineSettings.get(userId),
      exportDate: new Date().toISOString()
    };
    
    return JSON.stringify(userData, null, 2);
  },

  importData: (jsonData, userId) => {
    try {
      const data = JSON.parse(jsonData);
      
      // Import babies
      data.babies?.forEach(baby => {
        const babies = getFromStorage(STORAGE_KEYS.BABIES, {});
        babies[baby.id] = { ...baby, userId };
      });
      
      // Import activities
      data.activities?.forEach(activity => {
        const activities = getFromStorage(STORAGE_KEYS.ACTIVITIES, {});
        activities[activity.id] = { ...activity, userId };
      });
      
      // Import settings
      if (data.settings) {
        offlineSettings.update(userId, data.settings);
      }
      
      return true;
    } catch (error) {
      console.error('Import failed:', error);
      throw new Error('Invalid backup data');
    }
  }
};