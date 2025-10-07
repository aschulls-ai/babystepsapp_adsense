// API Connection Test Utility
export const testApiConnection = async () => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
  
  try {
    console.log(`Testing API connection to: ${backendUrl}`);
    
    // Test basic health endpoint
    const response = await fetch(`${backendUrl}/api/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ API Connection successful:', data);
      return { success: true, data };
    } else {
      console.error('❌ API Health check failed:', response.status);
      return { success: false, error: `HTTP ${response.status}` };
    }
  } catch (error) {
    console.error('❌ API Connection failed:', error.message);
    return { success: false, error: error.message };
  }
};

// Test authentication endpoint
export const testAuthEndpoint = async () => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
  
  try {
    // Test with invalid credentials to check if endpoint exists
    const response = await fetch(`${backendUrl}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'test@test.com',
        password: 'invalid'
      }),
    });
    
    // We expect this to fail with 401/422, but not 404
    if (response.status === 404) {
      console.error('❌ Auth endpoint not found (404)');
      return { success: false, error: 'Auth endpoint not available' };
    } else {
      console.log('✅ Auth endpoint accessible (got response)');
      return { success: true, status: response.status };
    }
  } catch (error) {
    console.error('❌ Auth endpoint test failed:', error.message);
    return { success: false, error: error.message };
  }
};

// Run both tests
export const runApiTests = async () => {
  console.log('🔍 Running API connection tests...');
  
  const healthTest = await testApiConnection();
  const authTest = await testAuthEndpoint();
  
  return {
    health: healthTest,
    auth: authTest,
    overall: healthTest.success && authTest.success
  };
};