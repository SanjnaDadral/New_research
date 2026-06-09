# 🚀 Quick Fix: Email OTP Not Sending on Render

## ❌ Problem
Password reset says "OTP sent" but email never arrives.

## ✅ Cause
Email credentials not configured in Render environment variables.

---

## 🔧 Fix (5 Minutes)

### **Step 1: Get Gmail App Password**

1. Go to: https://myaccount.google.com/apppasswords
2. Enable 2FA if not already enabled
3. Generate new App Password for "Mail"
4. **Copy the 16-character password**

### **Step 2: Add to Render**

1. Go to Render Dashboard → Your Service → **Environment** tab
2. Click **Add Environment Variable**
3. Add these:

```
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your.email@gmail.com
EMAIL_HOST_PASSWORD = (paste 16-char App Password)
DEFAULT_FROM_EMAIL = PaperAIzer <your.email@gmail.com>
```

4. Click **Save Changes** (service will redeploy automatically)

### **Step 3: Test**

Wait 2-3 minutes for redeploy, then:

```bash
# In Render Shell:
python manage.py test_email --to your@email.com
```

**Expected:** Test email arrives in 1-2 minutes

### **Step 4: Test Password Reset**

1. Go to your site
2. Click "Forgot Password"
3. Enter email
4. Check inbox (and spam folder!)
5. Enter OTP and reset password

---

## ⚠️ Important Notes

### **For Gmail:**
- ✅ **MUST** use App Password (not regular password)
- ✅ **MUST** enable 2FA first
- ✅ Get App Password: https://myaccount.google.com/apppasswords

### **Common Mistakes:**
- ❌ Using Gmail password instead of App Password
- ❌ Not enabling 2FA before generating App Password
- ❌ Copy/paste errors in App Password (include all 16 chars)
- ❌ Wrong EMAIL_PORT (must be 587 for TLS)

---

## 🧪 Verify Configuration

### **Quick Check:**
```bash
python manage.py test_email
```

Should show all ✅ checkmarks.

### **Send Test Email:**
```bash
python manage.py test_email --to your@email.com
```

Check inbox and spam folder!

---

## 🔍 Troubleshooting

### **Still no email?**

1. **Check Render Logs:**
   - Render Dashboard → Logs
   - Look for "OTP email sent successfully" or error messages

2. **Verify environment variables:**
   ```bash
   # In Render Shell:
   python manage.py shell
   ```
   ```python
   from django.conf import settings
   print(f"Host: {settings.EMAIL_HOST}")
   print(f"User: {settings.EMAIL_HOST_USER}")
   print(f"Pass set: {bool(settings.EMAIL_HOST_PASSWORD)}")
   ```

3. **Check spam folder!** (Most common issue)

### **"Authentication failed" error?**

- Double-check you're using **App Password**, not Gmail password
- Verify 2FA is enabled on Gmail account
- Try generating a new App Password

---

## 📖 Full Documentation

For detailed troubleshooting, SendGrid setup, and other email providers:
- Read: `EMAIL_OTP_FIX.md`

---

## ✅ Success Checklist

- [ ] Gmail App Password generated
- [ ] Environment variables added in Render
- [ ] Service redeployed (automatic)
- [ ] `test_email` command shows all ✅
- [ ] Test email received
- [ ] Password reset OTP received
- [ ] Can reset password successfully

---

**Time Required:** 5-10 minutes  
**Difficulty:** Easy  
**Status:** Ready to implement  

**That's it! Your email OTP should now work.** 🎉
