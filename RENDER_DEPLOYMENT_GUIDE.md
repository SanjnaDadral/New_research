# 🚀 Render Deployment Guide - PaperAIzer

This guide walks you through deploying the PaperAIzer application to Render.

---

## 📋 Pre-Deployment Checklist

### ✅ Local Testing (Before Deployment)

- [ ] Run `python manage.py migrate` locally
- [ ] Run `python manage.py collectstatic --noinput` locally
- [ ] Run `python manage.py test` (if tests exist)
- [ ] Verify the app starts: `python manage.py runserver`
- [ ] Test key features:
  - [ ] User registration & login
  - [ ] PDF/Text/URL analysis
  - [ ] Email OTP password reset
  - [ ] Comparison feature
  - [ ] Export functionality

---

## 🔧 Step 1: Prepare Your Render Account

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub, Google, or email

2. **Connect GitHub Repository**
   - Click "New" → "Web Service"
   - Select "Connect a repository"
   - Choose your GitHub account and the `Analye_Paper-main` repository

---

## 🗄️ Step 2: Create PostgreSQL Database

1. **Create Database**
   - From Render dashboard: "New" → "PostgreSQL"
   - Name: `paper-analyzer-db`
   - Plan: **Free Tier** ✓
   - Region: **Oregon** (same as web service)
   - Click "Create Database"

2. **Database Created**
   - Database will be created and linked automatically
   - Status: "Available" (wait for this)

---

## 🌐 Step 3: Deploy Web Service

### Option A: From GitHub (Recommended)

1. **Create Web Service**
   - Render Dashboard → "New" → "Web Service"
   - Connect GitHub repository: `Analye_Paper-main`
   - Runtime: **Python 3.12**
   - Build Command: `./build.sh`
   - Start Command: `gunicorn paper_analyzer.wsgi:application --workers 1 --timeout 120 --max-requests 1000 --bind 0.0.0.0:$PORT`

2. **Service Name**
   - Name: `paper-analyzer` (must match render.yaml)

3. **Advanced Settings**
   - Auto-Deploy: ✓ (checked)
   - Branch: `main`

