/**
 * AdMob Service
 * Handles native AdMob integration for Android/iOS
 * Manages banner ads, interstitial ads, and ad removal status
 */

import { AdMob, BannerAdOptions, BannerAdSize, BannerAdPosition, AdMobBannerSize } from '@capacitor-community/admob';
import { Capacitor } from '@capacitor/core';
import billingService from './BillingService';

// AdMob Configuration
const ADMOB_CONFIG = {
  appId: 'ca-app-pub-1934622676928053~2387202873',
  
  // Ad Unit IDs - Real production IDs from AdMob Console
  adUnits: {
    // Banner Ads
    banner_dashboard: 'ca-app-pub-1934622676928053/2387202873',
    banner_tracking: 'ca-app-pub-1934622676928053/2031979657',
    banner_ai_assistant: 'ca-app-pub-1934622676928053/3389293355',
    banner_formula: 'ca-app-pub-1934622676928053/7002710080',
    banner_emergency: 'ca-app-pub-1934622676928053/6811138394',
    banner_baby_profile: 'ca-app-pub-1934622676928053/4510803338',
    banner_analysis: 'ca-app-pub-1934622676928053/5505795582',
    
    // Interstitial Ads
    interstitial_app_open: 'ca-app-pub-1934622676928053/3018716129',
    interstitial_page_transition: 'ca-app-pub-1934622676928053/4966222611',
  },
  
  // Test device IDs (add your device ID for testing)
  testDeviceIds: []
};

class AdMobService {
  constructor() {
    this.isInitialized = false;
    this.isNativePlatform = false;
    this.currentBanners = {};
    this.interstitialLoaded = false;
  }

  /**
   * Initialize AdMob
   */
  async initialize() {
    try {
      // Check if running on native platform
      this.isNativePlatform = Capacitor.isNativePlatform();
      
      if (!this.isNativePlatform) {
        console.log('⚠️ Not on native platform, skipping AdMob initialization');
        return false;
      }

      // Initialize AdMob with error handling
      try {
        await AdMob.initialize({
          requestTrackingAuthorization: true,
          testingDevices: ADMOB_CONFIG.testDeviceIds,
          initializeForTesting: false
        });

        this.isInitialized = true;
        console.log('✅ AdMob initialized successfully');
        
        // Preload interstitial ad (non-blocking)
        setTimeout(() => {
          this.preloadInterstitial().catch(err => {
            console.log('⚠️ Could not preload interstitial:', err);
          });
        }, 2000);
        
        return true;
      } catch (initError) {
        console.error('❌ AdMob.initialize() failed:', initError);
        // Mark as not initialized but don't throw
        this.isInitialized = false;
        return false;
      }
    } catch (error) {
      console.error('❌ AdMob initialization failed:', error);
      this.isInitialized = false;
      return false;
    }
  }

  /**
   * Check if ads should be shown (user hasn't purchased ad removal)
   */
  async shouldShowAds() {
    const hasPurchased = billingService.hasAdRemoval();
    return !hasPurchased;
  }

  /**
   * Show banner ad
   */
  async showBanner(adUnitKey, position = BannerAdPosition.BOTTOM_CENTER) {
    try {
      if (!this.isNativePlatform) {
        return false;
      }
      
      if (!this.isInitialized) {
        console.log('⚠️ AdMob not initialized, skipping banner');
        return false;
      }

      // Check if user has purchased ad removal
      if (!(await this.shouldShowAds())) {
        console.log('✅ User has ad removal - skipping banner');
        return false;
      }

      const adUnitId = ADMOB_CONFIG.adUnits[adUnitKey];
      if (!adUnitId) {
        console.error(`❌ Ad unit not found: ${adUnitKey}`);
        return false;
      }

      // Hide any existing banner at this position
      if (this.currentBanners[adUnitKey]) {
        await this.hideBanner(adUnitKey).catch(() => {});
      }

      const options = {
        adId: adUnitId,
        adSize: BannerAdSize.ADAPTIVE_BANNER,
        position: position,
        margin: 0
      };

      await AdMob.showBanner(options);
      this.currentBanners[adUnitKey] = true;
      
      console.log(`✅ Banner ad shown: ${adUnitKey}`);
      return true;
    } catch (error) {
      console.error(`❌ Failed to show banner: ${adUnitKey}`, error);
      // Don't throw - just log and return false
      return false;
    }
  }

  /**
   * Hide banner ad
   */
  async hideBanner(adUnitKey) {
    try {
      if (!this.isNativePlatform || !this.currentBanners[adUnitKey]) {
        return;
      }

      await AdMob.hideBanner();
      delete this.currentBanners[adUnitKey];
      
      console.log(`✅ Banner ad hidden: ${adUnitKey}`);
    } catch (error) {
      console.error(`❌ Failed to hide banner: ${adUnitKey}`, error);
    }
  }

  /**
   * Remove all banners
   */
  async removeAllBanners() {
    try {
      if (!this.isNativePlatform) {
        return;
      }

      await AdMob.removeBanner();
      this.currentBanners = {};
      
      console.log('✅ All banner ads removed');
    } catch (error) {
      console.error('❌ Failed to remove banners', error);
    }
  }

  /**
   * Preload interstitial ad
   */
  async preloadInterstitial(adUnitKey = 'interstitial_page_transition') {
    try {
      if (!this.isNativePlatform || !this.isInitialized) {
        return false;
      }

      // Check if user has purchased ad removal
      if (!(await this.shouldShowAds())) {
        return false;
      }

      const adUnitId = ADMOB_CONFIG.adUnits[adUnitKey];
      if (!adUnitId) {
        console.error(`❌ Ad unit not found: ${adUnitKey}`);
        return false;
      }

      await AdMob.prepareInterstitial({
        adId: adUnitId
      });

      this.interstitialLoaded = true;
      console.log(`✅ Interstitial ad preloaded: ${adUnitKey}`);
      return true;
    } catch (error) {
      console.error(`❌ Failed to preload interstitial: ${adUnitKey}`, error);
      return false;
    }
  }

  /**
   * Show interstitial ad
   */
  async showInterstitial() {
    try {
      if (!this.isNativePlatform || !this.isInitialized || !this.interstitialLoaded) {
        return false;
      }

      // Check if user has purchased ad removal
      if (!(await this.shouldShowAds())) {
        console.log('✅ User has ad removal - skipping interstitial');
        return false;
      }

      await AdMob.showInterstitial();
      this.interstitialLoaded = false;
      
      console.log('✅ Interstitial ad shown');
      
      // Preload next interstitial
      setTimeout(() => this.preloadInterstitial(), 1000);
      
      return true;
    } catch (error) {
      console.error('❌ Failed to show interstitial', error);
      return false;
    }
  }

  /**
   * Get ad unit ID by key
   */
  getAdUnitId(key) {
    return ADMOB_CONFIG.adUnits[key] || null;
  }

  /**
   * Update ad unit IDs (call this after getting real IDs from AdMob console)
   */
  updateAdUnitIds(adUnits) {
    Object.assign(ADMOB_CONFIG.adUnits, adUnits);
    console.log('✅ Ad unit IDs updated');
  }
}

// Export singleton instance
const adMobService = new AdMobService();
export default adMobService;
