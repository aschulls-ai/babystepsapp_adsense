// Simple test for login API
const testLogin = async () => {
  try {
    console.log('Testing login API directly...');
    
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'test@babysteps.com',
        password: 'TestPassword123'
      })
    });
    
    console.log('Response status:', response.status);
    const data = await response.json();
    console.log('Response data:', data);
    
    if (response.ok) {
      console.log('✅ Login API working correctly');
    } else {
      console.log('❌ Login API failed');
    }
  } catch (error) {
    console.error('Error testing login API:', error);
  }
};

// Run test
testLogin();