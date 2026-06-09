# 🔧 Session & Login Issues - Complete Fix Guide

## 🎯 Problem Summary

You reported that on Render:
1. **After 1 hour, data doesn't show** - Sessions were expiring/lost
2. **Can't login with same ID used to create account** - Authentication not persisting

## 🔍 Root Causes Found

### 1. **File-Based Sessions (Main Issue)**
- Django's default session storage uses files
- Render containers have **ephemeral storage** - files are deleted on restart
- Your sessions were being lost every time the container restarted (roughly hourly)

### 2. **No Session Persistence Configuration**
- No explicit session timeout set
- Sessions not configured to survive browser close
- No session refresh on user activity

### 3. **Missing Database Session Table**
- `django_session` table might not have been created initially

---

## ✅ Fixes Implemented

### **File 1: `paper_analyzer/settings.py`**

Added comprehensive session configuration:

```python
# ======================
# SESSION CONFIGURATION (CRITICAL FOR RENDER)
# ======================
# Use database-backed sessions instead of file-based
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Session cookie settings
SESSION_COOKIE_SECURE = not DEBUG  # HTTPS only in production
CSRF_COOKIE_SECURE = not DEBUG

# Session timeout: 2 weeks
SESSION_COOKIE_AGE = 1209600  # 14 days in seconds
SESSION_SAVE_EVERY_REQUEST = True  # Refresh session on each request

# Cookie security settings
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_COOKIE_NAME = 'paperyzer_sessionid'

# Keep sessions after browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Database connection health checks
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,  # Auto-reconnect
    )
}
```

### **File 2: Management Commands**

Created 3 new management commands:

#### `setup_sessions.py` - Initial Setup
```bash
python manage.py setup_sessions
```
- Verifies session table exists
- Cleans up expired sessions
- Shows active session count

#### `cleanup_sessions.py` - Maintenance
```bash
python manage.py cleanup_sessions
python manage.py cleanup_sessions --dry-run  # Preview only
```
- Removes expired sessions
- Shows statistics
- Should be run weekly/monthly

#### `diagnose_sessions.py` - Debugging
```bash
python manage.py diagnose_sessions
```
- Checks all session settings
- Verifies database connection
- Identifies configuration issues
- Provides recommendations

### **File 3: Updated `build.sh`**

Added session setup to deployment:
```bash
echo "=== Step 4: Setting up sessions ==="
python manage.py setup_sessions
```

---

## 🚀 Deployment Steps (Follow These!)

### **Step 1: Commit and Push Changes**

```bash
git add .
git commit -m "Fix: Implement database sessions for Render persistence"
git push
```

### **Step 2: Wait for Render Deployment**

Monitor your Render dashboard - wait for deployment to complete

### **Step 3: Run Diagnostics (Via Render Shell)**

1. Go to your Render service dashboard
2. Click **Shell** tab
3. Run:

```bash
python manage.py diagnose_sessions
```

**Expected Output:**
```
✅ Using database-backed sessions (CORRECT)
✅ Database connection: OK
✅ Session table exists and accessible
✅ No issues found! Configuration looks good.
```

### **Step 4: Test Login**

1. **Clear browser cookies** (important!)
   - Chrome: DevTools (F12) → Application → Cookies → Delete all
   - Firefox: DevTools (F12) → Storage → Cookies → Delete all

2. **Login to your site**
3. **Check session cookie:**
   - Open DevTools (F12)
   - Go to Application/Storage → Cookies
   - Find `paperyzer_sessionid`
   - Verify it has:
     - ✅ `Secure` flag
     - ✅ `HttpOnly` flag
     - ✅ `SameSite=Lax`

4. **Test persistence:**
   - Stay logged in
   - Wait 2+ hours
   - Refresh the page
   - You should **still be logged in** ✅

---

## 🧪 Testing Checklist

- [ ] Deploy changes to Render
- [ ] Run `python manage.py diagnose_sessions` (no errors)
- [ ] Clear browser cookies
- [ ] Create new account / Login
- [ ] Verify `paperyzer_sessionid` cookie exists
- [ ] Upload a document
- [ ] See data in dashboard
- [ ] Close browser completely
- [ ] Reopen browser
- [ ] Go to site - **should still be logged in**
- [ ] Wait 2+ hours
- [ ] Refresh page - **should still be logged in**

---

## 🔧 Troubleshooting

### **Issue: Still getting logged out**

**Check 1: Is session table created?**
```bash
python manage.py shell
```
```python
from django.contrib.sessions.models import Session
print(Session.objects.count())  # Should be > 0 after login
```

