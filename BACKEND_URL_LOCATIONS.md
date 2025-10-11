# Backend URL Configuration Locations

## Overview
This document lists every location where the backend URL `https://baby-genius.preview.emergentagent.com` has been configured throughout the Baby Steps application. When moving to production, ALL of these locations must be updated to point to the production backend server.

## Current Backend URL
**Development/Preview**: `https://baby-genius.preview.emergentagent.com`
**Production**: `[TO BE UPDATED]`

---

## 🔧 Configuration Files

### 1. Frontend Environment Files
**Location**: `/app/frontend/.env`
```
REACT_APP_BACKEND_URL=https://baby-genius.preview.emergentagent.com
```

**Location**: `/app/frontend/.env.production` 
```
REACT_APP_BACKEND_URL=https://baby-genius.preview.emergentagent.com
```

**Location**: `/app/frontend/.env.local`
```
REACT_APP_BACKEND_URL=https://baby-genius.preview.emergentagent.com
```

### 2. Backend Environment Files
**Location**: `/app/backend/.env`
```
# No backend URL configured here - uses MONGO_URL and other configs
```

---

## 🤖 GitHub Workflows

### 3. Android Build Workflow
**Location**: `/app/.github/workflows/android-build.yml`
**Line**: ~133
```yaml
echo "REACT_APP_BACKEND_URL=https://baby-genius.preview.emergentagent.com" > .env.production
```

**Line**: ~141
```yaml
env:
  REACT_APP_BACKEND_URL: https://baby-genius.preview.emergentagent.com
```

---

## 📱 Mobile Configuration

### 4. Capacitor Configuration
**Location**: `/app/frontend/capacitor.config.json`
```json
"server": {
  "cleartext": true,
  "allowNavigation": [
    "https://baby-genius.preview.emergentagent.com",
    "https://baby-genius.preview.emergentagent.com/*"
  ]
}
```

### 5. Android Network Security Config
**Location**: `/app/frontend/android/app/src/main/res/xml/network_security_config.xml`
```xml
<domain includeSubdomains="true">emergentagent.com</domain>
<domain includeSubdomains="true">baby-genius.preview.emergentagent.com</domain>
```

---

## 💻 Application Code

### 6. App.js Configuration
**Location**: `/app/frontend/src/App.js`
**Line**: ~45
```javascript
const API = process.env.REACT_APP_BACKEND_URL;
```
*Note: This uses environment variable, so updating .env files will update this*

### 7. AIAssistant Component
**Location**: `/app/frontend/src/components/AIAssistant.js`
**Line**: ~84
```javascript
const response = await androidFetch(`${process.env.REACT_APP_BACKEND_URL}/api/ai/chat`, {
```
*Note: This uses environment variable, so updating .env files will update this*

### 8. Offline Mode Configuration
**Location**: `/app/frontend/src/offlineMode.js`
**Line**: ~10
```javascript
return !process.env.REACT_APP_BACKEND_URL;
```
*Note: This checks for environment variable presence, so updating .env files will update this*

---

## 📋 Production Deployment Checklist

When deploying to production, update the backend URL in ALL of the following locations:

### ✅ Environment Files (3 locations)
- [ ] `/app/frontend/.env`
- [ ] `/app/frontend/.env.production`
- [ ] `/app/frontend/.env.local`

### ✅ GitHub Workflows (2 locations)
- [ ] `/app/.github/workflows/android-build.yml` (line ~133)
- [ ] `/app/.github/workflows/android-build.yml` (line ~141)

### ✅ Mobile Configuration (2 locations)
- [ ] `/app/frontend/capacitor.config.json` (allowNavigation array)
- [ ] `/app/frontend/android/app/src/main/res/xml/network_security_config.xml` (domain entries)

### ✅ Verification Steps
- [ ] Build and test React app with production backend URL
- [ ] Run GitHub Actions workflow to ensure Android build works
- [ ] Test Android app connectivity to production backend
- [ ] Verify OpenAI token consumption from production server
- [ ] Test all AI Assistant functionality on Android device

---

## 🚨 Critical Notes

1. **Environment Variable Priority**: React loads environment variables in this order:
   - `.env.local` (highest priority - overrides everything)
   - `.env.production` (production builds)
   - `.env` (lowest priority)

2. **Android Build Process**: The GitHub workflow overrides environment files during build, so BOTH the workflow AND environment files must be updated.

3. **Network Security**: The Android network security config must include the production domain to allow HTTPS requests.

4. **Capacitor Navigation**: The allowNavigation array in Capacitor config must include the production backend URL for WebView to access it.

---

## 📞 Production Backend Requirements

When setting up the production backend server, ensure it:

1. **Has CORS enabled** for the mobile app domain
2. **Supports HTTPS** (required for Android app security)
3. **Has the same API endpoints** as the current backend:
   - `/api/auth/login`
   - `/api/auth/register`
   - `/api/babies`
   - `/api/ai/chat` (with OpenAI gpt-5-nano support)
4. **Has OpenAI API key** configured with proper permissions
5. **Has MongoDB connection** configured
6. **Runs on port that supports the API routing** (typically 8001 or standard HTTPS port)

---

## 🔄 Update Script Template

```bash
#!/bin/bash
# Production Backend URL Update Script
# Usage: ./update_backend_url.sh "https://your-production-backend.com"

NEW_BACKEND_URL="$1"

if [ -z "$NEW_BACKEND_URL" ]; then
  echo "Usage: $0 <new-backend-url>"
  exit 1
fi

echo "Updating backend URL to: $NEW_BACKEND_URL"

# Update environment files
sed -i "s|REACT_APP_BACKEND_URL=.*|REACT_APP_BACKEND_URL=$NEW_BACKEND_URL|g" frontend/.env
sed -i "s|REACT_APP_BACKEND_URL=.*|REACT_APP_BACKEND_URL=$NEW_BACKEND_URL|g" frontend/.env.production
sed -i "s|REACT_APP_BACKEND_URL=.*|REACT_APP_BACKEND_URL=$NEW_BACKEND_URL|g" frontend/.env.local

# Update GitHub workflow
sed -i "s|REACT_APP_BACKEND_URL=.*|REACT_APP_BACKEND_URL=$NEW_BACKEND_URL|g" .github/workflows/android-build.yml

echo "✅ Backend URL updated in all configuration files"
echo "⚠️  Remember to manually update:"
echo "   - frontend/capacitor.config.json (allowNavigation array)"
echo "   - frontend/android/app/src/main/res/xml/network_security_config.xml (domain entries)"
```

---

*Last Updated: October 11, 2025 - Testing certificate extraction*
*Created by: AI Development Agent*
*Purpose: Production deployment preparation*