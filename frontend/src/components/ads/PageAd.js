import React from 'react';
import AdBanner from './AdBanner';

const PageAd = ({ 
  position = "bottom", // "top", "bottom", "sidebar"
  adUnitKey, // AdMob ad unit key (e.g., 'banner_dashboard')
  title = "Advertisement", 
  className = "" 
}) => {
  // Different sizes based on position
  const getAdStyle = () => {
    switch (position) {
      case "top":
        return { 
          minWidth: '100%',
          minHeight: '90px',
          maxHeight: '120px'
        };
      case "sidebar":
        return { 
          minWidth: '250px',
          minHeight: '250px',
          maxWidth: '300px'
        };
      case "bottom":
      default:
        return { 
          minWidth: '100%',
          minHeight: '90px',
          maxHeight: '120px'
        };
    }
  };

  const getContainerClasses = () => {
    const baseClasses = "ad-container";
    switch (position) {
      case "top":
        return `${baseClasses} mb-6 ${className}`;
      case "sidebar":
        return `${baseClasses} mb-4 ${className}`;
      case "bottom":
      default:
        return `${baseClasses} mt-8 mb-4 ${className}`;
    }
  };

  return (
    <div className={getContainerClasses()}>
      {/* Ad Label for Transparency */}
      <div className="text-xs text-gray-400 mb-1 text-center font-medium">
        {title}
      </div>
      
      {/* Responsive Page Ad */}
      <AdBanner
        adSlot="1234567893"  // AdSense slot for web
        adUnitKey={adUnitKey}  // AdMob unit key for native
        adFormat="auto"
        style={getAdStyle()}
        className="rounded-md overflow-hidden border border-gray-200 bg-gray-50"
      />
      
      {/* Small disclaimer */}
      <div className="text-xs text-gray-400 mt-1 text-center">
        Ads help keep Baby Steps free
      </div>
    </div>
  );
};

export default PageAd;