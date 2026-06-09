# 🔑 Render Environment Variables Setup Guide

## Required Actions in Render Dashboard

When you create your Render web service, you **MUST** set these environment variables:

---

## 🔴 CRITICAL: Must Set Manually

### 1. Email Configuration (For OTP Password Reset)

#### EMAIL_HOST_USER
- **Value:** Your Gmail email address
- **Example:** `your-email@gmail.com`
- **Why:** For sending password reset OTP codes
- **Action:** Paste your email in Render Dashboard

#### EMAIL_HOST_PASSWORD
- **Value:** Gmail App Password (NOT your regular password!)
- **Get it:**
  1. Go to https://myaccount.google.com/apppasswords
  2. Make sure 2FA is enabled on your account
  3. Select "Mail" → "Windows Computer"
  4. Copy the 16-character password
  5. Paste it in Render Dashboard
- **Example:** `abcd efgh ijkl mnop` (spaces included)
- **Why:** Gmail doesn't allow regular passwords for apps

### 2. Admin Password (SECURITY CRITICAL ⚠️)

#### DJANGO_SUPERUSER_PASSWORD
- **Current Value:** `admin@123` (NOT SECURE!)
- **Action:** CHANGE THIS IMMEDIATELY in Render Dashboard
- **Suggested:** Use a strong password like `YourSecure@Pass2024!`
- **Why:** Anyone can access your admin panel with default password

---

## 🟡 OPTIONAL: But Recommended

### GROQ_API_KEY
- **Value:** Free API key from https://console.groq.com
- **Why:** Faster, better AI analysis (optional; app works without it)
- **Steps:**
  1. Go to https://console.groq.com
  2. Sign up with Google/GitHub
  3. Create API key
  4. Copy and paste in Render Dashboard
- **Leave empty** if you don't want to set it up

---

## ✅ AUTO-CONFIGURED (No Action Needed)

These are already set in `render.yaml` - you just verify them:

| Variable | Value | Purpose |
|----------|-------|---------|
| PYTHON_VERSION | 3.12.7 | Python runtime |
| DEBUG | False | Security (production) |
| SECRET_KEY | (auto-generated) | Django security |
| ALLOWED_HOSTS | .onrender.com | Domain whitelist |
| DATABASE_URL | (auto-set from PostgreSQL) | Database connection |
| EMAIL_HOST | smtp.gmail.com | Gmail SMTP server |
| EMAIL_PORT | 587 | SMTP port |
| EMAIL_USE_TLS | True | Secure email |
| PDF_MAX_PAGES | 25 | Max pages to analyze |
| PDF_PREFER_FAST | True | Fast PDF processing |
| ANALYSIS_TEXT_CAP | 5000 | Analysis text limit |
| MAX_PDF_UPLOAD_MB | 45 | Max file upload |
| MAX_STORE_PDF_MB | 16 | Max stored file |
| ENABLE_HEAVY_ML | False | Lightweight ML only |
| DJANGO_SUPERUSER_USERNAME | admin | Admin username |
| DJANGO_SUPERUSER_EMAIL | admin@paperyzer.ai | Admin email |

---

## 📋 Step-by-Step Setup

### In Render Dashboard:

1. **Navigate to Web Service**
   ```
   Dashboard → Web Service (paper-analyzer) → Environment
   ```

2. **Add EMAIL_HOST_USER**
   - Click "Add Environment Variable"
   - Key: `EMAIL_HOST_USER`
   - Value: `your-email@gmail.com`
   - Click "Save"

3. **Add EMAIL_HOST_PASSWORD**
   - Click "Add Environment Variable"
   - Key: `EMAIL_HOST_PASSWORD`
   - Value: (your Gmail app password)
   - Click "Save"

4. **Change DJANGO_SUPERUSER_PASSWORD**
   - Find existing variable: `DJANGO_SUPERUSER_PASSWORD`
   - Click "Edit"
   - Change value to strong password
   - Click "Save"

5. **Add GROQ_API_KEY (Optional)**
   - Click "Add Environment Variable"
   - Key: `GROQ_API_KEY`
   - Value: (your key from console.groq.com)
   - Click "Save"

6. **Service Redeploys**
   - Render automatically redeploys after each change
   - Watch logs to confirm deployment

---

## 🔐 How to Get Gmail App Password

### Requirements:
- Google Account with 2FA enabled
- Not a Google Workspace account (those are different)

