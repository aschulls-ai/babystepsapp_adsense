# Render Build Command Fix - emergentintegrations Installation

## 🚨 Deployment Error

```
ERROR: Could not find a version that satisfies the requirement emergentintegrations
ERROR: No matching distribution found for emergentintegrations
```

## 🔍 Root Cause

`emergentintegrations` is a **private package** hosted on a custom repository, not available on standard PyPI.

It requires a special installation command with a custom index URL:
```bash
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

## ✅ Solution: Update Render Build Command

### In Render Dashboard:

1. **Go to**: https://dashboard.render.com
2. **Select**: baby-steps-demo-api service
3. **Click**: Settings
4. **Find**: Build Command section
5. **Replace**:
   ```bash
   # OLD (FAILS):
   pip install -r requirements.txt
   
   # NEW (WORKS):
   pip install -r requirements.txt && pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
   ```
6. **Click**: Save Changes
7. **Wait**: Render will automatically redeploy

## 📋 Complete Build Configuration

**Build Command**:
```bash
pip install -r requirements.txt && pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

**Start Command**:
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

**Root Directory**:
```
public-server
```

## 🔄 Alternative: Use render.yaml

If you want to use Infrastructure as Code, the `render.yaml` file already has the correct configuration:

**File**: `/app/public-server/render.yaml`

```yaml
services:
  - type: web
    name: baby-steps-demo-api
    env: python
    buildCommand: "pip install -r requirements.txt && pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/"
    startCommand: "uvicorn app:app --host 0.0.0.0 --port $PORT"
    plan: free
    healthCheckPath: /api/health
    envVars:
      - key: PORT
        value: 10000
      - key: SECRET_KEY
        value: "baby-steps-demo-secret-2025"
      - key: EMERGENT_LLM_KEY
        value: "sk-emergent-41bA272B05dA9709c3"
```

To use render.yaml:
1. Go to Render Dashboard
2. New → Blueprint
3. Connect to your GitHub repo
4. Point to `public-server/render.yaml`

## ✅ Verification

After updating the build command and redeploying:

**Check Render Logs** for:
```
✅ AI integration available
```

**Test AI Endpoint**:
```bash
# Get token first
TOKEN=$(curl -X POST https://baby-steps-demo-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@babysteps.com","password":"demo123"}' | jq -r '.access_token')

# Test AI
curl -X POST https://baby-steps-demo-api.onrender.com/api/ai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message":"When can babies eat strawberries?","baby_age_months":6}'
```

**Expected**: Real AI response (not fallback)

## 📝 Why This Package?

`emergentintegrations` provides:
- Easy access to OpenAI, Anthropic, Google AI models
- Single API key (`EMERGENT_LLM_KEY`) for all LLM providers
- Simplified chat interface with `LlmChat` class
- Cost-effective model selection (gpt-5-nano)

## 🎯 Summary

**Problem**: emergentintegrations not found on PyPI  
**Solution**: Add custom index URL to build command  
**Action**: Update Render Dashboard Build Command setting  
**Time**: ~5 minutes for redeploy  
**Result**: AI features fully functional
