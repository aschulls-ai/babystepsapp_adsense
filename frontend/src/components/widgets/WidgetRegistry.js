import BabyProfileWidget from './BabyProfileWidget';
import RecentActivitiesWidget from './RecentActivitiesWidget';
import FoodSafetyQuickWidget from './FoodSafetyQuickWidget';
import EmergencyTrainingWidget from './EmergencyTrainingWidget';
import MealIdeasWidget from './MealIdeasWidget';
import QuickStatsWidget from './QuickStatsWidget';
import MilestonesWidget from './MilestonesWidget';

// Widget registry - maps widget types to their components
export const WidgetRegistry = {
  baby_profile: BabyProfileWidget,
  recent_activities: RecentActivitiesWidget,
  food_safety_quick: FoodSafetyQuickWidget,
  emergency_training: EmergencyTrainingWidget,
  meal_ideas: MealIdeasWidget,
  quick_stats: QuickStatsWidget,
  growth_charts: QuickStatsWidget, // Placeholder - using QuickStats for now
  research_bookmarks: QuickStatsWidget, // Placeholder - using QuickStats for now
};

// Get widget component by type
export const getWidgetComponent = (type) => {
  return WidgetRegistry[type] || null;
};

// Default widget configurations
export const DefaultWidgetConfigs = {
  baby_profile: {
    defaultPosition: { x: 0, y: 0, w: 4, h: 4 },
    minSize: { w: 3, h: 3 },
    maxSize: { w: 6, h: 6 }
  },
  recent_activities: {
    defaultPosition: { x: 4, y: 0, w: 4, h: 4 },
    minSize: { w: 4, h: 4 },
    maxSize: { w: 8, h: 8 }
  },
  food_safety_quick: {
    defaultPosition: { x: 0, y: 4, w: 4, h: 3 },
    minSize: { w: 3, h: 3 },
    maxSize: { w: 6, h: 4 }
  },
  emergency_training: {
    defaultPosition: { x: 4, y: 4, w: 4, h: 3 },
    minSize: { w: 3, h: 3 },
    maxSize: { w: 6, h: 4 }
  },
  meal_ideas: {
    defaultPosition: { x: 8, y: 0, w: 4, h: 4 },
    minSize: { w: 3, h: 3 },
    maxSize: { w: 6, h: 5 }
  },
  quick_stats: {
    defaultPosition: { x: 8, y: 4, w: 4, h: 3 },
    minSize: { w: 3, h: 2 },
    maxSize: { w: 6, h: 4 }
  },
  growth_charts: {
    defaultPosition: { x: 0, y: 7, w: 6, h: 4 },
    minSize: { w: 4, h: 3 },
    maxSize: { w: 8, h: 6 }
  },
  research_bookmarks: {
    defaultPosition: { x: 6, y: 7, w: 6, h: 4 },
    minSize: { w: 3, h: 3 },
    maxSize: { w: 6, h: 5 }
  }
};

export default WidgetRegistry;