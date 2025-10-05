import { useState, useEffect, useCallback } from 'react';
import { mobileService } from '../services/MobileService';
import axios from 'axios';

export const useOfflineData = (key, apiEndpoint, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isOffline, setIsOffline] = useState(false);

  // Load data from cache first, then try network
  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Load cached data first
      const cachedData = await mobileService.getItem(key);
      if (cachedData) {
        const parsed = JSON.parse(cachedData);
        setData(parsed);
        setLoading(false);
      }

      // Try to fetch fresh data from API
      if (mobileService.getNetworkStatus()) {
        try {
          const response = await axios.get(apiEndpoint);
          const freshData = response.data;
          
          // Update cache
          await mobileService.setItem(key, freshData);
          setData(freshData);
          setIsOffline(false);
        } catch (apiError) {
          console.error('API request failed:', apiError);
          setIsOffline(true);
          
          // If no cached data, show error
          if (!cachedData) {
            setError('Unable to load data offline');
          }
        }
      } else {
        setIsOffline(true);
        
        // If no cached data and offline, show error
        if (!cachedData) {
          setError('No data available offline');
        }
      }
    } catch (err) {
      console.error('Data loading error:', err);
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  }, [key, apiEndpoint]);

  // Save data (with offline support)
  const saveData = useCallback(async (newData, options = {}) => {
    const { optimistic = true, type } = options;

    try {
      if (optimistic) {
        // Optimistically update UI
        setData(newData);
        await mobileService.setItem(key, newData);
      }

      if (mobileService.getNetworkStatus()) {
        // Try to save to server
        const response = await axios.post(apiEndpoint, newData);
        
        // Update with server response
        const savedData = response.data;
        setData(savedData);
        await mobileService.setItem(key, savedData);
        
        return savedData;
      } else {
        // Save to offline queue
        await mobileService.saveOfflineData(type || 'unknown', newData);
        setIsOffline(true);
        
        return newData;
      }
    } catch (error) {
      console.error('Save failed:', error);
      
      if (!mobileService.getNetworkStatus()) {
        // Save to offline queue on network failure
        await mobileService.saveOfflineData(type || 'unknown', newData);
        setIsOffline(true);
      }
      
      throw error;
    }
  }, [key, apiEndpoint]);

  // Update data (with offline support)
  const updateData = useCallback(async (id, updates, options = {}) => {
    const { optimistic = true, type } = options;

    try {
      if (optimistic && data) {
        // Optimistically update UI
        const updatedData = Array.isArray(data) 
          ? data.map(item => item.id === id ? { ...item, ...updates } : item)
          : { ...data, ...updates };
        
        setData(updatedData);
        await mobileService.setItem(key, updatedData);
      }

      if (mobileService.getNetworkStatus()) {
        // Try to update on server
        const response = await axios.put(`${apiEndpoint}/${id}`, updates);
        
        // Update with server response
        const updatedItem = response.data;
        
        if (Array.isArray(data)) {
          const updatedArray = data.map(item => 
            item.id === id ? updatedItem : item
          );
          setData(updatedArray);
          await mobileService.setItem(key, updatedArray);
        } else {
          setData(updatedItem);
          await mobileService.setItem(key, updatedItem);
        }
        
        return updatedItem;
      } else {
        // Save update to offline queue
        await mobileService.saveOfflineData(type || 'update', { id, ...updates });
        setIsOffline(true);
      }
    } catch (error) {
      console.error('Update failed:', error);
      
      if (!mobileService.getNetworkStatus()) {
        // Save to offline queue on network failure
        await mobileService.saveOfflineData(type || 'update', { id, ...updates });
        setIsOffline(true);
      }
      
      throw error;
    }
  }, [key, apiEndpoint, data]);

  // Delete data (with offline support)
  const deleteData = useCallback(async (id, options = {}) => {
    const { optimistic = true, type } = options;

    try {
      if (optimistic && data) {
        // Optimistically update UI
        const filteredData = Array.isArray(data) 
          ? data.filter(item => item.id !== id)
          : null;
        
        setData(filteredData);
        await mobileService.setItem(key, filteredData);
      }

      if (mobileService.getNetworkStatus()) {
        // Try to delete on server
        await axios.delete(`${apiEndpoint}/${id}`);
        
        return true;
      } else {
        // Save delete to offline queue
        await mobileService.saveOfflineData(type || 'delete', { id, action: 'delete' });
        setIsOffline(true);
      }
    } catch (error) {
      console.error('Delete failed:', error);
      
      if (!mobileService.getNetworkStatus()) {
        // Save to offline queue on network failure
        await mobileService.saveOfflineData(type || 'delete', { id, action: 'delete' });
        setIsOffline(true);
      }
      
      throw error;
    }
  }, [key, apiEndpoint, data]);

  // Refresh data
  const refresh = useCallback(async () => {
    await loadData();
  }, [loadData]);

  // Clear cached data
  const clearCache = useCallback(async () => {
    await mobileService.removeItem(key);
    setData(null);
  }, [key]);

  // Load data on mount and dependency changes
  useEffect(() => {
    loadData();
  }, [loadData, ...dependencies]);

  return {
    data,
    loading,
    error,
    isOffline,
    saveData,
    updateData,
    deleteData,
    refresh,
    clearCache
  };
};

export default useOfflineData;