# 🔧 Email OTP Not Sending - Complete Fix Guide

## 🎯 Problem

On Render live, when users reset their password:
- ✅ "OTP sent to email" message shows
- ❌ But NO email arrives in inbox
- ❌ OTP not received

## 🔍 Root Cause

Email configuration is **missing or incorrect** in Render environment variables. The code is working, but SMTP credentials aren't properly configured.

---

## ✅ Solution: Configure Email in Render

### **Step 1: Get Email Credentials**

#### **Option A: Gmail (Recommended for Development)**

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter: "PaperAIzer Render"
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

#### **Option B: SendGrid (Recommended for Production)**

1. Sign up at https://sendgrid.com/ (Free tier: 100 emails/day)
2. Create API key in Settings → API Keys
3. Use these settings:
   - Host: `smtp.sendgrid.net`
   - Port: `587`
   - Username: `apikey` (literally the word "apikey")
   - Password: Your SendGrid API key

#### **Option C: AWS SES, Mailgun, etc.**

Follow your email provider's SMTP documentation.

---

### **Step 2: Add Environment Variables in Render**

1. Go to your Render dashboard
2. Select your web service
3. Click **Environment** tab
4. Click **Add Environment Variable**
5. Add these variables:

#### **For Gmail:**

| Key | Value | Example |
|-----|-------|---------|
| `EMAIL_HOST` | `smtp.gmail.com` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` | `587` |
| `EMAIL_USE_TLS` | `True` | `True` |
| `EMAIL_HOST_USER` | Your Gmail address | `your.email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | App Password (16 chars) | `abcd efgh ijkl mnop` |
| `DEFAULT_FROM_EMAIL` | Your Gmail or display name | `PaperAIzer <your.email@gmail.com>` |

#### **For SendGrid:**

| Key | Value | Example |
|-----|-------|---------|
| `EMAIL_HOST` | `smtp.sendgrid.net` | `smtp.sendgrid.net` |
| `EMAIL_PORT` | `587` | `587` |
| `EMAIL_USE_TLS` | `True` | `True` |
| `EMAIL_HOST_USER` | `apikey` | `apikey` |
| `EMAIL_HOST_PASSWORD` | Your API key | `SG.xxxxxxxxxxxx` |
| `DEFAULT_FROM_EMAIL` | Verified sender email | `noreply@yourdomain.com` |

6. **Click "Save Changes"**
7. **Wait for service to redeploy** (automatic)

---

### **Step 3: Test Email Configuration**

After Render redeploys:

1. **Go to Render Shell** (Shell tab in your service)

2. **Run diagnostic:**
   ```bash
   python manage.py test_email
   ```

3. **Expected output:**
   ```
   ✅ Using SMTP backend (correct)
   ✅ EMAIL_HOST configured: smtp.gmail.com
   ✅ EMAIL_HOST_USER configured
   ✅ EMAIL_HOST_PASSWORD configured
   ✅ TLS enabled
   ✅ Configuration looks good!
   ```

4. **Send test email:**
   ```bash
   python manage.py test_email --to your@email.com
   ```

5. **Check your inbox** (and spam folder!)

---

### **Step 4: Test Password Reset**

1. Go to your live site
2. Click "Forgot Password"
3. Enter your email
4. Click "Send OTP"
5. **Check your email inbox** (and spam folder!)
6. You should receive OTP within 1-2 minutes

---

## 🔧 Troubleshooting

### **Issue: "Configuration looks good" but still no email**

**Check Render Logs:**
```bash
# In Render Shell:
tail -f logs/app.log
```

Look for:
- `✅ OTP email sent successfully to...` (Success)
- `❌ SMTP Error sending OTP...` (Failed - see error details)

### **Issue: "Authentication failed" error**

**For Gmail:**
- ✅ Did you enable 2-Factor Authentication?
- ✅ Are you using App Password (not regular password)?
- ✅ Did you copy the App Password exactly (remove spaces)?

**Test authentication:**
```bash
python manage.py shell
```
```python
from django.core.mail import send_mail
from django.conf import settings

print(f"Host: {settings.EMAIL_HOST}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"Pass: {'*' * len(settings.EMAIL_HOST_PASSWORD)}")

# Try sending test email
try:
    result = send_mail(
        'Test',
        'This is a test',
        settings.EMAIL_HOST_USER,
        ['your@email.com'],
        fail_silently=False,
    )
    print(f"Success! Result: {result}")
except Exception as e:
    print(f"Error: {e}")
```

### **Issue: "Connection timeout"**

**Possible causes:**
1. Wrong port number (should be `587` for TLS)
2. Firewall blocking SMTP
3. EMAIL_TIMEOUT too short

**Fix:**
Add to Render environment variables:
```
EMAIL_TIMEOUT=30
```

### **Issue: Email goes to spam**

