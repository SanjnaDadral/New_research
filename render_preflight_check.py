#!/usr/bin/env python
"""
Render Deployment Pre-Flight Check
Validates that all required files and configurations are in place
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file_exists(filepath, name):
    """Check if a file exists"""
    path = BASE_DIR / filepath
    if path.exists():
        print(f"{GREEN}✓{RESET} {name}: {filepath}")
        return True
    else:
        print(f"{RED}✗{RESET} {name}: {filepath} NOT FOUND")
        return False

def check_file_contains(filepath, patterns, name):
    """Check if a file contains specific patterns"""
    path = BASE_DIR / filepath
    if not path.exists():
        print(f"{RED}✗{RESET} {name}: File not found")
        return False
    
    try:
        content = path.read_text()
        found_all = all(pattern in content for pattern in patterns)
        if found_all:
            print(f"{GREEN}✓{RESET} {name}: {filepath}")
            return True
        else:
            missing = [p for p in patterns if p not in content]
            print(f"{RED}✗{RESET} {name}: Missing patterns {missing}")
            return False
    except Exception as e:
        print(f"{RED}✗{RESET} {name}: Error reading file: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("RENDER DEPLOYMENT PRE-FLIGHT CHECK")
    print("="*60 + "\n")
    
    checks_passed = 0
    checks_total = 0
    
    # 1. Required Files
    print("📋 Required Files:")
    required_files = {
        'requirements.txt': 'Python Dependencies',
        'build.sh': 'Build Script',
        'render.yaml': 'Render Configuration',
        '.env': 'Environment Configuration',
        'manage.py': 'Django Manager',
        'paper_analyzer/settings.py': 'Django Settings',
    }
    
    for filepath, name in required_files.items():
        checks_total += 1
        if check_file_exists(filepath, name):
            checks_passed += 1
    
    # 2. File Content Checks
    print("\n🔍 Configuration Checks:")
    
    # Check requirements.txt has key dependencies
    checks_total += 1
    if check_file_contains('requirements.txt', ['Django', 'gunicorn', 'psycopg2', 'whitenoise'], 'requirements.txt content'):
        checks_passed += 1
    
    # Check render.yaml has database config
    checks_total += 1
    if check_file_contains('render.yaml', ['services:', 'databases:', 'paper-analyzer-db'], 'render.yaml database'):
        checks_passed += 1
    
    # Check build.sh has essential commands
    checks_total += 1
    if check_file_contains('build.sh', ['pip install', 'migrate', 'collectstatic'], 'build.sh commands'):
        checks_passed += 1
    
    # Check settings.py for production config
    checks_total += 1
    if check_file_contains('paper_analyzer/settings.py', ['DEBUG', 'ALLOWED_HOSTS', 'DATABASE_URL'], 'settings.py production'):
        checks_passed += 1
    
    # 3. Git Status
    print("\n📦 Git Status:")
    checks_total += 1
    try:
        status = os.popen('git status --porcelain').read()
        if status:
            print(f"{YELLOW}⚠{RESET}  Uncommitted changes detected:")
            print(status)
            print(f"{YELLOW}  → Run 'git add . && git commit -m \"Render deployment updates\"'{RESET}")
        else:
            print(f"{GREEN}✓{RESET}  All changes committed")
            checks_passed += 1
    except:
        print(f"{YELLOW}⚠{RESET}  Could not check git status")
    
    # Summary
    print("\n" + "="*60)
    print(f"SUMMARY: {checks_passed}/{checks_total} checks passed")
    print("="*60 + "\n")
    
    if checks_passed == checks_total:
        print(f"{GREEN}✅ All checks passed! Ready for Render deployment.{RESET}\n")
        print("Next steps:")
        print("1. Commit all changes: git add . && git commit -m 'Render deployment ready'")
        print("2. Push to GitHub: git push origin main")
        print("3. Go to render.com and create new Blueprint instance")
        print("4. Set environment variables in Render Dashboard:")
        print("   - SECRET_KEY (auto-generated)")
        print("   - GROQ_API_KEY")
        print("   - EMAIL_HOST_USER")
        print("   - EMAIL_HOST_PASSWORD")
        print("5. Click Deploy and monitor logs\n")
        return 0
    else:
        print(f"{RED}❌ Some checks failed. Please fix the issues above.{RESET}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
