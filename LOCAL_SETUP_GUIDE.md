# 🏠 Local Setup Guide - PaperAIzer

## Complete guide to run PaperAIzer on your local machine

---

## 📋 Prerequisites

Before starting, make sure you have:

- **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
- **Git** installed ([Download](https://git-scm.com/downloads))
- **Text Editor** (VS Code, PyCharm, or any editor)
- **Command Line** access (Terminal/PowerShell/CMD)

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Clone or Navigate to Project
```bash
# If you haven't cloned yet
git clone <your-repo-url>
cd paper_analyzer

# If already cloned
cd /path/to/paper_analyzer
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will take 2-3 minutes to install all packages.

### Step 4: Create Environment File
```bash
# Copy the example file
cp .env.example .env

# On Windows (if cp doesn't work):
copy .env.example .env
```

### Step 5: Edit .env File

Open `.env` in your text editor and set:

```env
# Django Settings
SECRET_KEY=your-local-secret-key-any-random-string
DEBUG=True

# REQUIRED: Groq API Key (for AI analysis)
GROQ_API_KEY=your-groq-api-key-here

# Email (Optional - for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Other settings (optional)
ALLOWED_HOSTS=localhost,127.0.0.1
```

**IMPORTANT**: You MUST set `GROQ_API_KEY` or the AI analysis won't work!

#### 🔑 How to Get GROQ API Key (FREE):
1. Go to https://console.groq.com/
2. Sign up/Login (free account)
3. Go to "API Keys" section
4. Click "Create API Key"
5. Copy the key and paste in `.env`

### Step 6: Run Migrations
```bash
# Create database tables
python manage.py migrate

# Setup sessions (important!)
python manage.py setup_sessions
```

### Step 7: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser

# Enter:
# - Username: admin (or your choice)
# - Email: admin@example.com
# - Password: (your choice, minimum 8 characters)
```

### Step 8: Download NLTK Data (One-Time Setup)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Step 9: Run the Server
```bash
python manage.py runserver
```

### Step 10: Open Your Browser
```
http://127.0.0.1:8000
```

🎉 **You're now running PaperAIzer locally!**

---

## 🔍 Checking for Issues

### Issue Check #1: GROQ API Key
```bash
python manage.py shell
```
Then type:
```python
from django.conf import settings
print(settings.GROQ_API_KEY)
# Should print your API key, not empty string
exit()
```

### Issue Check #2: Database Sessions
```bash
python manage.py diagnose_sessions
```
Should show:
```
✅ Session engine: database
✅ Session table exists: Yes
✅ Cookie age: 1209600 seconds (14 days)
```

### Issue Check #3: Static Files
```bash
python manage.py collectstatic --noinput
```

### Issue Check #4: Test Analysis (Optional)
1. Go to http://127.0.0.1:8000
2. Register a new account
3. Upload a sample PDF
4. Check if analysis works

---

## 📁 Project Structure

```
paper_analyzer/
├── analyzer/                  # Main app
│   ├── views.py              # All page logic
│   ├── models.py             # Database models
│   ├── forms.py              # Forms
│   ├── urls.py               # App URLs
│   ├── rag_utils.py          # AI analysis with Groq
│   ├── pdf_processor.py      # PDF handling
│   ├── management/commands/  # Management commands
│   └── templates/            # HTML templates
│
├── paper_analyzer/           # Project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py               # Root URLs
│   └── wsgi.py               # Server config
│
├── static/                   # Static files (CSS, JS, images)
├── templates/                # Global templates
├── media/                    # Uploaded files (created on first upload)
├── logs/                     # Application logs (created automatically)
├── db.sqlite3                # Local database (created by migrate)
├── .env                      # Your environment variables
├── .env.example              # Template for .env
├── requirements.txt          # Python dependencies
└── manage.py                 # Django management script
```

---

## 🛠️ Common Issues & Solutions

### Issue 1: "No module named 'analyzer'"
**Solution:**
```bash
# Make sure you're in the right directory
cd /path/to/paper_analyzer

# Check if manage.py exists
ls manage.py

# If not found, you're in wrong directory
```

### Issue 2: "GROQ_API_KEY not set"
**Solution:**
```bash
# Check .env file exists
ls .env

# Open .env and add:
GROQ_API_KEY=your-actual-key-here

# Restart the server
```

### Issue 3: "No such table: django_session"
**Solution:**
```bash
python manage.py migrate
python manage.py setup_sessions
```

### Issue 4: "Port 8000 already in use"
**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue 5: "ModuleNotFoundError: No module named 'groq'"
**Solution:**
```bash
pip install groq
# Or reinstall all requirements
pip install -r requirements.txt
```

### Issue 6: Static Files Not Loading (CSS/JS missing)
**Solution:**
```bash
python manage.py collectstatic --noinput
# Then restart server
```

### Issue 7: Database Locked
**Solution:**
```bash
# Stop the server (Ctrl+C)
# Delete database (WARNING: loses all data)
rm db.sqlite3
# Recreate
python manage.py migrate
python manage.py createsuperuser
```

---

## 🧪 Testing Locally

### Test 1: Home Page
```
http://127.0.0.1:8000/
```
✅ Should show homepage with upload option

### Test 2: Register Account
```
http://127.0.0.1:8000/register/
```
✅ Create account and login

### Test 3: Upload PDF
1. Download a sample research PDF
2. Go to upload page
3. Select PDF
4. Click "Analyze Paper"
5. ✅ Should process and show results

### Test 4: Bulk Upload
1. Select 2-3 small PDFs (hold Ctrl/Cmd + Click)
2. Upload
3. ✅ Should process all and show bulk results

### Test 5: Library
```
http://127.0.0.1:8000/library/
```
✅ Should show all analyzed papers

### Test 6: Admin Panel
```
http://127.0.0.1:8000/admin/
```
Login with superuser account
✅ Should access Django admin

---

## 🔧 Useful Management Commands

### Database
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Check for migration issues
python manage.py makemigrations
```

### Sessions
```bash
# Setup/verify sessions
python manage.py setup_sessions

# Diagnose session issues
python manage.py diagnose_sessions

# Cleanup old sessions
python manage.py cleanup_sessions
```

### Testing
```bash
# Test email (if configured)
python manage.py test_email your-email@example.com

# Check bulk upload
python manage.py check_bulk_upload

# Run Django shell
python manage.py shell
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput

# Clear static files
rm -rf staticfiles/
python manage.py collectstatic --noinput
```

---

## 📊 Monitoring & Debugging

### View Logs
```bash
# Application logs
cat logs/app.log

# Or on Windows:
type logs\app.log

# Watch logs in real-time (Mac/Linux)
tail -f logs/app.log

# Watch logs (Windows - PowerShell)
Get-Content logs\app.log -Wait
```

### Django Debug Toolbar (Optional)
Add to `requirements.txt`:
```
django-debug-toolbar==4.2.0
```

Install and configure for detailed debugging.

### Check Database
```bash
python manage.py dbshell

# Then run SQL:
SELECT COUNT(*) FROM django_session;
SELECT COUNT(*) FROM analyzer_document;
.exit
```

---

## 🌐 Access Points

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Homepage |
| http://127.0.0.1:8000/register/ | Register |
| http://127.0.0.1:8000/login/ | Login |
| http://127.0.0.1:8000/dashboard/ | Dashboard |
| http://127.0.0.1:8000/library/ | Library |
| http://127.0.0.1:8000/upload/ | Upload |
| http://127.0.0.1:8000/admin/ | Admin Panel |

---

## 🔄 Daily Development Workflow

### Starting Work
```bash
# 1. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 2. Pull latest changes (if working with team)
git pull origin main

# 3. Run migrations (if any new)
python manage.py migrate

# 4. Start server
python manage.py runserver
```

### Stopping Work
```bash
# 1. Stop server (Ctrl+C)

# 2. Deactivate virtual environment
deactivate
```

---

## 🎨 Making Changes

### Change Templates (HTML)
1. Edit files in `templates/analyzer/`
2. Save
3. Refresh browser (no server restart needed)

### Change Static Files (CSS/JS)
1. Edit files in `static/`
2. Save
3. Hard refresh browser (Ctrl+Shift+R)
4. If still not working:
   ```bash
   python manage.py collectstatic --noinput
   ```

### Change Python Code (Views/Models)
1. Edit Python files
2. Save
3. Restart server (Ctrl+C, then `python manage.py runserver`)

### Add New Dependencies
1. Add to `requirements.txt`
2. Run:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚨 Known Limitations (Local Environment)

### 1. Email Features
- Password reset OTP won't work without SMTP configuration
- Need to add EMAIL_* variables to .env
- Alternatively, reset passwords via admin panel

### 2. Large Files
- SQLite has size limits (~2GB database)
- For production use PostgreSQL (already configured for Render)

### 3. Performance
- Local server is single-threaded
- Large PDF processing is slower than production
- Don't worry, it's normal for development

### 4. Media Files
- Uploaded files stored in `media/` folder
- This folder can get large
- Periodically clean it:
  ```bash
  rm -rf media/uploads/*
  ```

---

## 🔒 Security Notes

### For Local Development
- ✅ DEBUG=True is OK locally
- ✅ SECRET_KEY can be simple
- ✅ SQLite is fine
- ⚠️ Don't commit `.env` to git
- ⚠️ Don't share your GROQ API key

### For Production (Render)
- ❌ DEBUG=False required
- ❌ Strong SECRET_KEY required
- ❌ PostgreSQL recommended
- ✅ Environment variables in Render dashboard
- ✅ HTTPS enforced

---

## 📦 Environment Variables Reference

### Required
```env
GROQ_API_KEY=your-key-here  # MUST HAVE for AI analysis
DEBUG=True                   # True for local, False for production
SECRET_KEY=any-random-string # Can be simple for local
```

### Optional (Email)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Optional (Advanced)
```env
PDF_MAX_PAGES=25
ANALYSIS_TEXT_MAX=50000
ENABLE_HEAVY_ML=False
MAX_PDF_UPLOAD_MB=45
```

---

## 🎓 Learning Resources

### Django Documentation
- https://docs.djangoproject.com/
- https://docs.djangoproject.com/en/4.2/intro/tutorial01/

### Python Virtual Environments
- https://docs.python.org/3/tutorial/venv.html

### Groq API
- https://console.groq.com/docs

---

## ✅ Final Checklist

Before starting development, verify:

- [ ] Python 3.10+ installed (`python --version`)
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file created with GROQ_API_KEY
- [ ] Database migrated (`python manage.py migrate`)
- [ ] Superuser created
- [ ] NLTK data downloaded
- [ ] Server runs without errors
- [ ] Can access http://127.0.0.1:8000
- [ ] Can register and login
- [ ] Can upload and analyze a PDF

---

## 🆘 Getting Help

### Check Logs First
```bash
# Application logs
cat logs/app.log

# Server output (console)
# Read the error messages in terminal
```

### Common Error Patterns

**"ModuleNotFoundError"**
→ Missing dependency, run: `pip install -r requirements.txt`

**"No such table"**
→ Run migrations: `python manage.py migrate`

**"GROQ_API_KEY not set"**
→ Add to `.env` file and restart server

**"Port already in use"**
→ Kill process or use different port

**"Static files not loading"**
→ Run: `python manage.py collectstatic --noinput`

---

## 🎉 You're Ready!

Your local development environment is now set up and running!

**Quick Start Command:**
```bash
# Just run this every time you start working:
venv\Scripts\activate && python manage.py runserver
```

**Happy coding!** 🚀

---

**Last Updated**: June 9, 2026  
**Status**: Complete Local Setup Guide  
**Python**: 3.10+  
**Django**: 4.2+