**Check 2: Is SECRET_KEY consistent?**
```bash
# In Render Shell:
echo $SECRET_KEY
```
- **Important:** SECRET_KEY must be **the same** across all deployments
- If it changes, all sessions become invalid

**Check 3: Database connection**
```bash
python manage.py dbshell
```
```sql
SELECT COUNT(*) FROM django_session;
```

### **Issue: "Table doesn't exist" error**

**Solution:**
```bash
python manage.py migrate
python manage.py setup_sessions
```

### **Issue: Data shows but disappears after refresh**

**Cause:** Session is being created but not retrieved

**Debug:**
```bash
python manage.py shell
```
```python
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

# Check sessions
for s in Session.objects.all():
    data = s.get_decoded()
    print(f"Session: {s.session_key[:10]}...")
    print(f"User ID: {data.get('_auth_user_id')}")
    print(f"Expires: {s.expire_date}")
    print("---")

# Check users
print(f"\nTotal users: {User.objects.count()}")
for u in User.objects.all():
    print(f"Username: {u.username}, Email: {u.email}")
```

### **Issue: Can't login with email**

Your app uses `EmailOrUsernameModelBackend` which allows login with both username and email.

**Test:**
```bash
python manage.py shell
```
```python
from django.contrib.auth import authenticate

# Test with username
user = authenticate(username='your_username', password='your_password')
print(f"Auth with username: {user}")

# Test with email
user = authenticate(username='your@email.com', password='your_password')
print(f"Auth with email: {user}")
```

---

## 📊 Monitoring Sessions

### **Check Active Sessions**
```bash
python manage.py shell
```
```python
from django.contrib.sessions.models import Session
from django.utils import timezone

active = Session.objects.filter(expire_date__gte=timezone.now()).count()
expired = Session.objects.filter(expire_date__lt=timezone.now()).count()

print(f"Active sessions: {active}")
print(f"Expired sessions: {expired}")
```

### **Clean Up Old Sessions (Run Weekly)**
```bash
python manage.py cleanup_sessions
```

### **View All Sessions for Debugging**
```bash
python manage.py shell
```
```python
from django.contrib.sessions.models import Session

for session in Session.objects.all()[:10]:
    print(f"\nSession Key: {session.session_key[:15]}...")
    print(f"Expires: {session.expire_date}")
    print(f"Data: {session.get_decoded()}")
```

---

## 🎯 Key Configuration Values

| Setting | Old Value | New Value | Why |
|---------|-----------|-----------|-----|
| `SESSION_ENGINE` | (file-based) | `db` | Persist across restarts |
| `SESSION_COOKIE_AGE` | (default 2 weeks) | `1209600` (14 days) | Explicit timeout |
| `SESSION_SAVE_EVERY_REQUEST` | `False` | `True` | Refresh on activity |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | (varies) | `False` | Keep after browser close |
| `conn_health_checks` | Not set | `True` | Auto-reconnect to DB |

---

## 🚨 Critical Warnings

### **1. NEVER Change SECRET_KEY After Deployment**
- Changing it invalidates **all existing sessions**
- Users will be logged out
- Set it once and keep it consistent

### **2. Always Run Migrations After Deploy**
```bash
python manage.py migrate
```

### **3. Clean Sessions Periodically**
Too many sessions can slow down database:
```bash
python manage.py cleanup_sessions
```

---

## 📚 Additional Resources

- [Django Sessions Docs](https://docs.djangoproject.com/en/stable/topics/http/sessions/)
- [Render Persistent Storage](https://render.com/docs/disks)
- [Django Authentication](https://docs.djangoproject.com/en/stable/topics/auth/)

---

## 💡 Next Steps

1. **Deploy and test** following the steps above
2. **Monitor sessions** for first 24 hours
3. **Set up weekly cleanup** (add to scheduled job or run manually)
4. **Test from multiple devices/browsers**

---

## ✅ Success Criteria

After implementing these fixes, you should be able to:

- ✅ Login successfully
- ✅ See your data immediately after login
- ✅ Refresh page and still see data
- ✅ Close browser, reopen, and still be logged in
- ✅ Wait 2+ hours and still be logged in
- ✅ Login from multiple devices simultaneously
- ✅ Session survives Render container restarts

---

**Implementation Date:** 2026-06-09  
**Status:** ✅ Ready for Deployment  
**Priority:** 🔴 Critical - Deploy ASAP

---

## 🆘 Need Help?

If you still experience issues after deployment:

1. Run `python manage.py diagnose_sessions`
2. Check output for ❌ errors
3. Review the Troubleshooting section above
4. Check Render logs for errors
