# 📚 Bulk Upload Feature - Complete Guide

## ✅ **Good News: Bulk Upload is Already Implemented!**

The bulk upload feature **IS working** and available in your application. If users are reporting they can't see it, here's how to troubleshoot and guide them.

---

## 🎯 How to Access Bulk Upload

### **Option 1: From Upload Page**

1. **Go to Upload page** (`/upload/`)
2. **Look for 3 tabs at the top:**
   - 📄 **PDF Upload** (single file)
   - 🌐 **URL / Link**
   - 📚 **Bulk Upload** (multiple files) ← Click this!

3. **Click "Bulk Upload" tab**
4. **Drag & drop multiple files** or click to browse
5. **Select 2-5 files** (PDF, DOCX, or DOC)
6. **Click "Analyze Paper"**

### **Visual Location:**

```
┌─────────────────────────────────────────┐
│  [PDF Upload] [URL/Link] [Bulk Upload]  │ ← Three tabs here
├─────────────────────────────────────────┤
│                                         │
│  Drop multiple files here...            │
│  Max 5 files, 45MB each                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔍 Why Users Might Not See It

### **1. Browser Cache Issue** (Most Common)

**Problem:** Old cached version of the page  
**Solution:**
```
Hard refresh the page:
- Windows/Linux: Ctrl + Shift + R
- Mac: Cmd + Shift + R
```

### **2. JavaScript Not Loading**

**Check:**
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for errors in red

**Fix:**
- Refresh page
- Clear browser cache
- Try different browser

### **3. Small Screen/Mobile**

**Problem:** Tabs might be stacked vertically on mobile  
**Solution:** Scroll down to see all 3 tabs

### **4. CSS Not Loading**

**Check:** If page looks broken or unstyled  
**Fix:**
```bash
# Run collectstatic on server
python manage.py collectstatic --no-input
```

---

## 📋 Bulk Upload Specifications

### **File Limits:**
- **Maximum files:** 5 papers per upload
- **File size:** 45 MB per file
- **Total size:** 225 MB maximum (5 × 45 MB)
- **Formats:** PDF, DOCX, DOC

### **Processing:**
- Each file analyzed separately
- Creates individual document for each file
- All results shown on bulk results page
- Can view/export each result individually

### **What Gets Analyzed:**
For each file:
- ✅ Summary & Abstract
- ✅ Keywords
- ✅ Methodology
- ✅ Technologies
- ✅ Plagiarism check
- ✅ References & citations
- ✅ Authors & publication year

---

## 🧪 Test Bulk Upload Feature

### **Quick Test:**

1. **Create test PDFs:**
   - Use any 2-3 research papers you have
   - Or download from arXiv.org

2. **Go to:** `your-site.com/upload/`

3. **Click:** "Bulk Upload" tab (third tab)

4. **Upload:** Select 2-3 PDF files

5. **Verify:**
   - Files should show in list
   - Total count and size displayed
   - "Analyze Paper" button enabled

6. **Click:** "Analyze Paper"

7. **Wait:** Processing takes 2-5 minutes for multiple files

8. **Result:** Redirects to bulk results page showing all analyses

---

## 🎨 UI Elements to Look For

### **Bulk Upload Tab:**
```html
┌──────────────────────────────────┐
│  🗂️ Bulk Upload                  │ ← Button with layer icon
└──────────────────────────────────┘
```

### **Drop Zone:**
```html
┌─────────────────────────────────────┐
│       ☁️                           │
│   Drag & drop multiple files here   │
│ or click to browse — PDF, DOCX, DOC │
│     max 5 files, 45 MB each         │
└─────────────────────────────────────┘
```

### **After Selection:**
```html
┌─────────────────────────────────────┐
│ ✅ 3 documents ready for analysis   │
│    (127.45 MB total)                │
│                                     │
│  📄 paper1.pdf                      │
│  📄 paper2.pdf                      │
│  📄 paper3.pdf                      │
│                                     │
│  [Remove All]                       │
└─────────────────────────────────────┘
```

---

## 🐛 Troubleshooting Checklist

Run through this checklist if bulk upload isn't showing:

- [ ] **Hard refresh browser** (Ctrl+Shift+R / Cmd+Shift+R)
- [ ] **Check if 3 tabs visible** at top of upload form
- [ ] **Open DevTools Console** (F12) - any errors?
- [ ] **Try different browser** (Chrome, Firefox, Edge)
- [ ] **Check on desktop** (not mobile) first
- [ ] **Clear browser cache completely**
- [ ] **Disable browser extensions** temporarily
- [ ] **Check internet connection** (slow load?)
- [ ] **Verify static files served** (CSS/JS loading?)

---

## 🔧 For Developers: Verify Implementation

### **Check Frontend:**

```bash
# Files that implement bulk upload:
templates/analyzer/upload.html  # Line 358: Bulk Upload tab
                                # Line 401: Bulk panel
                                # Line 525: JavaScript handler

static/js/app.js               # Line 239: Bulk file handling

