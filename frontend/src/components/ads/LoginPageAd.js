import React from 'react';
import AdBanner from './AdBanner';

const LoginPageAd = ({ className = "" }) => {
  return (
    <div className={`my-4 ${className}`}>
      {/* Small Ad Label */}
      <div className="text-xs text-gray-400 mb-2 text-center">Advertisement</div>
      
      {/* Compact Login Page Ad */}
      <div className="flex justify-center">
        <AdBanner
          adSlot="1234567893"  // Replace with your login page ad slot
          adFormat="rectangle" 
          style={{ 
            width: '300px',
            height: '100px'
          }}
          className="rounded-md border border-gray-100 shadow-sm bg-gray-50"
          fullWidthResponsive={false}
        />
      </div>
      
      {/* Subtle disclaimer */}
      <div className="text-xs text-gray-300 mt-1 text-center">
        Ads help keep Baby Steps free
      </div>
    </div>
  );
};

export default LoginPageAd;