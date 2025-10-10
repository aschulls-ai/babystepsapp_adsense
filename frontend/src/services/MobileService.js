import { Capacitor } from '@capacitor/core';
import { Preferences } from '@capacitor/preferences';
import { PushNotifications } from '@capacitor/push-notifications';
import { LocalNotifications } from '@capacitor/local-notifications';
import { Network } from '@capacitor/network';
import { App } from '@capacitor/app';

class MobileService {
  constructor() {
    this.isNative = Capacitor.isNativePlatform();
    this.isOnline = true;
    this.syncQueue = [];
    this.initializeServices();
  }

  async initializeServices() {
    if (this.isNative) {
      // Temporarily disabled push notifications to prevent crashes
      // await this.setupPushNotifications();
      await this.setupNetworkListener();
      await this.setupAppStateListener();
    }
  }

  // === OFFLINE STORAGE ===
  async setItem(key, value) {
    try {
      const data = typeof value === 'string' ? value : JSON.stringify(value);
      if (this.isNative) {
        await Preferences.set({ key, value: data });
      } else {
        localStorage.setItem(key, data);
      }
    } catch (error) {
      console.error('Error storing data:', error);
    }
  }

  async getItem(key) {
    try {
      if (this.isNative) {
        const { value } = await Preferences.get({ key });
        return value;
      } else {
        return localStorage.getItem(key);
      }
    } catch (error) {
      console.error('Error retrieving data:', error);
      return null;
    }
  }

  async removeItem(key) {
    try {
      if (this.isNative) {
        await Preferences.remove({ key });
      } else {
        localStorage.removeItem(key);
      }
    } catch (error) {
      console.error('Error removing data:', error);
    }
  }

  async clear() {
    try {
      if (this.isNative) {
        await Preferences.clear();
      } else {
        localStorage.clear();
      }
    } catch (error) {
      console.error('Error clearing storage:', error);
    }
  }

  // === OFFLINE DATA SYNC ===
  async saveOfflineData(type, data) {
    const timestamp = new Date().toISOString();
    const offlineData = {
      id: `offline_${timestamp}`,
      type,
      data,
      timestamp,
      synced: false
    };

    // Get existing offline data
    const existingData = await this.getOfflineData();
    existingData.push(offlineData);

    await this.setItem('offline_data', existingData);
    
    // Try to sync if online
    if (this.isOnline) {
      this.syncOfflineData();
    }

    return offlineData;
  }

  async getOfflineData() {
    const data = await this.getItem('offline_data');
    return data ? JSON.parse(data) : [];
  }

  async syncOfflineData() {
    const offlineData = await this.getOfflineData();
    const unsyncedData = offlineData.filter(item => !item.synced);

    for (const item of unsyncedData) {
      try {
        // Sync with backend API
        await this.syncSingleItem(item);
        
        // Mark as synced
        item.synced = true;
      } catch (error) {
        console.error('Sync failed for item:', item.id, error);
      }
    }

    // Update offline data
    await this.setItem('offline_data', offlineData);
  }

  async syncSingleItem(item) {
    // Disabled for standalone mode - all data stays local
    console.log('🏠 Standalone mode: Data sync skipped (offline mode)', item.type);
    return;
  }

  // === PUSH NOTIFICATIONS ===
  async setupPushNotifications() {
    if (!this.isNative) return;

    try {
      // Request permission
      const result = await PushNotifications.requestPermissions();
      
      if (result.receive === 'granted') {
        // Register for push notifications
        await PushNotifications.register();

        // Listen for registration
        PushNotifications.addListener('registration', (token) => {
          console.log('Push registration success, token: ' + token.value);
          this.sendTokenToServer(token.value);
        });

        // Listen for registration errors
        PushNotifications.addListener('registrationError', (err) => {
          console.error('Registration error: ', err.error);
        });

        // Listen for push notifications
        PushNotifications.addListener('pushNotificationReceived', (notification) => {
          console.log('Push notification received: ', notification);
          this.handlePushNotification(notification);
        });

        // Handle notification tap
        PushNotifications.addListener('pushNotificationActionPerformed', (notification) => {
          console.log('Push notification action performed', notification.actionId, notification.inputValue);
        });
      }
    } catch (error) {
      console.error('Push notification setup failed:', error);
    }
  }

  async sendTokenToServer(token) {
    // Disabled for standalone mode - no server sync needed
    console.log('🏠 Standalone mode: Push token registration skipped (offline mode)');
    return;
  }

  handlePushNotification(notification) {
    // Handle different notification types
    switch (notification.data?.type) {
      case 'feeding_reminder':
        this.showFeedingReminder(notification);
        break;
      case 'milestone_celebration':
        this.showMilestoneNotification(notification);
        break;
      default:
        console.log('Unknown notification type:', notification);
    }
  }

  // === LOCAL NOTIFICATIONS ===
  async scheduleLocalNotification(title, body, scheduledAt, data = {}) {
    if (!this.isNative) return;

    try {
      await LocalNotifications.schedule({
        notifications: [{
          title,
          body,
          id: Date.now(),
          schedule: { at: new Date(scheduledAt) },
          sound: 'beep.wav',
          attachments: [],
          actionTypeId: '',
          extra: data
        }]
      });
    } catch (error) {
      console.error('Failed to schedule notification:', error);
    }
  }

  async showFeedingReminder(notification) {
    await LocalNotifications.schedule({
      notifications: [{
        title: 'Feeding Time! 🍼',
        body: notification.body || 'Time for your baby\'s next feeding',
        id: Date.now(),
        sound: 'beep.wav',
        extra: { type: 'feeding_reminder' }
      }]
    });
  }

  async showMilestoneNotification(notification) {
    await LocalNotifications.schedule({
      notifications: [{
        title: 'Milestone Achievement! ⭐',
        body: notification.body || 'Your baby reached a new milestone!',
        id: Date.now(),
        sound: 'beep.wav',
        extra: { type: 'milestone' }
      }]
    });
  }

  // === NETWORK MONITORING ===
  async setupNetworkListener() {
    if (!this.isNative) return;

    Network.addListener('networkStatusChange', (status) => {
      this.isOnline = status.connected;
      
      if (status.connected) {
        console.log('Network reconnected - syncing offline data');
        this.syncOfflineData();
      } else {
        console.log('Network disconnected - switching to offline mode');
      }
    });

    // Get initial network status
    const status = await Network.getStatus();
    this.isOnline = status.connected;
  }

  // === APP STATE MANAGEMENT ===
  async setupAppStateListener() {
    if (!this.isNative) return;

    App.addListener('appStateChange', ({ isActive }) => {
      if (isActive) {
        // App became active - sync any offline data
        if (this.isOnline) {
          this.syncOfflineData();
        }
      }
    });

    App.addListener('backButton', ({ canGoBack }) => {
      if (!canGoBack) {
        App.exitApp();
      }
    });
  }

  // === UTILITY METHODS ===
  getNetworkStatus() {
    return this.isOnline;
  }

  async getBatteryInfo() {
    if (this.isNative) {
      try {
        const info = await Device.getBatteryInfo();
        return info;
      } catch (error) {
        console.error('Failed to get battery info:', error);
        return null;
      }
    }
    return null;
  }

  async getDeviceInfo() {
    if (this.isNative) {
      try {
        const info = await Device.getInfo();
        return info;
      } catch (error) {
        console.error('Failed to get device info:', error);
        return null;
      }
    }
    return null;
  }
}

// Export singleton instance
export const mobileService = new MobileService();
export default MobileService;