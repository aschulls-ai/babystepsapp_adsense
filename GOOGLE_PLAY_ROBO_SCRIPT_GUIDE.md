# Google Play Pre-Launch Report - Robo Script Guide

## Overview

This guide explains how to upload the Robo script to Google Play Console so the pre-launch report can properly test your Baby Steps app by logging in with demo credentials.

---

## 📄 Robo Script File

**File:** `baby-steps-robo-script.json`  
**Location:** `/app/baby-steps-robo-script.json`

**Purpose:** Guides Google Play's automated testing to:
1. Enter email: `demo@babysteps.com`
2. Enter password: `demo123`
3. Click Sign In button
4. Navigate through all main app pages

---

## 🚀 How to Upload Robo Script to Google Play Console

### Step 1: Download the Robo Script

Download the file from:
- `/app/baby-steps-robo-script.json`

Or copy the content and save as `baby-steps-robo-script.json` on your computer.

---

### Step 2: Go to Google Play Console

1. Visit: https://play.google.com/console
2. Select your **Baby Steps** app
3. Navigate to: **Release → Testing → Pre-launch report**

---

### Step 3: Upload Robo Script

#### Option A: From App Bundle Upload Screen

When uploading a new AAB/APK:

1. After uploading your APB/AAB file
2. Look for **"Pre-launch report settings"** or **"Robo script"** section
3. Click **"Upload Robo script"**
4. Select `baby-steps-robo-script.json`
5. Click **"Save"**

#### Option B: From Pre-Launch Report Settings

1. Go to: **Release → Testing → Pre-launch report**
2. Click **"Manage settings"** or **"Settings"** (gear icon)
3. Find **"Robo script"** section
4. Click **"Upload script"**
5. Select `baby-steps-robo-script.json`
6. Click **"Save"**

---

### Step 4: Verify Upload

After uploading:
- ✅ File name should appear: `baby-steps-robo-script.json`
- ✅ Status: "Script uploaded successfully"
- ✅ The script will be used for future pre-launch tests

---

## 🤖 What the Robo Script Does

### Login Flow:

1. **Waits 2 seconds** for app to load
2. **Enters email:** `demo@babysteps.com`
3. **Waits 0.5 seconds**
4. **Enters password:** `demo123`
5. **Waits 0.5 seconds**
6. **Clicks "Sign In" button**
7. **Waits 3 seconds** for login to complete

### Navigation Flow:

After login, navigates through all pages:
- Dashboard
- Track Activities
- Baby Profile
- Analysis
- AI Parenting Assistant
- Formula Comparison
- Emergency Training
- Settings

Each navigation includes 2-second waits to ensure pages load properly.

---

## 📋 Robo Script Structure

### Key Components:

```json
{
  "title": "Baby Steps Main App - Login and Navigation",
  "description": "Robo script for Baby Steps main app with demo account",
  "actions": [
    {
      "eventType": "VIEW_TEXT_CHANGED",
      "replacementText": "demo@babysteps.com",
      "elementDescriptors": [...]
    },
    {
      "eventType": "VIEW_CLICKED",
      "elementDescriptors": [...]
    },
    {
      "eventType": "WAIT",
      "delayTime": 2000
    }
  ]
}
```

### Event Types Used:

- **WAIT** - Pauses testing to allow UI to load
- **VIEW_TEXT_CHANGED** - Enters text into input fields
- **VIEW_CLICKED** - Clicks buttons or navigation items

---

## 🎯 Element Descriptors

The script uses multiple ways to identify UI elements:

### For Email Input:
```json
{
  "resourceId": "email",
  "text": "Email",
  "className": "android.widget.EditText",
  "contentDescription": "Email",
  "xpath": "//input[@type='email']"
}
```

### For Password Input:
```json
{
  "resourceId": "password",
  "text": "Password",
  "className": "android.widget.EditText",
  "contentDescription": "Password",
  "xpath": "//input[@type='password']"
}
```

### For Login Button:
```json
{
  "text": "Sign In",
  "text": "Login",
  "text": "LOG IN",
  "contentDescription": "Sign In",
  "className": "android.widget.Button"
}
```

**Why multiple descriptors?**
- Ensures Robo can find elements even if implementation changes
- Works with different Android versions
- Handles both native and web views (Capacitor)

---

## 🔄 When to Update Robo Script

Update the script if you:

### 1. Change Login UI
- Different input field IDs
- Different button text
- New login flow

### 2. Change Navigation
- Rename menu items
- Add new pages
- Change page routes

### 3. Add New Test Flows
- Want to test specific features
- Need to test forms
- Want to test error states

---

## 🧪 Testing Your Robo Script Locally

### Using Android Studio:

1. Open Android Studio
2. Go to: **Run → Record Espresso Test**
3. Or: **Tools → Record Espresso Test**
4. Perform the actions manually
5. Export as JSON
6. Compare with your script

### Manual Validation:

1. Check that all `resourceId` and `text` values match your actual UI
2. Verify button text matches exactly
3. Test wait times are sufficient

---

## ⚠️ Common Issues & Solutions

