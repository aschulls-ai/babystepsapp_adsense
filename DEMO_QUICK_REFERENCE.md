# Baby Steps - Demo Deployment Quick Reference

## 🚀 Deploy Demo (For AdSense Review)

```bash
cd /app/frontend
./deploy-demo.sh
cd build
vercel --prod
```

**Verify:** https://babystepsapp.app
- Should auto-login
- No login page
- Full access to all features

**Check ads.txt:** https://babystepsapp.app/ads.txt

---

## 🔙 Restore Main App (After Approval)

```bash
cd /app/frontend
./restore-main.sh
cd build
vercel --prod
```

**Verify:** https://babystepsapp.app
- Should show login page
- Normal authentication

---

## 📝 Demo Credentials

- **Email:** demo@babysteps.com
- **Password:** demo123

*(Auto-login, no manual entry needed)*

---

## ✅ Pre-Deployment Checklist

- [ ] AdSense code in `<head>` (index.html) ✅
- [ ] ads.txt in `/public` folder ✅
- [ ] Demo files created ✅
- [ ] Backend URL configured
- [ ] Site builds successfully
- [ ] All pages accessible

---

## 🔍 AdSense Requirements

1. ✅ Site live at: babystepsapp.app
2. ✅ ads.txt accessible
3. ✅ No login required for content
4. ✅ Multiple pages with content
5. ✅ Privacy policy page
6. ✅ Terms of service page
7. ✅ Mobile responsive
8. ✅ HTTPS enabled (Vercel automatic)

---

## 📧 AdSense Submission

1. Go to: https://adsense.google.com
2. Sites → Add site
3. Enter: `babystepsapp.app`
4. Code already placed ✅
5. Wait 1-3 days for review
6. After approval, run `restore-main.sh`

---

## ⚡ Quick Commands

### Deploy Demo
```bash
cd /app/frontend && ./deploy-demo.sh
```

### Restore Main
```bash
cd /app/frontend && ./restore-main.sh
```

### Manual Deploy
```bash
cd build && vercel --prod
```

### Check ads.txt
```bash
curl https://babystepsapp.app/ads.txt
```

---

## 🆘 Troubleshooting

### ads.txt not found?
- Check: `/app/frontend/public/ads.txt`
- Rebuild and redeploy

### Auto-login not working?
- Clear browser cache
- Check console for errors
- Verify demo files are active

### Build failed?
- Check Node version: `node -v`
- Clear cache: `rm -rf node_modules && npm install`
- Try: `npm run build`

---

**Need Help?** See full guide: `/app/VERCEL_DEMO_DEPLOYMENT.md`
