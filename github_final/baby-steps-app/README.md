# 👶 Baby Steps - Parenting Made Easy

A comprehensive parenting companion app with baby tracking, nutrition guidance, AI-powered features, and monetization through Google AdSense.

## 🌟 Features

### 👶 Baby Tracking & Management
- **Baby Profiles**: Multiple baby support with detailed profiles
- **Milestone Tracking**: Age-appropriate developmental milestones
- **Activity Tracking**: Feeding, diaper changes, sleep patterns
- **Growth Charts**: Weight, height, and development tracking

### 🤖 AI-Powered Features  
- **Food Research**: AI safety checks for baby foods
- **Meal Planning**: Age-appropriate meal suggestions
- **Emergency Training**: Step-by-step emergency procedures
- **Research Assistant**: Parenting questions and guidance

### 📱 Modern Features
- **Responsive Design**: Works perfectly on mobile and desktop
- **Offline Support**: Works without internet connection
- **Push Notifications**: Reminders and alerts
- **Dark/Light Mode**: User preference themes

### 💰 Monetization Ready
- **Google AdSense Integration**: Professional ad placements
- **Revenue Optimized**: Strategic ad positioning for maximum earnings
- **COPPA Compliant**: Safe for parenting apps

## 🚀 Live Demo

**Production App**: [babystepsapp.com](https://babystepsapp.com) *(Replace with your actual domain)*

## 💻 Tech Stack

- **Frontend**: React 19, TypeScript, Tailwind CSS
- **UI Components**: Shadcn UI, Radix UI
- **Routing**: React Router DOM
- **State Management**: React Context + Hooks
- **Charts**: Chart.js, React Chart.js 2
- **Grid Layout**: React Grid Layout (draggable dashboard)
- **Mobile**: Capacitor (iOS/Android support)
- **Monetization**: Google AdSense
- **Backend**: FastAPI + MongoDB *(separate deployment)*

## 🔧 Quick Start

### Prerequisites
- Node.js 18+ or 20+
- Yarn package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/baby-steps-app.git
   cd baby-steps-app
   ```

2. **Install dependencies**
   ```bash
   yarn install
   ```

3. **Set up environment variables**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Update .env with your values:
   REACT_APP_BACKEND_URL=your-backend-url
   REACT_APP_ADSENSE_CLIENT_ID=ca-pub-1934622676928053
   ```

4. **Start development server**
   ```bash
   yarn start
   ```

Visit `http://localhost:3000` to see the app running!

## 🌐 Deployment

### Deploy to Vercel (Recommended)

1. **Fork this repository on GitHub**

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - **Framework**: Create React App
   - **Root Directory**: Leave empty (or set to `/` if needed)

3. **Environment Variables** (Add in Vercel dashboard)
   ```
   REACT_APP_BACKEND_URL=https://babysteps-mobile.preview.emergentagent.com
   REACT_APP_ADSENSE_CLIENT_ID=ca-pub-1934622676928053
   ```

4. **Deploy!**
   - Vercel will auto-deploy from your main branch
   - Get your URL: `https://baby-steps-app.vercel.app`

## 💰 Google AdSense Setup

### Current Configuration
- ✅ **AdSense Client ID**: `ca-pub-1934622676928053` 
- ✅ **Ad Placements**: Bottom banner, sidebar, in-content
- ✅ **Privacy Policy**: COPPA compliant
- ✅ **Responsive Ads**: Mobile and desktop optimized

### Activate Your Ads

1. **Add Your Site to AdSense**
   - Go to [Google AdSense](https://www.google.com/adsense)
   - Sites → Add Site → Enter your deployed URL

2. **Create Ad Units**
   Replace these placeholder IDs in the code:
   - `1234567890` - Mobile banner ad
   - `1234567891` - Desktop banner ad  
   - `1234567892` - In-content ad
   - `1234567893` - Sidebar ad

3. **Files to Update** (after creating ad units):
   - `src/components/ads/BottomBannerAd.js`
   - `src/components/ads/InContentAd.js`
   - `src/components/ads/SidebarAd.js`

### Revenue Expectations
- **1,000 daily users**: $50-200/month
- **5,000 daily users**: $250-1,000/month
- **10,000+ daily users**: $500-2,000+/month

*Parenting niche typically has higher CPM rates*
