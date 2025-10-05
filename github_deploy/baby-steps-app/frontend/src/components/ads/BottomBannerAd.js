import React from 'react';
import AdBanner from './AdBanner';

const BottomBannerAd = () => {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 bg-white border-t shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        {/* Mobile Ad */}
        <div className="block md:hidden">
          <AdBanner
            adSlot="1234567890"  // Replace with your mobile banner ad slot
            adFormat="banner"
            style={{ width: '100%', height: '50px' }}
            className="py-1"
          />
        </div>
        
        {/* Desktop Ad */}
        <div className="hidden md:block">
          <AdBanner
            adSlot="1234567891"  // Replace with your desktop banner ad slot
            adFormat="banner"
            style={{ width: '100%', height: '90px' }}
            className="py-2"
          />
        </div>
        
        {/* Close button for user experience */}
        <button 
          className="absolute top-1 right-2 text-gray-400 hover:text-gray-600 text-xs"
          onClick={() => {
            // Option: Allow users to minimize ad (store in localStorage)
            const banner = document.querySelector('.fixed.bottom-0');
            if (banner) {
              banner.style.display = 'none';
              localStorage.setItem('adBannerMinimized', 'true');
            }
          }}
          title="Minimize ad"
        >
          ×
        </button>
      </div>
    </div>
  );
};

export default BottomBannerAd;