4. **Environment Variables**
   - See [Step 4](#step-4-configure-environment-variables) below

---

### Option B: Using render.yaml (Easier!)

1. **Push Changes to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Deploy via Render**
   - Render Dashboard → "New" → "Web Service"
   - Connect GitHub repository
   - Render auto-reads `render.yaml` for configuration
   - Review settings and click "Deploy"

---

## ⚙️ Step 4: Configure Environment Variables

In Render Dashboard → Web Service → "Environment":

### 🔐 Security (Generate in Render)
- **SECRET_KEY** ← Render auto-generates with `generateValue: true`
- **DEBUG** ← Already set to `False` in render.yaml

### 📧 Email Configuration (Required)
Set these in Render Dashboard:

1. **EMAIL_HOST_USER** 
   - Your Gmail email (e.g., `your-email@gmail.com`)

2. **EMAIL_HOST_PASSWORD**
   - Gmail **App Password** (not your regular password!)
   - Get it at: https://myaccount.google.com/apppasswords
   - Steps:
     1. Enable 2-Factor Authentication on your Google Account
     2. Go to myaccount.google.com/apppasswords
     3. Select "Mail" → "Windows Computer" (or other device)
     4. Copy the 16-character password
     5. Paste it here in Render Dashboard

### 🔑 API Keys (Optional but Recommended)
- **GROQ_API_KEY** ← Free from https://console.groq.com (optional; analysis works without it)

### 🎯 Superuser Credentials (Change These!)
**⚠️ SECURITY WARNING: Change the default password!**

In Render Dashboard, set:
- **DJANGO_SUPERUSER_USERNAME** ← Change from `admin`
- **DJANGO_SUPERUSER_PASSWORD** ← Change from `admin@123` (use a strong password!)
- **DJANGO_SUPERUSER_EMAIL** ← Your email

Example secure credentials:
- Username: `admin_secure_123`
- Password: `YourSuperSecurePassword2024!`
- Email: `your-email@gmail.com`

---

## 🚀 Step 5: Deploy

1. **Trigger Deployment**
   ```bash
   git push origin main
   ```
   
   OR manually click "Deploy" in Render Dashboard

2. **Monitor Deployment**
   - Render Dashboard → Web Service → "Logs"
   - Watch for build progress
   - Expected build time: **3-5 minutes**

3. **Verify Deployment**
   ```
   Build Output:
   ✓ Step 1: Installing Python dependencies
   ✓ Step 2: Running database migrations
   ✓ Step 3: Collecting static files
   ✓ Step 4: Setting up sessions
   ✓ Step 5: Creating superuser
   ✓ Step 6: Downloading NLTK data
   ✓ Build complete!
   ```

---

## ✨ Step 6: First Run Setup

1. **Access Your App**
   - URL: `https://paper-analyzer-XXXX.onrender.com`
   - Admin Panel: `https://paper-analyzer-XXXX.onrender.com/admin`

2. **Login to Admin**
   - Username: Your configured superuser username
   - Password: Your configured superuser password

3. **Verify Features**
   - [ ] Registration page works
   - [ ] Login works
   - [ ] Dashboard displays
   - [ ] Analysis features work
   - [ ] Email OTP works (check spam folder)
   - [ ] Comparison feature works

---

## 📊 Monitoring & Logs

### View Logs
```
Render Dashboard → Web Service → "Logs"
```

### Check Disk Usage
```
Render Dashboard → Web Service → "Settings" → "Free tier storage"
```

### Monitor Database
```
Render Dashboard → PostgreSQL → "Info"
```

---

## 🔧 Troubleshooting

### "Build failed" ❌

1. **Check logs** in Render Dashboard
2. **Common issues:**
   - Missing `build.sh` file
   - Python version mismatch
   - Missing dependencies in `requirements.txt`
   - Wrong `PYTHON_VERSION` in render.yaml

### "Application Error" ❌

1. **Check logs** for error messages
2. **Common fixes:**
   - Verify `DATABASE_URL` is set
   - Verify email credentials are correct
   - Check `SECRET_KEY` is generated
   - Run: `curl https://your-app.onrender.com/health` to test

### "Migrations Failed" ❌

1. **Manual Migration**
   ```bash
   # Get shell access via Render CLI or manual command
   python manage.py migrate --noinput
   ```

2. **Reset Database** (if needed)
   - Render Dashboard → PostgreSQL → "Settings"
   - Click "Delete Database" and recreate

### "Email Not Sending" ❌

1. **Verify credentials**
   - Double-check Gmail app password
   - Ensure 2FA is enabled on Google Account

2. **Test email**
   ```bash
   python manage.py test_email
   ```

3. **Check Gmail**
   - Look in SPAM folder
   - Allow "Less secure apps" if needed

### "Session Lost After Login" ❌

Database-backed sessions should prevent this. If issue persists:

1. **Verify session table**
   ```bash
   python manage.py dbshell
   SELECT COUNT(*) FROM django_session;
   ```

2. **Clean expired sessions**
   ```bash
   python manage.py cleanup_sessions
   ```

---

## 📈 Optimization Tips

### Reduce Build Time
- Fewer dependencies = faster builds
- Current build time: ~3-5 minutes

### Reduce Startup Time
- Gunicorn config (already optimized)
- Consider caching with Redis (not included)

### Manage File Storage
- Free tier: Limited ephemeral storage (~400MB)
- Media files reset on redeploy
- Solution: Use Render's object storage (paid) or external service

---

## 🔄 Deployment Updates

### Update Code

1. **Make changes locally**
   ```bash
   git add .
   git commit -m "Fix: describe your change"
   git push origin main
   ```

2. **Render auto-deploys**
   - Automatic on push to main
   - Manual: Dashboard → "Deploy"

### Update Environment Variables

1. **In Render Dashboard**
   - Web Service → "Environment"
   - Edit the variable
   - Click "Save"
   - Service auto-redeploys

---

## 🛑 Stopping the Service

1. **Pause Service**
   - Render Dashboard → Web Service → "Settings"
   - Click "Pause"
   - Service won't consume billing

2. **Resume Service**
   - Click "Resume" when ready

---

## 💰 Cost Estimate

**Free Tier:**
- Web Service: **$0** (450 hours/month limit)
- PostgreSQL Database: **$0** (500 MB limit)
- **Total: $0** for testing

**When to Upgrade:**
- Need persistent storage (upgrade Web Service to paid)
- Need more database storage (upgrade PostgreSQL)
- Need better performance

---

## 📞 Support & Troubleshooting

### Render Documentation
- https://render.com/docs

### Django Documentation
- https://docs.djangoproject.com/en/4.2/

### Common Commands

```bash
# View logs
curl https://your-app.onrender.com/health

# SSH into container (if supported)
render ssh paper-analyzer

# Run management command
render python manage.py command_name

# View database
render dbshell
```

---

## ✅ Deployment Checklist

Before going live:

- [ ] Database is created and "Available"
- [ ] All environment variables are set
- [ ] Build completes without errors
- [ ] Application starts successfully
- [ ] Homepage loads
- [ ] Registration works
- [ ] Login works
- [ ] Analysis features work
- [ ] Email OTP sends (check spam)
- [ ] Admin panel is accessible
- [ ] Superuser password is strong
- [ ] No hardcoded credentials in code
- [ ] DEBUG is False
- [ ] SECRET_KEY is generated

---

## 🎉 You're Live!

Your PaperAIzer app is now running on Render!

**Next Steps:**
1. Share your app URL with users
2. Set up custom domain (optional)
3. Monitor logs for errors
4. Set up email notifications (Render billing)
5. Plan database upgrades if needed

---

**Need Help?** Check the logs or contact Render support at support@render.com
