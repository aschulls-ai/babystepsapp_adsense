import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Trash2, ArrowLeft, AlertCircle, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const DataDeletion = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    reason: '',
    confirmation: ''
  });
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    // In production, this would send to your backend/email service
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="container mx-auto px-4 py-8 max-w-2xl">
          <Card className="border-0 shadow-lg">
            <CardContent className="p-8 text-center">
              <div className="mb-4 flex justify-center">
                <div className="p-4 bg-green-100 dark:bg-green-900 rounded-full">
                  <CheckCircle className="w-12 h-12 text-green-600 dark:text-green-400" />
                </div>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Request Received
              </h2>
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                Your data deletion request has been received. We will process your request within 30 days and send a confirmation to {formData.email}.
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
                If you have any questions, contact us at babystepsapp@gmail.com
              </p>
              <Button
                onClick={() => navigate('/')}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                Return to Home
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-8 max-w-3xl">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Back
          </button>
          
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-br from-red-500 to-pink-500 rounded-2xl">
              <Trash2 className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Account & Data Deletion
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Request permanent deletion of your Baby Steps account and data
              </p>
            </div>
          </div>
        </div>

        {/* Important Notice */}
        <Card className="border-0 shadow-lg bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500 mb-6">
          <CardContent className="p-6">
            <div className="flex gap-3">
              <AlertCircle className="w-6 h-6 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                  Important Information
                </h3>
                <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                  <li>• This action is <strong>permanent and cannot be undone</strong></li>
                  <li>• All your account data, baby profiles, and activity logs will be deleted</li>
                  <li>• Deletion will be completed within 30 days of your request</li>
                  <li>• You will receive confirmation via email once completed</li>
                  <li>• Any active subscriptions or purchases will be cancelled</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Deletion Request Form */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="text-gray-900 dark:text-white">
              Submit Deletion Request
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email */}
              <div>
                <Label htmlFor="email" className="text-gray-700 dark:text-gray-300">
                  Email Address *
                </Label>
                <Input
                  id="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  placeholder="your.email@example.com"
                  className="mt-1"
                />
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  Enter the email associated with your Baby Steps account
                </p>
              </div>

              {/* Reason */}
              <div>
                <Label htmlFor="reason" className="text-gray-700 dark:text-gray-300">
                  Reason for Deletion (Optional)
                </Label>
                <Textarea
                  id="reason"
                  value={formData.reason}
                  onChange={(e) => setFormData({...formData, reason: e.target.value})}
                  placeholder="Help us improve by sharing why you're leaving..."
                  rows={4}
                  className="mt-1"
                />
              </div>

              {/* Confirmation */}
              <div>
                <Label htmlFor="confirmation" className="text-gray-700 dark:text-gray-300">
                  Type "DELETE" to confirm *
                </Label>
                <Input
                  id="confirmation"
                  type="text"
                  required
                  value={formData.confirmation}
                  onChange={(e) => setFormData({...formData, confirmation: e.target.value})}
                  placeholder="DELETE"
                  className="mt-1"
                />
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  This confirms you understand this action is permanent
                </p>
              </div>

              {/* Submit Button */}
              <div className="flex gap-3 pt-4">
                <Button
                  type="submit"
                  disabled={formData.confirmation.toUpperCase() !== 'DELETE'}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Submit Deletion Request
                </Button>
                <Button
                  type="button"
                  onClick={() => navigate(-1)}
                  variant="outline"
                  className="flex-1 dark:bg-gray-700 dark:text-white dark:border-gray-600"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Alternative Contact */}
        <Card className="mt-6 border-0 shadow-lg">
          <CardContent className="p-6">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
              Alternative: Email Us Directly
            </h3>
            <p className="text-gray-700 dark:text-gray-300 mb-3">
              You can also request account deletion by emailing us directly:
            </p>
            <a
              href="mailto:babystepsapp@gmail.com?subject=Account%20Deletion%20Request"
              className="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium"
            >
              babystepsapp@gmail.com
            </a>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
              Include your account email address in your message
            </p>
          </CardContent>
        </Card>

        {/* GDPR & Privacy Info */}
        <div className="mt-8 text-center text-sm text-gray-600 dark:text-gray-400">
          <p>
            Your privacy rights are protected under GDPR and other data protection laws.
          </p>
          <p className="mt-2">
            Read our{' '}
            <a href="/privacy-policy" className="text-blue-600 hover:underline dark:text-blue-400">
              Privacy Policy
            </a>
            {' '}for more information.
          </p>
        </div>
      </div>
    </div>
  );
};

export default DataDeletion;
