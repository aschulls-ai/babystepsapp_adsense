import React, { useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { FileText, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const TermsOfService = () => {
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
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
            <div className="p-3 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                Terms of Service
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Last Updated: October 14, 2025
              </p>
            </div>
          </div>
        </div>

        {/* Content */}
        <Card className="border-0 shadow-lg">
          <CardContent className="p-8 prose prose-gray dark:prose-invert max-w-none">
            <div className="space-y-6 text-gray-700 dark:text-gray-300">
              
              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">1. Acceptance of Terms</h2>
                <p>
                  Welcome to Baby Steps! By accessing or using the Baby Steps mobile application and website (collectively, the "Service"), you agree to be bound by these Terms of Service ("Terms"). If you do not agree to these Terms, please do not use our Service.
                </p>
                <p>
                  These Terms constitute a legally binding agreement between you and Baby Steps ("we," "us," or "our"). We reserve the right to update these Terms at any time. Continued use of the Service after changes constitutes acceptance of the modified Terms.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">2. Service Description</h2>
                <p>
                  Baby Steps is a parenting companion app that provides:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Baby activity tracking (feeding, sleep, diapers, pumping, growth, milestones)</li>
                  <li>AI-powered parenting assistance and guidance</li>
                  <li>Emergency training resources</li>
                  <li>Formula comparison tools</li>
                  <li>Feeding reminders and timers</li>
                  <li>Activity analysis and insights</li>
                </ul>
                <p className="mt-3">
                  The Service is available as a mobile application (Android) and web application accessible at babystepsapp.app.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">3. User Accounts</h2>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">3.1 Registration</h3>
                <p>
                  To use certain features of the Service, you must create an account. You agree to:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Provide accurate, current, and complete information</li>
                  <li>Maintain and promptly update your account information</li>
                  <li>Keep your password confidential and secure</li>
                  <li>Notify us immediately of any unauthorized access to your account</li>
                  <li>Be responsible for all activities that occur under your account</li>
                </ul>

                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 mt-4">3.2 Account Termination</h3>
                <p>
                  We reserve the right to suspend or terminate your account if you violate these Terms or engage in conduct we deem inappropriate or harmful to the Service or other users.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">4. Medical Disclaimer</h2>
                <p className="font-semibold text-red-600 dark:text-red-400">
                  IMPORTANT: Baby Steps is NOT a medical device or service and does not provide medical advice.
                </p>
                <p>
                  The information provided through our Service, including AI-generated responses, emergency training resources, and general parenting guidance, is for informational and educational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment.
                </p>
                <p>
                  You should:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Always consult your pediatrician or healthcare provider for medical concerns</li>
                  <li>Never disregard professional medical advice because of information from our Service</li>
                  <li>Call emergency services (911) immediately in any emergency situation</li>
                  <li>Not rely on the Service's emergency training guides during an actual emergency</li>
                </ul>
                <p className="mt-3">
                  By using Baby Steps, you acknowledge that we are not liable for any health-related decisions you make based on information from the Service.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">5. User Content and Data</h2>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">5.1 Your Content</h3>
                <p>
                  You retain ownership of any content you submit to the Service, including baby profiles, activity logs, photos, and other data ("User Content"). By submitting User Content, you grant us a worldwide, non-exclusive, royalty-free license to use, store, and process your content to provide and improve the Service.
                </p>

                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 mt-4">5.2 Data Accuracy</h3>
                <p>
                  You are responsible for the accuracy of the data you enter into the Service. We are not responsible for any consequences resulting from inaccurate data entry.
                </p>

                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 mt-4">5.3 Data Backup</h3>
                <p>
                  While we implement security measures to protect your data, we recommend keeping your own records. We are not responsible for data loss due to technical issues, service interruptions, or account deletions.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">6. Acceptable Use Policy</h2>
                <p>You agree NOT to:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Use the Service for any illegal purpose or in violation of any laws</li>
                  <li>Attempt to gain unauthorized access to our systems or networks</li>
                  <li>Interfere with or disrupt the Service's operation</li>
                  <li>Use automated tools (bots, scrapers) to access the Service without permission</li>
                  <li>Upload malicious code, viruses, or harmful content</li>
                  <li>Harass, abuse, or harm other users</li>
                  <li>Impersonate others or create fake accounts</li>
                  <li>Reverse engineer, decompile, or attempt to extract source code</li>
                  <li>Resell or redistribute the Service without authorization</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">7. Intellectual Property</h2>
                <p>
                  The Service, including its design, text, graphics, logos, icons, images, audio clips, software, and all other content (excluding User Content), is owned by Baby Steps and protected by copyright, trademark, and other intellectual property laws.
                </p>
                <p>
                  You may not copy, modify, distribute, sell, or lease any part of the Service without our express written permission.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">8. AI-Generated Content</h2>
                <p>
                  Our AI Parenting Assistant uses artificial intelligence to generate responses. While we strive for accuracy, AI-generated content:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>May occasionally produce inaccurate or incomplete information</li>
                  <li>Should not be considered professional medical or legal advice</li>
                  <li>Is provided "as is" without warranties of any kind</li>
                  <li>Should be verified with professional sources for critical decisions</li>
                </ul>
                <p className="mt-3">
                  You use the AI Assistant at your own risk and discretion.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">9. Payments and Subscriptions</h2>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">9.1 In-App Purchases</h3>
                <p>
                  Baby Steps offers in-app purchases, including ad removal ($4.99 one-time payment). All payments are processed securely through Google Play Billing.
                </p>

                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 mt-4">9.2 Refunds</h3>
                <p>
                  Refund policies are governed by the Google Play Store's refund policy. Contact Google Play support for refund requests.
                </p>

                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 mt-4">9.3 Price Changes</h3>
                <p>
                  We reserve the right to modify pricing at any time. Changes will not affect purchases already made.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">10. Advertisements</h2>
                <p>
                  The free version of Baby Steps displays advertisements. We use Google AdSense to serve ads. By using the Service, you agree to the display of advertisements unless you purchase ad removal.
                </p>
                <p>
                  We are not responsible for the content of third-party advertisements. Clicking on ads may redirect you to external websites governed by their own terms and policies.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">11. Third-Party Services</h2>
                <p>
                  Our Service may contain links to or integrate with third-party websites, services, or content. We are not responsible for:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>The availability, content, or practices of third-party services</li>
                  <li>Any damages or losses resulting from your use of third-party services</li>
                  <li>The privacy policies of third-party services</li>
                </ul>
                <p className="mt-3">
                  Your use of third-party services is at your own risk and subject to their terms.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">12. Disclaimer of Warranties</h2>
                <p className="font-semibold">
                  THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED.
                </p>
                <p>
                  We disclaim all warranties, including but not limited to:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Implied warranties of merchantability and fitness for a particular purpose</li>
                  <li>Warranties regarding accuracy, reliability, or completeness of content</li>
                  <li>Warranties that the Service will be uninterrupted, secure, or error-free</li>
                  <li>Warranties regarding results obtained from using the Service</li>
                </ul>
                <p className="mt-3">
                  You use the Service at your own risk.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">13. Limitation of Liability</h2>
                <p className="font-semibold">
                  TO THE MAXIMUM EXTENT PERMITTED BY LAW, BABY STEPS SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Loss of profits, data, use, or goodwill</li>
                  <li>Service interruptions or data loss</li>
                  <li>Unauthorized access to or alteration of your transmissions or data</li>
                  <li>Health-related decisions made based on Service information</li>
                  <li>Any other matter relating to the Service</li>
                </ul>
                <p className="mt-3">
                  Our total liability shall not exceed the amount you paid us in the past 12 months, or $100, whichever is greater.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">14. Indemnification</h2>
                <p>
                  You agree to indemnify, defend, and hold harmless Baby Steps, its officers, directors, employees, and agents from any claims, liabilities, damages, losses, costs, or expenses (including legal fees) arising from:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Your use of the Service</li>
                  <li>Your violation of these Terms</li>
                  <li>Your violation of any rights of another party</li>
                  <li>Your User Content</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">15. Changes to the Service</h2>
                <p>
                  We reserve the right to:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Modify, suspend, or discontinue any part of the Service at any time</li>
                  <li>Change features, functionality, or availability</li>
                  <li>Impose limits on certain features or restrict access</li>
                </ul>
                <p className="mt-3">
                  We will not be liable to you or any third party for any modifications or discontinuation of the Service.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">16. Privacy</h2>
                <p>
                  Your privacy is important to us. Please review our Privacy Policy, which explains how we collect, use, and protect your personal information. By using the Service, you agree to our Privacy Policy.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">17. Children's Privacy</h2>
                <p>
                  The Service is intended for use by adults (18+) to track information about their children. We do not knowingly collect personal information directly from children under 13. Parents and guardians are responsible for all data entered about their children.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">18. Governing Law</h2>
                <p>
                  These Terms shall be governed by and construed in accordance with the laws of the United States, without regard to conflict of law principles. Any disputes shall be resolved in the courts located in [Your Jurisdiction].
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">19. Severability</h2>
                <p>
                  If any provision of these Terms is found to be invalid or unenforceable, that provision shall be limited or eliminated to the minimum extent necessary, and the remaining provisions shall remain in full force and effect.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">20. Contact Information</h2>
                <p>
                  If you have questions about these Terms, please contact us:
                </p>
                <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg mt-3">
                  <p className="font-semibold">Baby Steps</p>
                  <p>Email: babystepsapp@gmail.com</p>
                  <p>Website: babystepsapp.app</p>
                </div>
              </section>

              <section className="border-t border-gray-300 dark:border-gray-700 pt-6 mt-8">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  By using Baby Steps, you acknowledge that you have read, understood, and agree to be bound by these Terms of Service.
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                  Last Updated: October 14, 2025
                </p>
              </section>

            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default TermsOfService;
