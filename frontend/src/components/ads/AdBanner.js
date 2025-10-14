import React, { useEffect, useState } from 'react';
import { Capacitor } from '@capacitor/core';
import adMobService from '../../services/AdMobService';

const AdBanner = ({ 
  adSlot, 
  adUnitKey, // AdMob ad unit key (e.g., 'banner_dashboard')
  adFormat = "auto",
  fullWidthResponsive = true,
  style = {},
  className = ""
}) => {
  const [isNative, setIsNative] = useState(false);

  useEffect(() => {
    const isNativePlatform = Capacitor.isNativePlatform();
    setIsNative(isNativePlatform);

    if (isNativePlatform && adUnitKey) {
      // Show AdMob banner on native platforms (non-blocking, with error handling)
      const showAd = async () => {
        try {
          await adMobService.showBanner(adUnitKey);
        } catch (error) {
          console.error('Non-critical: AdMob banner failed to show:', error);
          // Continue without showing ad - don't crash the app
        }
      };
      
      // Delay slightly to ensure AdMob is initialized
      const timer = setTimeout(showAd, 1500);

      // Cleanup: hide banner when component unmounts
      return () => {
        clearTimeout(timer);
        try {
          adMobService.hideBanner(adUnitKey).catch(() => {});
        } catch (error) {
          // Ignore cleanup errors
        }
      };
    } else {
      // Initialize AdSense ad for web
      try {
        if (process.env.NODE_ENV === 'production' && window.adsbygoogle) {
          (window.adsbygoogle = window.adsbygoogle || []).push({});
        }
      } catch (error) {
        if (process.env.NODE_ENV !== 'development') {
          console.error('AdSense error:', error);
        }
      }
    }
  }, [adUnitKey, isNative]);

  // Don't show ads during development
  if (process.env.NODE_ENV === 'development') {
    return (
      <div className={`ad-placeholder border-2 border-dashed border-gray-300 bg-gray-50 flex items-center justify-center text-gray-500 text-sm ${className}`} style={{ minHeight: '100px', ...style }}>
        <div className="text-center">
          <div>📢 Ad Placeholder</div>
          <div className="text-xs">
            {isNative ? 'AdMob' : 'AdSense'} will appear here in production
          </div>
        </div>
      </div>
    );
  }

  // On native platforms, AdMob banner is rendered natively (not in DOM)
  // Return a spacer div
  if (isNative) {
    return (
      <div 
        className={`admob-banner-spacer ${className}`} 
        style={{ minHeight: '50px', ...style }}
      >
        {/* Native AdMob banner appears here */}
      </div>
    );
  }

  // On web, render AdSense banner
  return (
    <div className={`ad-container ${className}`} style={style}>
      <ins 
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client={process.env.REACT_APP_ADSENSE_CLIENT_ID || "ca-pub-1934622676928053"}
        data-ad-slot={adSlot}
        data-ad-format={adFormat}
        data-full-width-responsive={fullWidthResponsive ? "true" : "false"}
      />
    </div>
  );
};

export default AdBanner;