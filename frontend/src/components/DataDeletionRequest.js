import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { ArrowLeft, Trash2, AlertTriangle, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

const DataDeletionRequest = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [reason, setReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email) {
      toast.error('Please enter your email address');
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      toast.error('Please enter a valid email address');
      return;
    }

    setIsSubmitting(true);

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/deletion-request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email,
          reason: reason || 'No reason provided'
        })
      });

      if (response.ok) {
        setIsSubmitted(true);
        toast.success('Your deletion request has been submitted successfully');
      } else {
        const error = await response.json();
        toast.error(error.detail || 'Failed to submit deletion request');
      }
    } catch (error) {
      console.error('Deletion request error:', error);
      toast.error('Failed to submit deletion request. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-8 px-4">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="flex items-center gap-4 mb-8">
            <Button 
              onClick={() => navigate('/settings')}
              variant="ghost" 
              size="sm"
              className="flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Settings
            </Button>
          </div>

          <Card className="shadow-xl border-0">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="h-10 w-10 text-green-600 dark:text-green-400" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Request Submitted Successfully
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                Your data deletion request has been received. Our team will review your request and process it within 30 days.
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
                You will receive a confirmation email at <strong>{email}</strong> once your data has been deleted.
              </p>
              <Button 
                onClick={() => navigate('/settings')}
                className="bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-800"
              >
                Return to Settings
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-orange-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button 
            onClick={() => navigate('/settings')}
            variant="ghost" 
            size="sm"
            className="flex items-center gap-2 text-gray-700 dark:text-gray-300"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Settings
          </Button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-red-600 dark:bg-red-700 rounded-lg flex items-center justify-center">
              <Trash2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Data Deletion Request</h1>
              <p className="text-gray-600 dark:text-gray-400">Request deletion of your account and data</p>
            </div>
          </div>
        </div>

        <Card className="shadow-xl border-0 mb-6">
          <CardHeader className="bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Important Information
            </CardTitle>
          </CardHeader>
          
          <CardContent className="p-6 space-y-4">
            <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
              <h3 className="font-semibold text-yellow-900 dark:text-yellow-200 mb-2">⚠️ This Action Cannot Be Undone</h3>
              <p className="text-yellow-800 dark:text-yellow-300 text-sm">
                Once your data is deleted, it cannot be recovered. Please make sure you want to proceed before submitting this request.
              </p>
            </div>

            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 dark:text-white">What Will Be Deleted:</h3>
              <ul className="list-disc pl-6 text-gray-700 dark:text-gray-300 space-y-2 text-sm">
                <li><strong>Your Account:</strong> Email, name, and login credentials</li>
                <li><strong>Baby Profiles:</strong> All baby information including names, birth dates, and photos</li>
                <li><strong>Activity Data:</strong> All tracked activities (feeding, sleep, diaper changes, etc.)</li>
                <li><strong>Measurements & Milestones:</strong> Growth data and developmental milestones</li>
                <li><strong>AI Conversations:</strong> All questions asked to the AI Assistant</li>
                <li><strong>Settings & Preferences:</strong> All your personalized settings</li>
              </ul>
            </div>

            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900 dark:text-white">Processing Time:</h3>
              <p className="text-gray-700 dark:text-gray-300 text-sm">
                Your deletion request will be processed within <strong>30 days</strong> as required by privacy regulations (GDPR, CCPA). You will receive a confirmation email once your data has been permanently deleted.
              </p>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <h3 className="font-semibold text-blue-900 dark:text-blue-200 mb-2">💡 Alternative Options</h3>
              <p className="text-blue-800 dark:text-blue-300 text-sm mb-2">
                If you're concerned about privacy or want to take a break, consider:
              </p>
              <ul className="text-blue-800 dark:text-blue-300 text-sm list-disc pl-4 space-y-1">
                <li>Logging out of your account (data remains available for future use)</li>
                <li>Deleting specific baby profiles instead of your entire account</li>
                <li>Contacting support at <a href="mailto:babystepsapp@gmail.com" className="underline">babystepsapp@gmail.com</a> for assistance</li>
              </ul>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-xl border-0">
          <CardHeader>
            <CardTitle className="text-gray-900 dark:text-white">Submit Deletion Request</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="email" className="text-gray-900 dark:text-white">
                  Email Address <span className="text-red-600">*</span>
                </Label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your registered email address"
                  required
                  className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  Please enter the email address associated with your Baby Steps account
                </p>
              </div>

              <div>
                <Label htmlFor="reason" className="text-gray-900 dark:text-white">
                  Reason for Deletion (Optional)
                </Label>
                <textarea
                  id="reason"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="Let us know why you're leaving (optional)"
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                />
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  Your feedback helps us improve Baby Steps for other parents
                </p>
              </div>

              <div className="pt-4 border-t dark:border-gray-700">
                <Button 
                  type="submit" 
                  disabled={isSubmitting}
                  className="w-full bg-red-600 hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-800 text-white"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Submitting Request...
                    </>
                  ) : (
                    <>
                      <Trash2 className="w-4 h-4 mr-2" />
                      Submit Deletion Request
                    </>
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Need help or have questions? Contact us at{' '}
            <a href="mailto:babystepsapp@gmail.com" className="text-blue-600 dark:text-blue-400 hover:underline">
              babystepsapp@gmail.com
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default DataDeletionRequest;