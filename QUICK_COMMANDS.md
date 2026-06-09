v# ⚡ Quick Commands Reference - PaperAIzer

## 🏠 Local Development

### First Time Setup (5 minutes)
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env           # Mac/Linux
copy .env.example .env         # Windows

# 5. Edit .env and add:
# GROQ_API_KEY=your-key-here

# 6. Setup database
python manage.py migrate
python manage.py setup_sessions

# 7. Create admin user
python manage.py createsuperuser

# 8. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# 9. Run server
python manage.py runserver

# 10. Open browser
# http://127.0.0.1:8000
```

---

### Daily Development
```bash
# Start working
venv\Scripts\activate              # Windows
source venv/bin/activate           # Mac/Linux
python manage.py runserver

# Stop working
Ctrl+C                             # Stop server
deactivate                         # Deactivate venv
```

---

## 🚀 Deployment (Render)

### Deploy to Render
```bash
git add .
git commit -m "Your message"
git push origin main
# Render deploys automatically!
```

---

## 🔧 Management Commands

### Database
```bash
python manage.py migrate                    # Run migrations
python manage.py makemigrations             # Create new migrations
python manage.py createsuperuser            # Create admin user
python manage.py dbshell                    # Open database shell
```

### Sessions
```bash
python manage.py setup_sessions             # Setup session table
python manage.py diagnose_sessions          # Check session config
python manage.py cleanup_sessions           # Clean old sessions
```

### Testing
```bash
python manage.py test_email test@example.com    # Test email
python manage.py check_bulk_upload              # Check bulk upload
python manage.py shell                          # Django shell
```

### Static Files
```bash
python manage.py collectstatic --noinput    # Collect static files
```

---

## 🔍 Checking Issues

### Check GROQ API Key
```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.GROQ_API_KEY)
>>> exit()
```

### Check Sessions
```bash
python manage.py diagnose_sessions
```

### Check Logs
```bash
cat logs/app.log              # Mac/Linux
type logs\app.log             # Windows
tail -f logs/app.log          # Watch (Mac/Linux)
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001

# Or kill process (Windows)
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Or kill process (Mac/Linux)
lsof -ti:8000 | xargs kill -9
```

### Database Issues
```bash
# Reset database (WARNING: loses data)
rm db.sqlite3                              # Mac/Linux
del db.sqlite3                             # Windows
python manage.py migrate
python manage.py createsuperuser
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
# Then restart server
```

---

## 📦 Virtual Environment

### Create
```bash
python -m venv venv
```

### Activate
```bash
venv\Scripts\activate          # Windows CMD
venv\Scripts\Activate.ps1      # Windows PowerShell
source venv/bin/activate       # Mac/Linux
```

### Deactivate
```bash
deactivate
```

### Delete (if needed)
```bash
deactivate
rm -rf venv                    # Mac/Linux
rmdir /s venv                  # Windows
```

---

## 🔑 Get GROQ API Key

```
1. Go to: https://console.groq.com/
2. Sign up (free)
3. API Keys → Create API Key
4. Copy key
5. Add to .env: GROQ_API_KEY=your-key-here
```

---

## 🌐 URLs

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | Homepage |
| http://127.0.0.1:8000/register/ | Register |
| http://127.0.0.1:8000/login/ | Login |
| http://127.0.0.1:8000/dashboard/ | Dashboard |
| http://127.0.0.1:8000/library/ | Library |
| http://127.0.0.1:8000/upload/ | Upload |
| http://127.0.0.1:8000/admin/ | Admin Panel |

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables (YOUR SECRETS) |
| `db.sqlite3` | Local database |
| `requirements.txt` | Python dependencies |
| `manage.py` | Django commands |
| `logs/app.log` | Application logs |

---

## 🎯 Common Tasks

### Test Analysis Works
```bash
# 1. Start server
python manage.py runserver

# 2. Open http://127.0.0.1:8000
# 3. Register account
# 4. Upload a PDF
# 5. Check if analysis shows
```

### Update Dependencies
```bash
pip install --upgrade package-name
pip freeze > requirements.txt
```

### Check Django Version
```bash
python -c "import django; print(django.get_version())"
```

### Check Python Version
```bash
python --version
```

---

## 🔒 Environment Variables

### Required
```env
GROQ_API_KEY=your-key-here
DEBUG=True
SECRET_KEY=any-random-string
```

### Optional (Email)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 📚 Documentation Quick Links

| Need | Read This |
|------|-----------|
| **Local Setup** | [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md) |
| **Deploy Fast** | [QUICK_DEPLOY_GUIDE.md](QUICK_DEPLOY_GUIDE.md) |
| **All Fixes** | [ALL_FIXES_SUMMARY.md](ALL_FIXES_SUMMARY.md) |
| **Check Issues** | [ISSUES_CHECK_REPORT.md](ISSUES_CHECK_REPORT.md) |
| **Sessions** | [SESSION_FIX_INSTRUCTIONS.md](SESSION_FIX_INSTRUCTIONS.md) |
| **Email** | [EMAIL_QUICK_FIX.md](EMAIL_QUICK_FIX.md) |
| **Everything** | [README_FIXES.md](README_FIXES.md) |

---

## ⚡ Super Quick Setup (One Command)

### Windows PowerShell
```powershell
python -m venv venv; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt; cp .env.example .env; python manage.py migrate; python manage.py setup_sessions; python -c "import nltk; nltk.download('punkt')"; python manage.py runserver
```

### Mac/Linux
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && python manage.py migrate && python manage.py setup_sessions && python -c "import nltk; nltk.download('punkt')" && python manage.py runserver
```

**Then**: Edit `.env` to add GROQ_API_KEY and restart server!

---

## 🎉 That's It!

**Start developing**:
```bash
venv\Scripts\activate && python manage.py runserver
```

**Deploy**:
```bash
git push origin main
```

**Need help?** Check [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md)

---

**Last Updated**: June 9, 2026  
**Quick Reference**: Keep this handy!