### Issue 1: Script Doesn't Enter Credentials

**Cause:** Element descriptors don't match actual UI

**Solution:**
1. Inspect your login form HTML/React code
2. Check input field IDs and labels
3. Update `elementDescriptors` in script
4. Ensure `type="email"` and `type="password"` are set

### Issue 2: Login Button Not Clicked

**Cause:** Button text doesn't match

**Solution:**
1. Check exact button text in your AuthPage.js
2. Update `text` values in script
3. Add multiple variations if needed

### Issue 3: Navigation Fails

**Cause:** Wait times too short or element names changed

**Solution:**
1. Increase `delayTime` values (3000ms = 3 seconds)
2. Verify navigation menu text matches script
3. Check Layout.js navigation array

### Issue 4: Web View Elements Not Found

**Cause:** Capacitor web views need different selectors

**Solution:**
1. Use `xpath` selectors for web elements
2. Add `className: "android.webkit.WebView"`
3. Use multiple descriptor types

---

## 📊 Pre-Launch Report Results

After Robo script runs, you'll see:

### Success Indicators:
- ✅ Login successful
- ✅ Dashboard loaded
- ✅ All pages navigated
- ✅ No crashes
- ✅ Screenshots of each page

### What Google Tests:
- App stability
- UI rendering
- Memory usage
- Battery consumption
- Security vulnerabilities
- Accessibility issues

### Devices Tested:
- Multiple Android versions (Android 8-14)
- Different screen sizes
- Various manufacturers (Samsung, Google, etc.)

---

## 🔐 Demo Account Requirements

### Credentials Used:
- **Email:** demo@babysteps.com
- **Password:** demo123

### Important:
1. ✅ Account must exist in production database
2. ✅ Credentials must be valid
3. ✅ Account should have sample data for testing
4. ✅ Keep credentials secure but accessible for testing

### Creating Demo Account:

If account doesn't exist:
1. Use your app's signup flow
2. Or insert directly into database
3. Add sample baby profiles
4. Add sample activities/data

---

## 📁 File Locations

### Main Robo Script (For Main App):
```
/app/baby-steps-robo-script.json
```
**Use this:** After reverting from demo version

### Simple Navigation Script:
```
/app/baby-steps-robo-script-simple.json
```
**Use this:** For demo version without login

---

## 🚦 Deployment Workflow

### When Uploading to Google Play:

1. **Build release APK/AAB**
2. **Upload to Google Play Console**
3. **Upload Robo script** (baby-steps-robo-script.json)
4. **Wait for pre-launch report** (30-60 minutes)
5. **Review results**
6. **Fix any issues found**
7. **Promote to production**

---

## 📝 Best Practices

### 1. Use Descriptive Names
- Clear action notes
- Descriptive titles
- Comments for complex flows

### 2. Add Sufficient Waits
- 2-3 seconds between actions
- Longer for API calls
- Consider slow devices

### 3. Test Critical Paths
- Login flow
- Main features
- Purchase flows
- User data operations

### 4. Keep It Simple
- Don't over-complicate
- Focus on happy path
- Test one flow thoroughly

### 5. Update Regularly
- After UI changes
- With new features
- When tests fail

---

## 🔍 Debugging Failed Tests

### Steps to Debug:

1. **Check Pre-Launch Report**
   - View screenshots
   - Check error logs
   - See where script stopped

2. **Review Element Descriptors**
   - Verify IDs match
   - Check text values
   - Validate xpaths

3. **Test Locally**
   - Run app on emulator
   - Check element inspector
   - Verify element properties

4. **Update Script**
   - Fix mismatched descriptors
   - Adjust wait times
   - Add fallback selectors

5. **Re-upload**
   - Upload updated script
   - Trigger new pre-launch test
   - Verify fixes work

---

## 📞 Support Resources

### Google Play Documentation:
- [Pre-Launch Reports](https://support.google.com/googleplay/android-developer/answer/7002270)
- [Robo Scripts](https://firebase.google.com/docs/test-lab/android/robo-ux-test)
- [Test Lab](https://firebase.google.com/docs/test-lab)

### Baby Steps Specific:
- Demo credentials: demo@babysteps.com / demo123
- Login page: AuthPage.js
- Navigation: Layout.js

---

## ✅ Checklist Before Uploading

Pre-upload verification:

- [ ] Robo script file downloaded
- [ ] Demo account exists and is valid
- [ ] Credentials correct (demo@babysteps.com / demo123)
- [ ] Element descriptors match current UI
- [ ] Navigation menu items match script
- [ ] Wait times are sufficient
- [ ] File is valid JSON (no syntax errors)
- [ ] Script tested locally (optional)

---

## 🎉 Success!

After successful upload:
- ✅ Robo script appears in console
- ✅ Future builds use this script
- ✅ Pre-launch tests login automatically
- ✅ Full app coverage in reports

---

**Created:** October 14, 2025  
**File:** baby-steps-robo-script.json  
**Purpose:** Google Play Pre-Launch Report Testing  
**Demo Account:** demo@babysteps.com / demo123
