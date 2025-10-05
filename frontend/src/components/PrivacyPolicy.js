import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { ArrowLeft, Shield, Mail, Calendar } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const PrivacyPolicy = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button 
            onClick={() => navigate(-1)}
            variant="ghost" 
            size="sm"
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </Button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Privacy Policy</h1>
              <p className="text-gray-600">Baby Steps Application</p>
            </div>
          </div>
        </div>

        <Card className="shadow-xl border-0">
          <CardHeader className="bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Your Privacy Matters to Us
            </CardTitle>
            <div className="text-green-100 text-sm flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Last Updated: October 5, 2025
            </div>
          </CardHeader>
          
          <CardContent className="p-8 space-y-8">
            {/* Introduction */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">1. Introduction</h2>
              <p className="text-gray-700 leading-relaxed">
                Welcome to Baby Steps, a comprehensive parenting application designed to help parents track their baby's development, 
                nutrition, and safety. This Privacy Policy explains how we collect, use, disclose, and safeguard your information 
                when you use our application and services.
              </p>
              <div className="mt-4 p-4 bg-green-50 border-l-4 border-green-500 rounded">
                <p className="text-green-800 font-medium">
                  🛡️ Your trust is important to us. We are committed to protecting your privacy and your baby's information.
                </p>
              </div>
            </section>

            {/* Information We Collect */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">2. Information We Collect</h2>
              
              <h3 className="text-lg font-medium text-gray-800 mb-3">2.1 Personal Information</h3>
              <ul className="list-disc pl-6 text-gray-700 space-y-2 mb-4">
                <li><strong>Account Information:</strong> Name, email address, password (encrypted)</li>
                <li><strong>Baby Profile Information:</strong> Baby's name, birth date, birth weight, birth length, gender (optional)</li>
                <li><strong>Contact Information:</strong> Email for verification and communications</li>
              </ul>

              <h3 className="text-lg font-medium text-gray-800 mb-3">2.2 Tracking Data</h3>
              <ul className="list-disc pl-6 text-gray-700 space-y-2 mb-4">
                <li><strong>Feeding Records:</strong> Feeding times, amounts, types (bottle, breast, solid foods)</li>
                <li><strong>Sleep Patterns:</strong> Sleep start/end times, duration, quality notes</li>
                <li><strong>Diaper Changes:</strong> Change times, types (wet/dirty), notes</li>
                <li><strong>Developmental Milestones:</strong> Milestone tracking and progress notes</li>
                <li><strong>Growth Measurements:</strong> Weight, height, head circumference (when provided)</li>
              </ul>

              <h3 className="text-lg font-medium text-gray-800 mb-3">2.3 Usage Information</h3>
              <ul className="list-disc pl-6 text-gray-700 space-y-2 mb-4">
                <li><strong>Research Queries:</strong> Food safety questions, meal planning searches</li>
                <li><strong>Dashboard Preferences:</strong> Widget configurations, layout preferences</li>
                <li><strong>Application Usage:</strong> Features used, interaction patterns (aggregated and anonymized)</li>
              </ul>

              <h3 className="text-lg font-medium text-gray-800 mb-3">2.4 Technical Information</h3>
              <ul className="list-disc pl-6 text-gray-700 space-y-2">
                <li><strong>Device Information:</strong> Browser type, device type, operating system</li>
                <li><strong>Log Data:</strong> IP addresses, access times, error logs</li>
                <li><strong>Cookies:</strong> Authentication tokens, preferences (essential cookies only)</li>
              </ul>
            </section>

            {/* How We Use Information */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">3. How We Use Your Information</h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <h3 className="font-medium text-blue-900 mb-2">✨ Core Services</h3>
                  <ul className="text-blue-800 text-sm space-y-1">
                    <li>• Provide personalized baby tracking</li>
                    <li>• Generate age-appropriate insights</li>
                    <li>• Deliver safety recommendations</li>
                    <li>• Enable milestone tracking</li>
                  </ul>
                </div>
                
                <div className="p-4 bg-green-50 rounded-lg">
                  <h3 className="font-medium text-green-900 mb-2">🔒 Account Security</h3>
                  <ul className="text-green-800 text-sm space-y-1">
                    <li>• Authenticate user access</li>
                    <li>• Protect against unauthorized use</li>
                    <li>• Send security notifications</li>
                    <li>• Verify email addresses</li>
                  </ul>
                </div>
                
                <div className="p-4 bg-orange-50 rounded-lg">
                  <h3 className="font-medium text-orange-900 mb-2">📧 Communications</h3>
                  <ul className="text-orange-800 text-sm space-y-1">
                    <li>• Send account verification emails</li>
                    <li>• Provide password reset links</li>
                    <li>• Share important updates</li>
                    <li>• Respond to support requests</li>
                  </ul>
                </div>
                
                <div className="p-4 bg-purple-50 rounded-lg">
                  <h3 className="font-medium text-purple-900 mb-2">📊 Improvement</h3>
                  <ul className="text-purple-800 text-sm space-y-1">
                    <li>• Analyze usage patterns (anonymized)</li>
                    <li>• Improve application features</li>
                    <li>• Fix bugs and issues</li>
                    <li>• Enhance user experience</li>
                  </ul>
                </div>
              </div>
            </section>

            {/* Information Sharing */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">4. Information Sharing and Disclosure</h2>
              
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                <h3 className="font-bold text-red-900 mb-2">🚫 We Do NOT Sell Your Data</h3>
                <p className="text-red-800">
                  We never sell, rent, or trade your personal information or your baby's data to third parties for marketing purposes.
                </p>
              </div>

              <h3 className="text-lg font-medium text-gray-800 mb-3">Limited Sharing Situations:</h3>
              <ul className="list-disc pl-6 text-gray-700 space-y-2">
                <li><strong>Service Providers:</strong> Trusted vendors who help operate our service (hosting, email delivery) under strict confidentiality agreements</li>
                <li><strong>Legal Requirements:</strong> When required by law, legal process, or to protect rights and safety</li>
                <li><strong>Business Transfers:</strong> In case of merger or acquisition (with continued privacy protection)</li>
                <li><strong>Consent:</strong> With your explicit permission for specific purposes</li>
              </ul>
            </section>

            {/* Data Security */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">5. Data Security</h2>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div className="p-4 border border-gray-200 rounded-lg">
                  <h3 className="font-medium text-gray-800 mb-2">🔐 Encryption</h3>
                  <p className="text-gray-600 text-sm">All data is encrypted in transit (HTTPS) and at rest using industry-standard encryption.</p>
                </div>
                
                <div className="p-4 border border-gray-200 rounded-lg">
                  <h3 className="font-medium text-gray-800 mb-2">🛡️ Access Controls</h3>
                  <p className="text-gray-600 text-sm">Strict access controls ensure only authorized personnel can access systems.</p>
                </div>
                
                <div className="p-4 border border-gray-200 rounded-lg">
                  <h3 className="font-medium text-gray-800 mb-2">🔒 Authentication</h3>
                  <p className="text-gray-600 text-sm">Secure password hashing and JWT tokens for user authentication.</p>
                </div>
                
                <div className="p-4 border border-gray-200 rounded-lg">
                  <h3 className="font-medium text-gray-800 mb-2">📱 Multi-Device</h3>
                  <p className="text-gray-600 text-sm">Secure multi-device access with independent session management.</p>
                </div>
              </div>
            </section>

            {/* Your Rights */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">6. Your Privacy Rights</h2>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <h3 className="font-medium text-blue-900 mb-3">You Have the Right To:</h3>
                <div className="grid md:grid-cols-2 gap-4 text-blue-800">
                  <div>
                    <p className="font-medium">📖 Access Your Data</p>
                    <p className="text-sm">Request a copy of your personal information</p>
                  </div>
                  <div>
                    <p className="font-medium">✏️ Correct Your Data</p>
                    <p className="text-sm">Update or correct inaccurate information</p>
                  </div>
                  <div>
                    <p className="font-medium">🗑️ Delete Your Data</p>
                    <p className="text-sm">Request deletion of your account and data</p>
                  </div>
                  <div>
                    <p className="font-medium">📤 Export Your Data</p>
                    <p className="text-sm">Download your data in a portable format</p>
                  </div>
                </div>
              </div>
            </section>

            {/* Data Retention */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">7. Data Retention</h2>
              <ul className="list-disc pl-6 text-gray-700 space-y-2">
                <li><strong>Account Data:</strong> Retained while your account is active</li>
                <li><strong>Baby Tracking Data:</strong> Retained to provide historical insights and trends</li>
                <li><strong>Usage Data:</strong> Aggregated data retained for service improvement (anonymized)</li>
                <li><strong>Deletion Requests:</strong> Data deleted within 30 days of verified deletion request</li>
              </ul>
            </section>

            {/* Children's Privacy */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">8. Children's Privacy</h2>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-900">
                  <strong>👶 Special Protection for Children:</strong> While our app tracks baby information, 
                  we recognize that babies cannot consent to data collection. Parents/guardians have full control 
                  over their baby's data and can request deletion at any time. We never use baby data for 
                  marketing or advertising purposes.
                </p>
              </div>
            </section>

            {/* International Users */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">9. International Users</h2>
              <p className="text-gray-700 leading-relaxed">
                If you are accessing Baby Steps from outside the United States, please note that your information 
                may be transferred to, stored, and processed in the United States. We ensure appropriate safeguards 
                are in place to protect your privacy rights.
              </p>
            </section>

            {/* Updates to Policy */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">10. Changes to This Privacy Policy</h2>
              <p className="text-gray-700 leading-relaxed mb-3">
                We may update this Privacy Policy periodically. We will notify you of any material changes by:
              </p>
              <ul className="list-disc pl-6 text-gray-700 space-y-1">
                <li>Posting the updated policy on this page</li>
                <li>Updating the "Last Updated" date</li>
                <li>Sending email notifications for significant changes</li>
              </ul>
            </section>

            {/* Contact Information */}
            <section className="bg-gray-50 rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Mail className="h-5 w-5 text-green-600" />
                Contact Us
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium text-gray-800 mb-2">Privacy Questions</h3>
                  <p className="text-gray-700 mb-2">
                    If you have questions about this Privacy Policy or our data practices:
                  </p>
                  <div className="space-y-1 text-gray-600">
                    <p>📧 Email: privacy@babysteps.app</p>
                    <p>📮 Mail: Baby Steps Privacy Team</p>
                    <p className="ml-4">123 Parent Lane</p>
                    <p className="ml-4">Safe City, SC 12345</p>
                    <p className="ml-4">United States</p>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-medium text-gray-800 mb-2">Data Rights Requests</h3>
                  <p className="text-gray-700 mb-2">
                    To exercise your privacy rights (access, correct, delete data):
                  </p>
                  <div className="space-y-1 text-gray-600">
                    <p>📧 Email: rights@babysteps.app</p>
                    <p>🔒 Include: Full name and email address</p>
                    <p>⏱️ Response Time: Within 30 days</p>
                    <p>🆔 Identity verification may be required</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-green-100 border border-green-300 rounded">
                <p className="text-green-800 text-sm">
                  <strong>Quick Response Guarantee:</strong> We typically respond to privacy inquiries within 48 hours 
                  and fulfill data requests within 7-14 business days.
                </p>
              </div>
            </section>

            {/* Legal Basis */}
            <section>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">11. Legal Basis for Processing (GDPR)</h2>
              <p className="text-gray-700 mb-3">For users in the European Union, we process your data based on:</p>
              <ul className="list-disc pl-6 text-gray-700 space-y-2">
                <li><strong>Consent:</strong> For marketing communications and optional features</li>
                <li><strong>Contract Performance:</strong> To provide the baby tracking services you requested</li>
                <li><strong>Legitimate Interests:</strong> To improve our services and ensure security</li>
                <li><strong>Legal Compliance:</strong> To comply with applicable laws and regulations</li>
              </ul>
            </section>

            {/* Footer */}
            <div className="border-t pt-6 mt-8">
              <p className="text-center text-gray-500 text-sm">
                This privacy policy is effective as of October 5, 2025, and applies to all users of the Baby Steps application.
              </p>
              <div className="flex justify-center mt-4">
                <Button 
                  onClick={() => navigate(-1)}
                  className="bg-green-600 hover:bg-green-700"
                >
                  Return to Baby Steps
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default PrivacyPolicy;