import React from 'react';
import { ChatKit, useChatKit } from '@openai/chatkit-react';

const ChatKitWrapper = ({ title, subtitle, currentBaby }) => {
  const { control } = useChatKit({
    api: {
      async getClientSecret(existingSecret) {
        try {
          console.log('🔑 Fetching ChatKit client secret...');
          
          // Get auth token from localStorage
          const token = localStorage.getItem('token');
          if (!token) {
            throw new Error('No authentication token found');
          }
          
          // Call our backend to get ChatKit session
          const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/chatkit/session`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
          });
          
          if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || 'Failed to create ChatKit session');
          }
          
          const { client_secret } = await res.json();
          console.log('✅ ChatKit client secret obtained');
          
          return client_secret;
        } catch (error) {
          console.error('❌ Failed to get ChatKit client secret:', error);
          throw error;
        }
      },
    },
  });

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-6">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          {title}
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          {subtitle}
        </p>
        {currentBaby && (
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Getting guidance for <span className="font-semibold text-rose-600">{currentBaby.name}</span>
          </p>
        )}
      </div>

      {/* ChatKit Component */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
        <ChatKit 
          control={control} 
          className="min-h-[600px] w-full"
          style={{
            '--chatkit-primary-color': '#f43f5e',
            '--chatkit-secondary-color': '#fb7185',
            '--chatkit-background-color': '#ffffff',
            '--chatkit-text-color': '#1f2937',
            '--chatkit-border-radius': '12px',
          }}
        />
      </div>

      {/* Disclaimer */}
      <div className="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
        <p>💡 This information is for educational purposes. Always consult your pediatrician for personalized medical advice.</p>
      </div>
    </div>
  );
};

export default ChatKitWrapper;
