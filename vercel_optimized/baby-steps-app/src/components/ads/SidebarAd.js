import React from 'react';
import AdBanner from './AdBanner';

const SidebarAd = ({ className = "" }) => {
  return (
    <div className={`hidden lg:block ${className}`}>
      <div className="text-xs text-gray-500 mb-2 text-center">Sponsored</div>
      <AdBanner
        adSlot="1234567893"  // Replace with your sidebar ad slot
        adFormat="vertical"
        style={{ 
          width: '300px',
          height: '600px'
        }}
        className="rounded-lg overflow-hidden border border-gray-200"
      />
    </div>
  );
};

export default SidebarAd;