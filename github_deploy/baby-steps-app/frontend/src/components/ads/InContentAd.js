import React from 'react';
import AdBanner from './AdBanner';

const InContentAd = ({ title = "Sponsored", className = "" }) => {
  return (
    <div className={`my-6 ${className}`}>
      {/* Ad Label for Transparency */}
      <div className="text-xs text-gray-500 mb-2 text-center">{title}</div>
      
      {/* Responsive In-Content Ad */}
      <AdBanner
        adSlot="1234567892"  // Replace with your in-content ad slot
        adFormat="fluid"
        style={{ 
          minWidth: '300px',
          minHeight: '250px'
        }}
        className="rounded-lg overflow-hidden border border-gray-200"
      />
    </div>
  );
};

export default InContentAd;