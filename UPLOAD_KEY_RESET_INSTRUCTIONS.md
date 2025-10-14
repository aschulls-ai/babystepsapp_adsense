# Upload Key Reset Instructions for Google Play

## ✅ Certificate Exported Successfully!

Your upload key certificate has been exported in PEM format as requested by Google Play Developer Support.

---

## 📋 Key Information

**Keystore Details:**
- **Alias:** `babysteps-upload`
- **Algorithm:** RSA 2048-bit
- **Valid Until:** March 1, 2053 (27+ years)
- **SHA1 Fingerprint:** `82:DF:2D:DF:8F:5D:45:AD:F3:F5:7C:30:0A:08:33:AC:8C:23:13:F1`

**Certificate File Location:**
- `/app/upload_certificate.pem`

---

## 🚀 Next Steps to Reset Upload Key in Google Play Console

### Step 1: Go to Google Play Console

1. Navigate to: **Test and release > App integrity**
2. Click on **Play app signing** 
3. Click on **Settings** (top right)

### Step 2: Request Upload Key Reset

1. Click on **"Request upload key reset"**
2. You'll be prompted to provide a reason (mention the email from support)
3. **Upload the PEM file** (`upload_certificate.pem`)

### Step 3: Provide the Certificate

You can either:

**Option A:** Download the certificate file from this server:
- File path: `/app/upload_certificate.pem`
- Download it and upload to Google Play Console

**Option B:** Copy and paste the certificate content directly:

```
-----BEGIN CERTIFICATE-----
MIIDhDCCAmygAwIBAgIJAIJADcuXyvHDMA0GCSqGSIb3DQEBDAUAMG8xCzAJBgNV
BAYTAlVTMQ4wDAYDVQQIEwVTdGF0ZTENMAsGA1UEBxMEQ2l0eTETMBEGA1UEChMK
QmFieSBTdGVwczEXMBUGA1UECxMOQmFieSBTdGVwcyBBcHAxEzARBgNVBAMTCkJh
YnkgU3RlcHMwIBcNMjUxMDE0MDYxNDE2WhgPMjA1MzAzMDEwNjE0MTZaMG8xCzAJ
BgNVBAYTAlVTMQ4wDAYDVQQIEwVTdGF0ZTENMAsGA1UEBxMEQ2l0eTETMBEGA1UE
ChMKQmFieSBTdGVwczEXMBUGA1UECxMOQmFieSBTdGVwcyBBcHAxEzARBgNVBAMT
CkJhYnkgU3RlcHMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDWuIuz
6L9axABepuXa87dvPa/Dm/cRGEzWsU5I9QNjKfaMeki/L2PUclftvOdW22umTQ8N
+vuUQyXa84CdlgH+5zYnFoobHf/5vnX+q06Py8E+3a9TJj/NcdXcrJa715syLSOx
pOcbJ1X83HgnfTwNp0rppvEOUM2ZTOyhOLj/VDP83DAFNvdvER0OTsQqsJ4Tf6dr
29oE4EKP4krIas/5F377Xz4azaHKjbtdCoMD9NlxUjKNWU+J1jDey7qX8UyFZnx1
0x3FnL7/C4pWRVwZcW1pPNTSjiyoboyngJJtjYbYODRmmVMz8Ciz+6eTkGaYg0Xm
qB10hfVvEz/aYVs/AgMBAAGjITAfMB0GA1UdDgQWBBQuYkig7stpKA35U56jbfoH
MRyNnjANBgkqhkiG9w0BAQwFAAOCAQEAOAzeGkawn/f2mdGYl/0p+X7uMX/nbymj
eAbomVDiH3M8ZmxsYl2OAqXPAkkAjPdU7lipu2ZK6db1Nj2uNLslHaug4dRCC7gj
WcqO1nUA5HtW+yMr5qWCWvKJkyEJxI6pf5JU/CX7oEaohDCKllAnu+BFMk2T1/AB
qRxYs3G+JAs8QUvAMsGWx/1r76d7TCVlUHLR3/02jz4KHiaKaNmewJhInNwz5/E+
6iD4KYa+eXPnA2O8AEwOyWLk2RXSVJHLk8ta6jrxDzE8GjaYmP3Tk595UmqlCXHe
37GFm0vWWvRdzryEehuKAs/LP9Ye6O4djm7qoy/J6BQkER699hTUuw==
-----END CERTIFICATE-----
```

### Step 4: Confirm Reset

1. Provide a reason for the reset (e.g., "Following Google support instructions to reset upload key")
2. Submit the request
3. **Wait 48 hours** before uploading new builds (as mentioned in Google's email)

### Step 5: After 48 Hours

Once Google processes the reset:
1. Your existing keystore will continue to work
2. New uploads will be accepted with your current upload key
3. No changes needed to your GitHub Actions workflow
4. The SHA1 fingerprint will remain: `82:DF:2D:DF:8F:5D:45:AD:F3:F5:7C:30:0A:08:33:AC:8C:23:13:F1`

---

## 📱 Important Notes

### ✅ What You Already Have Configured

Your GitHub repository already has the correct setup:
- ✅ Keystore stored in GitHub Secret: `ANDROID_KEYSTORE_BASE64`
- ✅ Password stored in GitHub Secret: `KEYSTORE_PASSWORD` = `BabySteps2024!`
- ✅ Key alias stored in GitHub Secret: `KEY_ALIAS` = `babysteps-upload`
- ✅ GitHub Actions workflow configured to use these secrets

### 🔐 Security

- The keystore is safely stored in GitHub Secrets
- The password is: `BabySteps2024!`
- Keep this password secure
- Never commit the keystore file to Git

### 🔄 No Changes Needed

After the reset is complete:
- Your GitHub Actions builds will continue to work
- No code changes required
- No configuration changes needed
- Just wait 48 hours after submitting the reset request

---

## 📞 Support Reference

**Google Play Developer Support Ticket:**
- Your app: `com.babysteps.app`
- Email received: October 14, 2024
- Action: Upload key reset

---

## ✅ Checklist

- [x] Certificate exported in PEM format
- [ ] Upload PEM certificate to Google Play Console
- [ ] Submit upload key reset request
- [ ] Wait 48 hours
- [ ] Test new build upload after 48 hours

---

## Questions?

If you encounter any issues:
1. Reference the Google support email
2. Ensure the PEM file is uploaded correctly
3. Verify the SHA1 fingerprint matches: `82:DF:2D:DF:8F:5D:45:AD:F3:F5:7C:30:0A:08:33:AC:8C:23:13:F1`
4. Contact Google Play Developer Support if needed

---

**Created:** October 14, 2025
**Certificate File:** `/app/upload_certificate.pem`