static/js/analysis_handler.js  # Line 194: Bulk FormData
```

### **Check Backend:**

```bash
# Backend implementation:
analyzer/views.py              # Line 431: Bulk upload handler
                               # Processes 'bulk_files' from request
```

### **Test Backend Directly:**

```bash
# In Django shell:
python manage.py shell
```

```python
from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.first()
client.force_login(user)

# Try bulk upload endpoint
response = client.post('/analyze/', {
    'input_type': 'bulk',
    # Add files in actual test
})

print(response.status_code)
print(response.json())
```

---

## 📊 Usage Statistics

### **What's Processed:**

```python
# Backend logic (analyzer/views.py line 431+):
1. Receives bulk_files from request.FILES
2. Validates: max 5 files, each < 45MB
3. Loops through each file:
   - Extracts text (PDF/Word)
   - Runs AI analysis
   - Checks plagiarism
   - Saves to database
4. Returns list of document IDs
5. Redirects to bulk results page
```

### **Performance:**

| Files | Avg Processing Time |
|-------|---------------------|
| 1 file | 30-60 seconds |
| 2 files | 1-2 minutes |
| 3 files | 2-3 minutes |
| 5 files | 4-6 minutes |

---

## 🎯 User Guide (Share This!)

### **How to Upload Multiple Papers:**

1. **Navigate to Upload Page**
   - Click "Upload" or "Analyze" in main menu
   - Or go directly to `/upload/`

2. **Select Bulk Upload Mode**
   - You'll see 3 tabs at top
   - Click the third tab: "🗂️ Bulk Upload"

3. **Add Your Files**
   - Click the upload zone OR
   - Drag & drop multiple files
   - Select 2-5 PDF or Word files

4. **Verify Selection**
   - Check all files listed
   - Verify total size shown
   - Click "Analyze Paper" button

5. **Wait for Processing**
   - Progress animation shown
   - Takes 2-5 minutes for multiple files
   - Don't close browser

6. **View Results**
   - Automatically redirects when done
   - Shows all analyses in grid
   - Click any paper to see details

---

## 🚨 Common User Errors

### **Error: "Maximum 5 files allowed"**
**Cause:** Selected more than 5 files  
**Fix:** Select only 2-5 files at a time

### **Error: "File too large"**
**Cause:** One file exceeds 45 MB  
**Fix:** Compress PDF or split large file

### **Error: "No files uploaded"**
**Cause:** Clicked submit before selecting files  
**Fix:** Select files first, then submit

### **Error: "Only PDF and Word files allowed"**
**Cause:** Selected unsupported format  
**Fix:** Convert to PDF, DOCX, or DOC

---

## 💡 Tips for Best Results

### **Optimize Your PDFs:**
- ✅ Use text-based PDFs (not scanned images)
- ✅ Keep files under 20 MB each when possible
- ✅ Ensure PDFs are not password-protected
- ✅ Use clear, readable text

### **Processing Tips:**
- ✅ Start with 2-3 files for first test
- ✅ Don't close browser during processing
- ✅ Use strong internet connection
- ✅ Analyze related papers together

### **Organization:**
- ✅ Upload papers from same topic together
- ✅ Use tags/notes to organize results
- ✅ Export results before bulk upload again

---

## 📸 Screenshots Needed?

If users need visual guide, consider adding screenshots showing:

1. **Upload page with 3 tabs visible**
2. **Bulk Upload tab highlighted**
3. **Drop zone for multiple files**
4. **File list after selection**
5. **Bulk results page**

---

## ✅ Feature Confirmation

**The bulk upload feature includes:**

✅ **Tab-based interface** (PDF / URL / Bulk)  
✅ **Multi-file selection** (up to 5 files)  
✅ **Drag & drop support**  
✅ **File validation** (type, size)  
✅ **Progress animation**  
✅ **Individual analysis** per file  
✅ **Bulk results page**  
✅ **Export capabilities**  

---

## 🆘 Still Not Visible?

If bulk upload tab is still not showing after trying all above:

1. **Check server logs** for JavaScript errors:
   ```bash
   # In Render Dashboard → Logs
   # Look for: 404 errors on .js or .css files
   ```

2. **Verify static files:**
   ```bash
   # In Render Shell:
   ls -la staticfiles/js/
   ls -la staticfiles/css/
   ```

3. **Re-collect static files:**
   ```bash
   python manage.py collectstatic --no-input --clear
   ```

4. **Check Render environment:**
   - Ensure `STATIC_ROOT` is set
   - Verify `STATICFILES_STORAGE` configured
   - Check `STATIC_URL` is correct

---

## 📝 Summary

✅ **Bulk upload IS implemented**  
✅ **Available on /upload/ page**  
✅ **Third tab in upload interface**  
✅ **Supports 2-5 files**  
✅ **Works with PDF, DOCX, DOC**  

**Most common issue:** Browser cache - tell users to hard refresh!

---

**Last Updated:** 2026-06-09  
**Status:** ✅ Feature Fully Implemented  
**Location:** `/upload/` page, third tab  
**Backend:** `analyzer/views.py` line 431  
**Frontend:** `templates/analyzer/upload.html` line 358  
