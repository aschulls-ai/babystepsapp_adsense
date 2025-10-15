package com.babysteps.mobile;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebView;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Enable WebView debugging
        WebView.setWebContentsDebuggingEnabled(true);
        
        // Enable edge-to-edge display for Android 15+
        enableEdgeToEdge();
    }
    
    private void enableEdgeToEdge() {
        // Make status bar and navigation bar transparent
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        
        // Set status bar and navigation bar colors to transparent
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            getWindow().setStatusBarColor(android.graphics.Color.TRANSPARENT);
            getWindow().setNavigationBarColor(android.graphics.Color.TRANSPARENT);
            
            // For Android 15+, disable navigation bar contrast enforcement for full transparency
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.VANILLA_ICE_CREAM) {
                getWindow().setNavigationBarContrastEnforced(false);
            }
        }
        
        // Handle system bar insets to prevent content from being hidden
        View rootView = findViewById(android.R.id.content);
        if (rootView != null) {
            ViewCompat.setOnApplyWindowInsetsListener(rootView, (v, windowInsets) -> {
                // Get system bar insets
                Insets systemBars = windowInsets.getInsets(WindowInsetsCompat.Type.systemBars());
                Insets displayCutout = windowInsets.getInsets(WindowInsetsCompat.Type.displayCutout());
                
                // Combine system bars and display cutout insets
                int topInset = Math.max(systemBars.top, displayCutout.top);
                int bottomInset = Math.max(systemBars.bottom, displayCutout.bottom);
                
                // Apply padding to prevent content from being hidden by system UI
                // Only apply top and bottom padding, leave sides for true edge-to-edge
                v.setPadding(0, topInset, 0, bottomInset);
                
                return WindowInsetsCompat.CONSUMED;
            });
        }
        
        // Make system bars icons dark or light based on content
        View decorView = getWindow().getDecorView();
        int systemUiVisibility = decorView.getSystemUiVisibility();
        
        // Use light icons on dark background, dark icons on light background
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            systemUiVisibility |= View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            systemUiVisibility |= View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
        }
        
        decorView.setSystemUiVisibility(systemUiVisibility);
    }
}
