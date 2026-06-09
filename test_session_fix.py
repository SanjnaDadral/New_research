#!/usr/bin/env python
"""
Quick test script to verify session configuration
Run this with: python test_session_fix.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_analyzer.settings')
django.setup()

from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import connection


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def check_session_config():
    """Verify session configuration"""
    print_section("1. SESSION CONFIGURATION CHECK")
    
    checks = {
        'Session Engine': settings.SESSION_ENGINE,
        'Cookie Age (days)': settings.SESSION_COOKIE_AGE / 86400,
        'Cookie Secure': settings.SESSION_COOKIE_SECURE,
        'Cookie HttpOnly': settings.SESSION_COOKIE_HTTPONLY,
        'Cookie SameSite': settings.SESSION_COOKIE_SAMESITE,
        'Save Every Request': settings.SESSION_SAVE_EVERY_REQUEST,
        'Expire at Browser Close': settings.SESSION_EXPIRE_AT_BROWSER_CLOSE,
    }
    
    for key, value in checks.items():
        print(f"  {key:.<40} {value}")
    
    # Validate
    issues = []
    if settings.SESSION_ENGINE != 'django.contrib.sessions.backends.db':
        issues.append("❌ SESSION_ENGINE must be 'django.contrib.sessions.backends.db'")
    else:
        print("\n  ✅ Session engine is correctly set to database")
    
    if not settings.SESSION_SAVE_EVERY_REQUEST:
        issues.append("⚠️  SESSION_SAVE_EVERY_REQUEST should be True")
    
    if settings.SESSION_EXPIRE_AT_BROWSER_CLOSE:
        issues.append("⚠️  SESSION_EXPIRE_AT_BROWSER_CLOSE should be False")
    
    return len(issues) == 0, issues


def check_database_connection():
    """Test database connectivity"""
    print_section("2. DATABASE CONNECTION CHECK")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("  ✅ Database connection: OK")
                return True
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False


def check_session_table():
    """Check if session table exists and is accessible"""
    print_section("3. SESSION TABLE CHECK")
    
    try:
        total = Session.objects.count()
        active = Session.objects.filter(expire_date__gte=timezone.now()).count()
        expired = total - active
        
        print(f"  Total sessions: {total}")
        print(f"  Active sessions: {active}")
        print(f"  Expired sessions: {expired}")
        
        if total > 0:
            print("\n  ✅ Session table exists and is accessible")
            
            # Show newest session
            newest = Session.objects.order_by('-expire_date').first()
            if newest:
                print(f"  Newest session expires: {newest.expire_date}")
        else:
            print("\n  ⚠️  No sessions in database yet (this is OK for fresh install)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Session table error: {e}")
        print("  💡 Run: python manage.py migrate")
        return False


def check_users():
    """Check user accounts"""
    print_section("4. USER ACCOUNTS CHECK")
    
    try:
        user_count = User.objects.count()
        print(f"  Total users: {user_count}")
        
        if user_count > 0:
            print("\n  Sample users:")
            for user in User.objects.all()[:5]:
                print(f"    - {user.username} ({user.email})")
        else:
            print("  ⚠️  No users yet")
        
        return True
        
    except Exception as e:
        print(f"  ❌ User check error: {e}")
        return False


def check_secret_key():
    """Verify SECRET_KEY is set"""
    print_section("5. SECRET KEY CHECK")
    
    if settings.SECRET_KEY == 'django-insecure-dev-key-change-this':
        print("  ❌ SECRET_KEY is using default value!")
        print("  💡 Set SECRET_KEY environment variable")
        return False
    else:
        print(f"  ✅ SECRET_KEY is customized ({len(settings.SECRET_KEY)} chars)")
        return True


def check_debug_mode():
    """Check DEBUG setting"""
    print_section("6. DEBUG MODE CHECK")
    
    if settings.DEBUG:
        print("  ⚠️  DEBUG = True (OK for development)")
        print("  💡 Set DEBUG=False for production")
    else:
        print("  ✅ DEBUG = False (correct for production)")
    
    return True


def check_environment():
    """Check deployment environment"""
    print_section("7. ENVIRONMENT CHECK")
    
    render_host = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_host:
        print(f"  ✅ Running on Render: {render_host}")
    else:
        print("  ℹ️  Running locally (not on Render)")
    
    # Check important env vars
    important_vars = ['DATABASE_URL', 'SECRET_KEY', 'DEBUG']
    print("\n  Environment variables:")
    for var in important_vars:
        value = os.getenv(var)
        if value:
            if var == 'SECRET_KEY':
                print(f"    {var}: {'*' * 20} (hidden)")
            elif var == 'DATABASE_URL':
                # Show only the protocol
                protocol = value.split('://')[0] if '://' in value else 'unknown'
                print(f"    {var}: {protocol}://... (hidden)")
            else:
                print(f"    {var}: {value}")
        else:
            print(f"    {var}: Not set")
    
    return True


def run_all_checks():
    """Run all diagnostic checks"""
    print("\n" + "=" * 60)
    print("  🔍 SESSION FIX VERIFICATION TEST")
    print("=" * 60)
    
    results = []
    
    # Run all checks
    results.append(("Session Config", check_session_config()))
    results.append(("Database Connection", check_database_connection()))
    results.append(("Session Table", check_session_table()))
    results.append(("User Accounts", check_users()))
    results.append(("Secret Key", check_secret_key()))
    results.append(("Debug Mode", check_debug_mode()))
    results.append(("Environment", check_environment()))
    
    # Summary
    print_section("SUMMARY")
    
    passed = 0
    total = 0
    
    for name, result in results:
        if isinstance(result, tuple):
            success, issues = result
            if success:
                print(f"  ✅ {name}: PASS")
                passed += 1
            else:
                print(f"  ❌ {name}: FAIL")
                for issue in issues:
                    print(f"     {issue}")
            total += 1
        elif result:
            print(f"  ✅ {name}: PASS")
            passed += 1
            total += 1
        else:
            print(f"  ❌ {name}: FAIL")
            total += 1
    
    print(f"\n  Score: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n  🎉 ALL CHECKS PASSED! Your session configuration is correct.")
        print("  ✅ You can now deploy to Render with confidence.")
    else:
        print(f"\n  ⚠️  {total - passed} checks failed. Review issues above.")
    
    print("\n" + "=" * 60 + "\n")
    
    return passed == total


if __name__ == '__main__':
    try:
        success = run_all_checks()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test script error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
