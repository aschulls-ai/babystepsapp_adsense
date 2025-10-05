import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { CheckCircle, XCircle, Loader2 } from 'lucide-react';

const EmailVerification = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('loading'); // 'loading', 'success', 'error'
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await axios.get(`/auth/verify-email/${token}`);
        setStatus('success');
        setMessage(response.data.message);
        
        // Redirect to login after 3 seconds
        setTimeout(() => {
          navigate('/auth');
        }, 3000);
      } catch (error) {
        setStatus('error');
        setMessage(error.response?.data?.detail || 'Verification failed');
      }
    };

    if (token) {
      verifyEmail();
    }
  }, [token, navigate]);

  const handleGoToLogin = () => {
    navigate('/auth');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-green-50 via-white to-blue-50">
      <div className="w-full max-w-md">
        <Card className="shadow-2xl border-0">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-semibold text-gray-800">
              Email Verification
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="text-center">
              {status === 'loading' && (
                <div>
                  <Loader2 className="w-12 h-12 text-blue-600 mx-auto mb-4 animate-spin" />
                  <p className="text-gray-600">Verifying your email...</p>
                </div>
              )}
              
              {status === 'success' && (
                <div>
                  <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-green-800 mb-2">
                    Email Verified Successfully!
                  </h3>
                  <p className="text-green-700 mb-4">{message}</p>
                  <p className="text-sm text-gray-600 mb-6">
                    You can now log in to your account. Redirecting in 3 seconds...
                  </p>
                  <Button 
                    onClick={handleGoToLogin}
                    className="bg-green-600 hover:bg-green-700 text-white"
                  >
                    Go to Login
                  </Button>
                </div>
              )}
              
              {status === 'error' && (
                <div>
                  <XCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-red-800 mb-2">
                    Verification Failed
                  </h3>
                  <p className="text-red-700 mb-4">{message}</p>
                  <p className="text-sm text-gray-600 mb-6">
                    The verification link may be expired or invalid.
                  </p>
                  <Button 
                    onClick={handleGoToLogin}
                    variant="outline"
                    className="border-red-600 text-red-600 hover:bg-red-50"
                  >
                    Back to Login
                  </Button>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default EmailVerification;