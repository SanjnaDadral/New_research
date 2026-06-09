# 🔧 Render Session & Authentication Fix

## ❌ Problems Identified

Your Render deployment was experiencing session loss after ~1 hour due to:

1. **File-based sessions** (default) - Lost when containers restart
2. **No explicit session timeout configuration**
3. **Sessions not persisting across deployments**
4. **Container restarts clearing ephemeral storage**

---

## ✅ Solutions Implemented

### 1. **Database-Backed Sessions**
Changed from file-based to database-backed sessions in `settings.py`:

```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 14 days
SESSION_SAVE_EVERY_REQUEST = True  # Extend session on activity
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Persist after browser close
```

### 2. **Session Cookie Configuration**
```python
SESSION_COOKIE_SECURE = True  # HTTPS only in production
SESSION_COOKIE_HTTPONLY = True  # Prevent XSS attacks
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_COOKIE_NAME = 'paperyzer_sessionid'  # Unique name
```

### 3. **Database Connection Health Checks**
```python
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,  # Auto-reconnect if connection lost
    )
}
```

### 4. **Session Management Command**
Created `analyzer/management/commands/setup_sessions.py` to:
- Verify session table exists
- Clean up expired sessions
- Show active session count

---

## 🚀 Deployment Steps

### **On Render Dashboard:**

1. **Verify Environment Variables:**
   - `SECRET_KEY` - Must be set and consistent (don't change after deployment)
   - `DATABASE_URL` - Automatically set by Render (PostgreSQL)
   - `DEBUG` - Should be `False` in production

2. **Manual Deployment Steps:**
   ```bash
   # The build.sh script now automatically runs:
   python manage.py migrate
   python manage.py setup_sessions
   python manage.py collectstatic --no-input
   ```

3. **After Deployment:**
   - Go to your Render service → Shell tab
   - Run: `python manage.py setup_sessions`
   - Verify output shows session table exists

### **Testing the Fix:**

1. **Test Login Persistence:**
   ```bash
   # Login to your site
   # Wait 2 hours
   # Refresh page - should still be logged in
   ```

2. **Check Session in Database:**
   ```bash
   # In Render Shell:
   python manage.py shell
   ```
   ```python
   from django.contrib.sessions.models import Session
   from django.utils import timezone
   
   # Count active sessions
   active = Session.objects.filter(expire_date__gte=timezone.now()).count()
   print(f"Active sessions: {active}")
   
   # Check your session
   for s in Session.objects.all()[:5]:
       print(f"Session: {s.session_key[:10]}... expires: {s.expire_date}")
   ```

---

## 🔍 Debugging Session Issues

### **Check if session table exists:**
```bash
python manage.py dbshell
```
```sql
-- For PostgreSQL:
\dt django_session

-- Or:
SELECT * FROM django_session LIMIT 5;
```

### **Clear all sessions (if needed):**
```bash
python manage.py clearsessions
```

### **Check session in browser:**
1. Open Developer Tools (F12)
2. Go to Application/Storage → Cookies
3. Look for `paperyzer_sessionid`
4. Verify it has:
   - `Secure` flag (on HTTPS)
   - `HttpOnly` flag
   - `SameSite=Lax`

---

## 🛡️ Security Improvements

The fix also includes:

1. **HttpOnly cookies** - Prevents JavaScript access to session cookies
2. **Secure flag** - Only sends cookies over HTTPS
3. **SameSite=Lax** - Protects against CSRF attacks
4. **Connection health checks** - Auto-reconnects to database if connection drops

---

## 📝 Common Issues & Solutions

### **Issue: "User not found" after 1 hour**
**Cause:** Old file-based sessions were lost on container restart
**Fix:** ✅ Now using database sessions (persists across restarts)

### **Issue: "Login loop" - keeps redirecting to login**
**Possible Causes:**
1. Session cookie not being set (check browser DevTools)
2. `SECRET_KEY` changed between deployments (sessions invalidated)
3. Database connection issues

**Fix:**
```bash
# Check if SECRET_KEY is consistent:
echo $SECRET_KEY  # Should be same value always

# Verify session cookie settings:
python manage.py shell
from django.conf import settings
print(f"Session Engine: {settings.SESSION_ENGINE}")
print(f"Cookie Age: {settings.SESSION_COOKIE_AGE}")
print(f"Secure: {settings.SESSION_COOKIE_SECURE}")
```

### **Issue: Data shows for some users but not others**
**Cause:** User foreign key relationship working correctly, but sessions expiring
**Fix:** ✅ Extended session timeout to 14 days with activity refresh

---

## 🎯 Next Steps

1. **Deploy the changes** (git push to trigger Render deployment)
2. **Run migrations** (automatic in build.sh)
3. **Test login persistence** (wait 2+ hours)
4. **Clear old sessions periodically:**
   ```bash
   # Add to cron or run manually:
   python manage.py clearsessions
   ```

---

## 💡 Monitoring Sessions

Add this to your Django admin or create a monitoring endpoint:

```python
# In Django shell or admin:
from django.contrib.sessions.models import Session
from django.utils import timezone

# Active sessions count
active = Session.objects.filter(expire_date__gte=timezone.now()).count()
print(f"Active sessions: {active}")

# Expired sessions count
expired = Session.objects.filter(expire_date__lt=timezone.now()).count()
print(f"Expired sessions: {expired}")
```

---

## 🚨 Important Notes

1. **Don't change SECRET_KEY** after deployment - This will invalidate all existing sessions
2. **Run migrations** after every deployment to ensure session table is up to date
3. **Monitor session growth** - Run `clearsessions` periodically to remove expired sessions
4. **Test thoroughly** after deployment before announcing to users

---

## 📚 References

- [Django Sessions Documentation](https://docs.djangoproject.com/en/stable/topics/http/sessions/)
- [Render Persistent Storage](https://render.com/docs/disks)
- [Django Database-backed Sessions](https://docs.djangoproject.com/en/stable/topics/http/sessions/#using-database-backed-sessions)

---

**Last Updated:** 2026-06-09
**Status:** ✅ Fixed - Database sessions implemented