**Solutions:**
1. **Check spam folder first!** (Most common issue)
2. **Add sender to contacts**
3. **Use proper FROM address** (not noreply if not verified)
4. **For production:** Use verified domain with SPF/DKIM records

### **Issue: Gmail says "Less secure apps"**

**Gmail no longer supports "less secure apps"** - You **MUST** use App Password.

1. Enable 2FA on Gmail
2. Generate App Password at: https://myaccount.google.com/apppasswords
3. Use that 16-character password (not your Gmail password)

### **Issue: SendGrid "Sender not verified"**

SendGrid requires sender verification:

1. Go to SendGrid → Settings → Sender Authentication
2. Verify your domain OR single sender email
3. Use that verified email in `DEFAULT_FROM_EMAIL`

---

## 📊 Verify Email Configuration

### **Quick Check Script:**

Save this and run it to verify all settings:

```bash
python manage.py test_email
```

### **Check Environment Variables:**

```bash
# In Render Shell:
echo $EMAIL_HOST
echo $EMAIL_PORT
echo $EMAIL_HOST_USER
echo $EMAIL_USE_TLS
# Don't echo EMAIL_HOST_PASSWORD (it's secret!)
```

### **Check Settings in Django:**

```bash
python manage.py shell
```
```python
from django.conf import settings

print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"TLS: {settings.EMAIL_USE_TLS}")
print(f"User: {settings.EMAIL_HOST_USER}")
print(f"Pass set: {bool(settings.EMAIL_HOST_PASSWORD)}")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")
```

---

## 🎯 Common Email Providers Configuration

### **Gmail**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=<16-char-app-password>
```

### **SendGrid**
```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<your-api-key>
```

### **Outlook/Office365**
```
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@outlook.com
EMAIL_HOST_PASSWORD=<your-password>
```

### **AWS SES**
```
EMAIL_HOST=email-smtp.<region>.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<SMTP-username>
EMAIL_HOST_PASSWORD=<SMTP-password>
```

### **Mailgun**
```
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@<your-domain>
EMAIL_HOST_PASSWORD=<smtp-password>
```

---

## 🛡️ Security Best Practices

1. **Never commit credentials to git**
   - Use environment variables only
   - Check `.env` is in `.gitignore`

2. **Use App Passwords for Gmail**
   - Don't use your actual Gmail password
   - Rotate App Passwords periodically

3. **For production:**
   - Use dedicated email service (SendGrid, AWS SES)
   - Set up SPF/DKIM/DMARC records
   - Use verified domain

4. **Monitor email delivery:**
   - Check Render logs regularly
   - Set up alerts for email failures
   - Test regularly

---

## 📋 Deployment Checklist

After configuring email:

- [ ] Environment variables added in Render
- [ ] Service redeployed automatically
- [ ] `python manage.py test_email` shows all ✅
- [ ] Test email sent successfully
- [ ] Test email received (check spam!)
- [ ] Password reset OTP received
- [ ] OTP verification works
- [ ] Password reset completes successfully
- [ ] Can login with new password

---

## 🆘 Still Not Working?

### **Check Render Logs in Real-Time:**

1. Go to Render Dashboard → Your Service → Logs
2. Click "Forgot Password" on your site
3. Watch logs for:
   ```
   Processing OTP email request for...
   Attempting to send OTP email via SMTP...
   ✅ OTP email sent successfully
   ```

### **Enable Debug Logging:**

Add to Render environment variables:
```
DEBUG=True
```

Then check logs for detailed error messages.

⚠️ **Remember to set `DEBUG=False` after troubleshooting!**

---

## 📚 Related Files

- **Email Test Command:** `analyzer/management/commands/test_email.py`
- **OTP Utilities:** `analyzer/otp_utils.py`
- **Views:** `analyzer/views.py` (forgot_password function)
- **Settings:** `paper_analyzer/settings.py` (EMAIL_* settings)

---

## ✅ Success Indicators

When everything is working correctly:

1. **In Render Logs:**
   ```
   Processing OTP email request for user@email.com
   Attempting to send OTP email via SMTP to user@email.com
   ✅ OTP email sent successfully to user@email.com
   ```

2. **User sees:**
   - "An OTP has been sent to your email"
   - Email arrives within 1-2 minutes
   - OTP verification succeeds
   - Password reset completes

3. **Test command shows:**
   ```
   ✅ Using SMTP backend (correct)
   ✅ EMAIL_HOST configured
   ✅ EMAIL_HOST_USER configured
   ✅ EMAIL_HOST_PASSWORD configured
   ✅ TEST EMAIL SENT SUCCESSFULLY!
   ```

---

**Status:** ⚠️  Requires Configuration  
**Priority:** 🔴 Critical  
**Estimated Time:** 10-15 minutes  

**Next Steps:**
1. Get email credentials (Gmail App Password or SendGrid API key)
2. Add environment variables in Render
3. Wait for redeploy
4. Test with `python manage.py test_email --to your@email.com`
5. Test password reset flow