### Steps:

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup process
   - Confirm phone number

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select:
     - App: "Mail"
     - Device: "Windows Computer" (or your device)
   - Click "Generate"

3. **Copy Password**
   - Google shows 16-character password
   - Copy all of it (including spaces)
   - Example: `abcd efgh ijkl mnop`

4. **Paste in Render**
   - Open Render Dashboard
   - Web Service → Environment
   - Paste password in EMAIL_HOST_PASSWORD

---

## 🧪 Test Email Configuration

After setting environment variables:

1. **Wait for redeploy** (2-3 minutes)

2. **Send test email:**
   ```bash
   # Via Render dashboard shell or local
   python manage.py test_email
   ```

3. **Check your email**
   - Look in INBOX
   - Check SPAM folder too
   - Should see test email from noreply@paperyzer.ai

---

## ❌ Common Mistakes

### ❌ Using Gmail Password Instead of App Password
- Gmail **blocks** this for security
- Always use App Password from apppasswords.google.com

### ❌ Forgetting 2FA
- 2FA must be enabled first
- Then go to apppasswords.google.com
- Without 2FA, apppasswords.google.com won't show

### ❌ Not Changing Default Admin Password
- Default `admin@123` is a security risk
- Anyone who knows this can access your admin panel
- Change it immediately!

### ❌ Empty GROQ_API_KEY
- Analysis works without it (uses fallback AI)
- Only needed if you want better performance
- Safe to leave empty

---

## 🔍 Verify Setup

### Check Environment Variables in Render Dashboard

1. Go to Web Service → "Environment"
2. Verify you see:
   - ✅ EMAIL_HOST_USER (your email)
   - ✅ EMAIL_HOST_PASSWORD (hidden as dots)
   - ✅ DJANGO_SUPERUSER_PASSWORD (hidden as dots)
   - ✅ GROQ_API_KEY (if you added it)

### Test Features After Deployment

1. **Test Login**
   - Go to https://your-app.onrender.com/login
   - Username: `admin` (or your custom username)
   - Password: (your changed password)

2. **Test Email OTP**
   - Go to /forgot-password
   - Enter your email
   - Check spam folder
   - Should receive OTP email

3. **Test Analysis**
   - Upload a PDF or text
   - Should analyze without errors

---

## 📞 Troubleshooting

### "Email not sending" ❌

1. **Check if app password is correct**
   - Go back to https://myaccount.google.com/apppasswords
   - Create a new one
   - Update in Render Dashboard

2. **Check if 2FA is enabled**
   - Go to https://myaccount.google.com/security
   - Look for "2-Step Verification: On"
   - If off, enable it first

3. **Check EMAIL_HOST_USER**
   - Must be the same email as app password
   - Example: `myemail@gmail.com`

4. **Wait for redeploy**
   - Changes take 2-3 minutes
   - Watch logs in Render Dashboard

5. **Run test command**
   ```bash
   python manage.py test_email
   ```

### "Can't login to admin" ❌

1. **Check DJANGO_SUPERUSER_PASSWORD**
   - Make sure you saved it in Render Dashboard
   - Check it's not still the default

2. **Check DJANGO_SUPERUSER_USERNAME**
   - Default is `admin`
   - Use that unless you changed it

3. **Wait for redeploy**
   - Service might still be deploying
   - Check logs

### "Variable not taking effect" ❌

1. **Did you click Save?**
   - After changing a variable, click "Save"
   - Render shows yellow notification while saving

2. **Did service redeploy?**
   - Check "Deployments" tab
   - Should see new deployment in progress
   - Wait for it to complete

3. **Clear browser cache**
   - Press Ctrl+Shift+Delete
   - Clear cookies and cache
   - Try again

---

## 🚀 Summary

### Before Clicking Deploy:

1. ✅ Set EMAIL_HOST_USER (your Gmail)
2. ✅ Set EMAIL_HOST_PASSWORD (app password, not regular)
3. ✅ Change DJANGO_SUPERUSER_PASSWORD (strong password)
4. ⚠️ Optionally set GROQ_API_KEY

### After Deployment:

1. ✅ Test login with new admin password
2. ✅ Test email OTP with test_email command
3. ✅ Test analysis feature
4. ✅ Monitor logs for errors

---

**Ready to deploy?** Follow RENDER_DEPLOYMENT_GUIDE.md for full steps.
