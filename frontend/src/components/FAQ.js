import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { ChevronDown, ChevronUp, HelpCircle, Book, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const FAQ = () => {
  const navigate = useNavigate();
  const [openIndex, setOpenIndex] = useState(null);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const faqData = [
    {
      category: "Getting Started",
      questions: [
        {
          q: "How do I add my baby's profile?",
          a: "Navigate to the Baby Profile page from the dashboard. Click 'Add Baby Profile' and enter your baby's name, date of birth, and gender. You can also upload a profile picture. The app supports multiple baby profiles for families with twins or siblings."
        },
        {
          q: "Can I track multiple babies?",
          a: "Yes! Baby Steps supports multiple baby profiles. You can switch between babies using the dropdown selector on the Dashboard and Track Activities pages. Each baby's data is stored separately."
        },
        {
          q: "How do I switch between light and dark mode?",
          a: "Look for the sun/moon icon in the top right corner of the app. Tap it to toggle between light and dark modes. Your preference is saved automatically."
        }
      ]
    },
    {
      category: "Tracking Activities",
      questions: [
        {
          q: "How do I log a feeding?",
          a: "Go to Track Activities and tap 'Quick Feed'. Select the type (bottle, breast, or solid food). For bottle feeding, enter the amount in ounces. For breastfeeding, enter the duration in minutes. The app will automatically timestamp the activity."
        },
        {
          q: "How do sleep and pumping timers work?",
          a: "Tap 'Start Sleep' or 'Start Pump' to begin timing. The button will show a live countdown. When finished, tap 'Stop Sleep' or 'Stop Pump'. The duration is automatically calculated, but you can adjust it before saving."
        },
        {
          q: "What's the difference between feeding types?",
          a: "Bottle feeding tracks the amount in ounces. Breastfeeding tracks duration in minutes. Solid food logs when you introduced solids. Choose the appropriate type for accurate tracking."
        },
        {
          q: "How do I track growth measurements?",
          a: "Use the 'Measurements' quick action to log your baby's weight (lbs) and height (inches). These appear in the Growth filter and help you monitor developmental progress."
        },
        {
          q: "What milestone categories are available?",
          a: "Milestones are organized into five categories: Physical (rolling, sitting, walking), Cognitive (recognizing faces, babbling), Social (smiling, playing), Feeding (first solids, using utensils), and Sleep (sleeping through the night)."
        }
      ]
    },
    {
      category: "Activity History & Analysis",
      questions: [
        {
          q: "How do I filter my activities?",
          a: "In the Activity History section, use the dropdown menu to filter by activity type: All Activities, Feeding, Diaper, Sleep, Pumping, Growth (measurements), or Milestones. You can also sort by date or type."
        },
        {
          q: "Why don't my milestone activities show up in the filter?",
          a: "Make sure you're selecting 'Milestones' from the filter dropdown (not 'Milestone' singular). The activities are stored with plural names."
        },
        {
          q: "How can I see feeding patterns?",
          a: "Go to the Analysis page to view feeding trends, sleep patterns, and diaper frequency over time. You can filter by date range and view charts showing patterns."
        }
      ]
    },
    {
      category: "AI Assistant",
      questions: [
        {
          q: "What can the AI Assistant help with?",
          a: "The AI Parenting Assistant can answer questions about feeding schedules, sleep training, developmental milestones, common baby concerns, nutrition, and general parenting advice. It's available 24/7 for quick guidance."
        },
        {
          q: "Is the AI Assistant a replacement for medical advice?",
          a: "No. The AI Assistant provides general parenting information and guidance, but it's not a substitute for professional medical advice. Always consult your pediatrician for medical concerns or emergencies."
        },
        {
          q: "How do I ask a question?",
          a: "Navigate to 'AI Parenting Assistant' from the dashboard. Type your question in the chat box and press send. The AI will respond with helpful information based on your query."
        }
      ]
    },
    {
      category: "Emergency Training",
      questions: [
        {
          q: "Where can I find emergency procedures?",
          a: "Access the Emergency Training section from the dashboard. You'll find step-by-step guides for infant CPR, choking response, and other critical emergency procedures."
        },
        {
          q: "Should I rely on the app during an emergency?",
          a: "The Emergency Training section is for educational reference. In a real emergency, call 911 immediately. Use the app's guides to familiarize yourself with procedures beforehand."
        }
      ]
    },
    {
      category: "Features & Tools",
      questions: [
        {
          q: "What is the Formula Comparison tool?",
          a: "This tool helps you compare different baby formulas side-by-side. Filter by age range and review nutritional information to find the best formula for your baby."
        },
        {
          q: "How do feeding reminders work?",
          a: "Set a custom reminder by specifying hours and minutes. The app will show a real-time countdown. When the timer reaches zero, you'll be notified it's time for the next feeding."
        },
        {
          q: "Can I remove ads?",
          a: "Yes! Purchase the ad removal option for $4.99 (one-time payment) in the Settings page under 'Ad Removal'. This removes all advertisements for a distraction-free experience."
        }
      ]
    },
    {
      category: "Data & Privacy",
      questions: [
        {
          q: "Is my data secure?",
          a: "Yes. Your data is stored securely and encrypted. We take privacy seriously and never share your personal information with third parties without consent. Read our full Privacy Policy for details."
        },
        {
          q: "Can I export my data?",
          a: "Data export functionality is currently in development. You can view all your activities in the Activity History section and Analysis page."
        },
        {
          q: "What happens if I delete the app?",
          a: "Your data is stored on our servers, so if you delete and reinstall the app, you can log back in to access your data. However, if you delete your account, all data is permanently removed."
        }
      ]
    },
    {
      category: "iOS & Cross-Platform",
      questions: [
        {
          q: "Is there an iOS app?",
          a: "The iOS app is currently in development. In the meantime, iOS users can access the fully-featured web app at babystepsapp.app and add it to their home screen for a native app experience."
        },
        {
          q: "How can my partner access the app on iPhone?",
          a: "Your partner can visit babystepsapp.app on Safari, tap the Share button, and select 'Add to Home Screen'. They can then log in with the same account to stay synced across devices."
        },
        {
          q: "Can we use the same account on multiple devices?",
          a: "Yes! Log in with the same credentials on Android (app), iOS (web), or desktop (web) to sync all your baby's data across devices."
        }
      ]
    },
    {
      category: "Troubleshooting",
      questions: [
        {
          q: "Why isn't my activity saving?",
          a: "Make sure you're connected to the internet. Check that all required fields are filled out before clicking Save. If the problem persists, try logging out and back in."
        },
        {
          q: "The timer isn't working correctly. What should I do?",
          a: "Ensure the app stays open or running in the background while timing. If you close the app completely, the timer may reset. We recommend keeping the app active during timed sessions."
        },
        {
          q: "I can't see my activities in the history. Why?",
          a: "Check your filter settings - you might be viewing a specific activity type. Select 'All Activities' to see everything. Also verify you have the correct baby profile selected."
        },
        {
          q: "Dark mode text is hard to read. How do I fix it?",
          a: "We've optimized the app for both light and dark modes. If you're experiencing issues, try switching modes or updating to the latest version. Report any specific issues to babystepsapp@gmail.com."
        }
      ]
    },
    {
      category: "Account & Settings",
      questions: [
        {
          q: "How do I change my account information?",
          a: "Go to Settings and tap 'Edit Profile'. You can update your name, email, and password. Changes are saved automatically."
        },
        {
          q: "I forgot my password. What do I do?",
          a: "On the login page, tap 'Forgot Password'. Enter your email address, and we'll send you a password reset link."
        },
        {
          q: "How do I delete my account?",
          a: "Contact us at babystepsapp@gmail.com to request account deletion. Please note that this action is permanent and all data will be removed."
        }
      ]
    },
    {
      category: "Support",
      questions: [
        {
          q: "How do I report a bug or request a feature?",
          a: "We'd love to hear from you! Email us at babystepsapp@gmail.com with your feedback, bug reports, or feature requests. We actively review all submissions."
        },
        {
          q: "Is there a desktop version?",
          a: "Yes! Visit babystepsapp.app from any web browser to access the full web version of Baby Steps. All features are available on desktop."
        },
        {
          q: "How often is the app updated?",
          a: "We regularly release updates with new features, improvements, and bug fixes. Keep your app updated through the Google Play Store to get the latest enhancements."
        }
      ]
    }
  ];

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
              <Book className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                User Guide & FAQ
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Everything you need to know about Baby Steps
              </p>
            </div>
          </div>
        </div>

        {/* FAQ Categories */}
        <div className="space-y-6">
          {faqData.map((category, categoryIndex) => (
            <Card key={categoryIndex} className="border-0 shadow-lg">
              <CardContent className="p-6">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                  <HelpCircle className="w-5 h-5 text-blue-500" />
                  {category.category}
                </h2>
                
                <div className="space-y-3">
                  {category.questions.map((item, qIndex) => {
                    const globalIndex = categoryIndex * 100 + qIndex;
                    const isOpen = openIndex === globalIndex;
                    
                    return (
                      <div
                        key={qIndex}
                        className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
                      >
                        <button
                          onClick={() => toggleFAQ(globalIndex)}
                          className="w-full px-4 py-3 flex items-center justify-between bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-750 transition-colors text-left"
                        >
                          <span className="font-medium text-gray-900 dark:text-white pr-4">
                            {item.q}
                          </span>
                          {isOpen ? (
                            <ChevronUp className="w-5 h-5 text-gray-500 flex-shrink-0" />
                          ) : (
                            <ChevronDown className="w-5 h-5 text-gray-500 flex-shrink-0" />
                          )}
                        </button>
                        
                        {isOpen && (
                          <div className="px-4 py-3 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                              {item.a}
                            </p>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Contact Support */}
        <Card className="mt-8 border-0 shadow-lg bg-gradient-to-r from-blue-500 to-purple-500">
          <CardContent className="p-6 text-center">
            <h3 className="text-xl font-bold text-white mb-2">
              Still have questions?
            </h3>
            <p className="text-blue-100 mb-4">
              We're here to help! Contact our support team.
            </p>
            <a
              href="mailto:babystepsapp@gmail.com"
              className="inline-block px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
            >
              Email Support
            </a>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default FAQ;
