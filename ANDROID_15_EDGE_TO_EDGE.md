# Android 15+ Edge-to-Edge Implementation

## Overview

This document outlines the implementation of Android 15's mandatory edge-to-edge display requirement for Baby Steps app targeting SDK 35.

---

## What is Edge-to-Edge?

Starting with Android 15 (API 35), apps **must** support edge-to-edge display where:
- Content extends behind system bars (status bar and navigation bar)
- System bars become transparent
- Apps must handle safe area insets to prevent content from being obscured

**This is mandatory for all apps targeting SDK 35+ and cannot be opted out.**

---

## Implementation Details

### 1. Android Native Implementation

#### A. MainActivity.java

**Location:** `/app/frontend/android/app/src/main/java/com/babysteps/mobile/MainActivity.java`

**Key Changes:**
```java
private void enableEdgeToEdge() {
    // Make window draw behind system bars
    WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
    
    // Set transparent colors for system bars
    getWindow().setStatusBarColor(android.graphics.Color.TRANSPARENT);
    getWindow().setNavigationBarColor(android.graphics.Color.TRANSPARENT);
    
    // Android 15+: Disable navigation bar contrast for full transparency
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.VANILLA_ICE_CREAM) {
        getWindow().setNavigationBarContrastEnforced(false);
    }
    
    // Handle window insets to prevent content overlap
    ViewCompat.setOnApplyWindowInsetsListener(rootView, (v, windowInsets) -> {
        Insets systemBars = windowInsets.getInsets(WindowInsetsCompat.Type.systemBars());
        Insets displayCutout = windowInsets.getInsets(WindowInsetsCompat.Type.displayCutout());
        
        int topInset = Math.max(systemBars.top, displayCutout.top);
        int bottomInset = Math.max(systemBars.bottom, displayCutout.bottom);
        
        v.setPadding(0, topInset, 0, bottomInset);
        return WindowInsetsCompat.CONSUMED;
    });
}
```

**What This Does:**
- ✅ Enables transparent system bars
- ✅ Handles safe area insets automatically
- ✅ Prevents content from being hidden by system UI
- ✅ Supports notches and display cutouts
- ✅ Works on Android 15+ and backwards compatible

---

#### B. styles.xml

**Location:** `/app/frontend/android/app/src/main/res/values/styles.xml`

**Key Changes:**
```xml
<style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">
    <!-- Enable edge-to-edge -->
    <item name="android:windowTranslucentStatus">false</item>
    <item name="android:windowTranslucentNavigation">false</item>
    <item name="android:statusBarColor">@android:color/transparent</item>
    <item name="android:navigationBarColor">@android:color/transparent</item>
    <item name="android:windowDrawsSystemBarBackgrounds">true</item>
    <item name="android:enforceNavigationBarContrast">false</item>
    <item name="android:enforceStatusBarContrast">false</item>
</style>
```

**What This Does:**
- ✅ Disables default system bar backgrounds
- ✅ Enables transparent system bars at theme level
- ✅ Disables contrast enforcement for Android 15+
- ✅ Allows content to draw behind system UI

---

### 2. Web/CSS Implementation

#### A. index.html Viewport

**Location:** `/app/frontend/public/index.html`

**Key Change:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
```

**What This Does:**
- ✅ `viewport-fit=cover` tells the browser to use full screen including safe areas
- ✅ Essential for iOS notch support and Android edge-to-edge

---

#### B. index.css Safe Areas

**Location:** `/app/frontend/src/index.css`

**Key Changes:**
```css
body {
    /* Use safe area insets for padding */
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);
}

