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
   REACT_APP_BACKEND_URL=https://babysteps-app.preview.emergentagent.com
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

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
