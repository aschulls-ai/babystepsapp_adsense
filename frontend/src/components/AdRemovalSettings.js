import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { ShieldCheck, Star, X, Check } from 'lucide-react';
import { toast } from 'sonner';
import billingService from '../services/BillingService';

const AdRemovalSettings = () => {
  const [hasPurchased, setHasPurchased] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Initialize billing service
    const init = async () => {
      await billingService.initialize();
      setHasPurchased(billingService.hasAdRemoval());
    };
    init();
  }, []);

  const handlePurchase = async () => {
    setLoading(true);
    try {
      const success = await billingService.purchaseAdRemoval();
      if (success) {
        setHasPurchased(true);
        toast.success('🎉 Purchase successful! Ads removed.');
      } else {
        toast.info('ℹ️ Purchase flow needs billing plugin integration');
      }
    } catch (error) {
      toast.error('Failed to complete purchase. Please try again.');
      console.error('Purchase error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRestore = async () => {
    setLoading(true);
    try {
      const restored = await billingService.restorePurchases();
      if (restored) {
        setHasPurchased(true);
        toast.success('✅ Purchase restored! Ads removed.');
      } else {
        toast.info('No previous purchases found.');
      }
    } catch (error) {
      toast.error('Failed to restore purchases.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-gray-800 dark:text-white">
          <Star className="h-5 w-5 text-yellow-500" />
          Premium Features
        </CardTitle>
      </CardHeader>
      <CardContent>
        {hasPurchased ? (
          // Already purchased
          <div className="text-center py-6">
            <div className="mb-4">
              <ShieldCheck className="h-16 w-16 text-green-500 mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Premium Active
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              You're enjoying an ad-free experience!
            </p>
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <ul className="text-left space-y-2 text-sm text-green-800 dark:text-green-300">
                <li className="flex items-center gap-2">
                  <Check className="h-4 w-4" />
                  No ads in the app
                </li>
                <li className="flex items-center gap-2">
                  <Check className="h-4 w-4" />
                  Cleaner, faster experience
                </li>
                <li className="flex items-center gap-2">
                  <Check className="h-4 w-4" />
                  Support app development
                </li>
              </ul>
            </div>
          </div>
        ) : (
          // Not purchased yet
          <div className="space-y-4">
            <div className="text-center py-4">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Remove Ads Forever
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Enjoy an ad-free experience for just $1.99
              </p>
              
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mb-4">
                <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                  $1.99
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">One-time payment</p>
                
                <ul className="text-left mt-4 space-y-2 text-sm text-gray-700 dark:text-gray-300">
                  <li className="flex items-center gap-2">
                    <X className="h-4 w-4 text-red-500" />
                    <span>No more banner ads</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <X className="h-4 w-4 text-red-500" />
                    <span>No more interstitial ads</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    <span>Cleaner interface</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500" />
                    <span>Support independent development</span>
                  </li>
                </ul>
              </div>

              <Button
                onClick={handlePurchase}
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 text-lg"
              >
                {loading ? 'Processing...' : '🎁 Remove Ads - $1.99'}
              </Button>

              <Button
                onClick={handleRestore}
                disabled={loading}
                variant="ghost"
                className="w-full mt-2 text-gray-600 dark:text-gray-400"
              >
                Already purchased? Restore
              </Button>
            </div>

            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-xs text-gray-600 dark:text-gray-400">
              <p>
                ✓ One-time purchase • ✓ Works on all your devices • ✓ No subscription • ✓ Support development
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AdRemovalSettings;