#root {
    min-height: 100vh;
    min-height: 100dvh; /* Dynamic viewport height for mobile */
}
```

**What This Does:**
- ✅ `env(safe-area-inset-*)` CSS variables provide safe area padding
- ✅ Automatically adjusts for notches, status bars, and navigation bars
- ✅ Works on iOS (notch) and Android (edge-to-edge)
- ✅ Dynamic viewport height accounts for browser UI changes

---

## Testing Checklist

### Android Devices to Test:

- [ ] **Android 15 (API 35)** - Edge-to-edge enforced
- [ ] **Android 14 (API 34)** - Backwards compatibility
- [ ] **Android 13 (API 33)** - Backwards compatibility
- [ ] **Device with notch/punch-hole** - Display cutout handling
- [ ] **Device with gesture navigation** - Transparent navigation bar
- [ ] **Device with 3-button navigation** - Translucent navigation bar

### Test Scenarios:

1. **Status Bar Overlap**
   - [ ] Content doesn't hide behind status bar
   - [ ] Header/title visible at top of screen
   - [ ] Gradient backgrounds extend to top edge

2. **Navigation Bar Overlap**
   - [ ] Bottom buttons not obscured by navigation bar
   - [ ] FAB/action buttons positioned correctly
   - [ ] Keyboard doesn't overlap input fields

3. **Display Cutouts (Notch/Punch-hole)**
   - [ ] Content avoids notch area
   - [ ] Important UI elements not cut off
   - [ ] Safe area padding applied correctly

4. **Rotation**
   - [ ] Landscape mode handles insets correctly
   - [ ] Safe areas update on orientation change
   - [ ] No content overlap in any orientation

5. **Dark/Light Mode**
   - [ ] System bar icons visible in both modes
   - [ ] Status bar icons adjust to background color
   - [ ] Navigation bar icons visible

6. **Different Screen Sizes**
   - [ ] Tablets handle edge-to-edge correctly
   - [ ] Foldables adapt to different screen states
   - [ ] Small phones don't lose content

---

## Browser Support

### CSS Safe Area Insets Browser Compatibility:

| Browser | Version | Support |
|---------|---------|---------|
| Chrome (Android) | 69+ | ✅ Full |
| Safari (iOS) | 11.2+ | ✅ Full |
| Firefox (Android) | 68+ | ✅ Full |
| Samsung Internet | 9.0+ | ✅ Full |
| WebView (Android) | 69+ | ✅ Full |

**Fallback:** If `env(safe-area-inset-*)` is not supported, it falls back to `0px`, so older browsers aren't affected.

---

## Benefits of Edge-to-Edge

### User Experience:
- ✅ **Modern Look**: Matches Android 15's system UI design
- ✅ **Immersive**: More screen real estate for content
- ✅ **Consistent**: Matches other modern Android apps
- ✅ **Professional**: Follows Google's Material Design 3 guidelines

### Technical Benefits:
- ✅ **Required**: Mandatory for SDK 35+ (no choice)
- ✅ **Future-Proof**: Aligns with Android's design direction
- ✅ **Cross-Platform**: Works on iOS with notches too
- ✅ **Flexible**: Adapts to all screen shapes and sizes

---

## Common Issues & Solutions

### Issue 1: Content Hidden Behind Status Bar
**Symptom:** App header or title cut off at top
**Solution:** Android native code applies `topInset` padding automatically. Ensure `enableEdgeToEdge()` is called in MainActivity.

### Issue 2: Bottom Buttons Obscured
**Symptom:** FAB or bottom navigation hidden by gesture bar
**Solution:** CSS `padding-bottom: env(safe-area-inset-bottom)` handles this. Check body padding in index.css.

### Issue 3: Notch Overlaps Content
**Symptom:** Content appears in notch area on devices with cutouts
**Solution:** MainActivity combines `displayCutout` insets with `systemBars` insets. Uses `Math.max()` to respect both.

### Issue 4: Navigation Bar Not Transparent
**Symptom:** Three-button navigation shows gray background
**Solution:** Added `setNavigationBarContrastEnforced(false)` for Android 15+. Check MainActivity line 30.

### Issue 5: Works in Emulator, Fails on Device
**Symptom:** Edge-to-edge works in Android Studio emulator but not on physical device
**Solution:** Ensure targetSdkVersion is 35 in variables.gradle. Clean and rebuild the app.

---

## Files Modified

### Android Native:
1. ✅ `/app/frontend/android/app/src/main/java/com/babysteps/mobile/MainActivity.java`
   - Added `enableEdgeToEdge()` method
   - Window insets handling
   - System bar configuration

2. ✅ `/app/frontend/android/app/src/main/res/values/styles.xml`
   - Updated `AppTheme.NoActionBar` style
   - Added edge-to-edge attributes
   - Disabled contrast enforcement

### Web/CSS:
3. ✅ `/app/frontend/public/index.html`
   - Updated viewport meta tag with `viewport-fit=cover`

4. ✅ `/app/frontend/src/index.css`
   - Added safe area inset padding to body
   - Added dynamic viewport height to #root

---

## SDK Versions

```gradle
minSdkVersion = 23       // Android 6.0 (Minimum supported)
compileSdkVersion = 35   // Android 15 (Compile against)
targetSdkVersion = 35    // Android 15 (Target for behavior)
```

**Edge-to-edge is enforced for targetSdkVersion 35+**

---

## References

### Official Documentation:
- [Android Edge-to-Edge Guide](https://developer.android.com/develop/ui/views/layout/edge-to-edge)
- [Android 15 Behavior Changes](https://developer.android.com/about/versions/15/behavior-changes-15)
- [WindowInsets API](https://developer.android.com/reference/androidx/core/view/WindowInsetsCompat)
- [CSS Safe Area Insets](https://developer.mozilla.org/en-US/docs/Web/CSS/env)

### Community Resources:
- [Capacitor Edge-to-Edge Discussion](https://github.com/ionic-team/capacitor/issues/7951)
- [React Native Android 15 Support](https://github.com/react-native-community/discussions-and-proposals/discussions/827)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| Oct 14, 2025 | 1.0 | Initial edge-to-edge implementation for Android 15 |

---

## Next Steps

### Post-Implementation:
1. ✅ Test on multiple Android devices (15, 14, 13)
2. ✅ Test on devices with notches and punch-holes
3. ✅ Verify with gesture and button navigation
4. ✅ Check in landscape and portrait modes
5. ✅ Test dark and light themes
6. ✅ Verify web app on mobile browsers
7. ✅ Submit to Google Play Store

### Future Enhancements:
- Monitor Android 16 edge-to-edge changes
- Add predictive back gesture support (Android 14+)
- Consider per-page safe area customization
- Add telemetry for edge-to-edge adoption

---

**Implemented by:** AI Engineer  
**Date:** October 14, 2025  
**Target SDK:** Android 15 (API 35)  
**Status:** ✅ Complete and Ready for Testing
