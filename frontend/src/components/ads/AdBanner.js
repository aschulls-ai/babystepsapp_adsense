import React, { useEffect } from 'react';

const AdBanner = ({ 
  adSlot, 
  adFormat = "auto",
  fullWidthResponsive = true,
  style = {},
  className = ""
}) => {
  useEffect(() => {
    try {
      // Initialize AdSense ad
      if (window.adsbygoogle && window.adsbygoogle.loaded) {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      }
    } catch (error) {
      console.error('AdSense error:', error);
    }
  }, []);

  // Don't show ads during development or if AdSense is not loaded
  if (process.env.NODE_ENV === 'development') {
    return (
      <div className={`ad-placeholder border-2 border-dashed border-gray-300 bg-gray-50 flex items-center justify-center text-gray-500 text-sm ${className}`} style={{ minHeight: '100px', ...style }}>
        <div className="text-center">
          <div>📢 Ad Placeholder</div>
          <div className="text-xs">Google AdSense will appear here in production</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`ad-container ${className}`} style={style}>
      <ins 
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client={process.env.REACT_APP_ADSENSE_CLIENT_ID || "ca-pub-0000000000000000"}
        data-ad-slot={adSlot}
        data-ad-format={adFormat}
        data-full-width-responsive={fullWidthResponsive ? "true" : "false"}
      />
    </div>
  );
};

export default AdBanner;