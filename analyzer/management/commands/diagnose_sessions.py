"""
Management command to diagnose session configuration issues
Run this to verify your session setup is correct
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db import connection


class Command(BaseCommand):
    help = 'Diagnose session configuration and potential issues'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Session Configuration Diagnosis'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # 1. Check Session Engine
        self.stdout.write(self.style.SUCCESS('\n📋 Session Configuration:'))
        self.stdout.write(f'   Engine: {settings.SESSION_ENGINE}')
        
        if settings.SESSION_ENGINE == 'django.contrib.sessions.backends.db':
            self.stdout.write(self.style.SUCCESS('   ✅ Using database-backed sessions (CORRECT)'))
        else:
            self.stdout.write(self.style.ERROR(
                '   ❌ Not using database sessions! This will cause issues on Render.'
            ))
        
        # 2. Session Cookie Settings
        self.stdout.write(f'\n🍪 Cookie Settings:')
        self.stdout.write(f'   Name: {settings.SESSION_COOKIE_NAME}')
        self.stdout.write(f'   Age: {settings.SESSION_COOKIE_AGE} seconds ({settings.SESSION_COOKIE_AGE / 3600:.1f} hours)')
        self.stdout.write(f'   Secure: {settings.SESSION_COOKIE_SECURE}')
        self.stdout.write(f'   HttpOnly: {settings.SESSION_COOKIE_HTTPONLY}')
        self.stdout.write(f'   SameSite: {settings.SESSION_COOKIE_SAMESITE}')
        self.stdout.write(f'   Expire at browser close: {settings.SESSION_EXPIRE_AT_BROWSER_CLOSE}')
        self.stdout.write(f'   Save every request: {settings.SESSION_SAVE_EVERY_REQUEST}')
        
        # 3. Check Database Connection
        self.stdout.write(f'\n🗄️  Database Connection:')
        try:
            db_conn = settings.DATABASES['default']
            self.stdout.write(f'   Engine: {db_conn.get("ENGINE", "Not specified")}')
            self.stdout.write(f'   Connection max age: {db_conn.get("CONN_MAX_AGE", 0)} seconds')
            
            # Test database connectivity
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS('   ✅ Database connection: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Database connection error: {e}'))
        
        # 4. Check Session Table
        self.stdout.write(f'\n📊 Session Table Status:')
        try:
            total_sessions = Session.objects.count()
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now()).count()
            expired_sessions = total_sessions - active_sessions
            
            self.stdout.write(f'   Total sessions: {total_sessions}')
            self.stdout.write(f'   Active sessions: {active_sessions}')
            self.stdout.write(f'   Expired sessions: {expired_sessions}')
            
            if total_sessions > 0:
                self.stdout.write(self.style.SUCCESS('   ✅ Session table exists and accessible'))
                
                # Show sample session data
                sample = Session.objects.first()
                if sample:
                    self.stdout.write(f'\n   Sample session:')
                    self.stdout.write(f'     Key: {sample.session_key[:20]}...')
                    self.stdout.write(f'     Expires: {sample.expire_date}')
                    self.stdout.write(f'     Is expired: {sample.expire_date < timezone.now()}')
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  No sessions in database yet'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error accessing session table: {e}'))
            self.stdout.write(self.style.WARNING('   💡 Run: python manage.py migrate'))
        
        # 5. Check SECRET_KEY
        self.stdout.write(f'\n🔐 Security Settings:')
        if settings.SECRET_KEY == 'django-insecure-dev-key-change-this':
            self.stdout.write(self.style.ERROR('   ❌ SECRET_KEY is using default value! Change this!'))
        else:
            self.stdout.write(self.style.SUCCESS('   ✅ SECRET_KEY is customized'))
        
        self.stdout.write(f'   DEBUG mode: {settings.DEBUG}')
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING('   ⚠️  DEBUG is True (should be False in production)'))
        else:
            self.stdout.write(self.style.SUCCESS('   ✅ DEBUG is False (correct for production)'))
        
        # 6. Recommendations
        self.stdout.write(self.style.SUCCESS('\n📝 Recommendations:'))
        
        issues_found = []
        
        if settings.SESSION_ENGINE != 'django.contrib.sessions.backends.db':
            issues_found.append('Change SESSION_ENGINE to django.contrib.sessions.backends.db')
        
        if settings.SESSION_COOKIE_AGE < 86400:  # Less than 24 hours
            issues_found.append(f'SESSION_COOKIE_AGE is only {settings.SESSION_COOKIE_AGE / 3600:.1f} hours, consider increasing')
        
        if not settings.SESSION_SAVE_EVERY_REQUEST:
            issues_found.append('Enable SESSION_SAVE_EVERY_REQUEST to extend sessions on activity')
        
        if settings.SESSION_EXPIRE_AT_BROWSER_CLOSE:
            issues_found.append('SESSION_EXPIRE_AT_BROWSER_CLOSE is True, sessions will not persist')
        
        if settings.DEBUG:
            issues_found.append('Disable DEBUG mode in production')
        
        if settings.SECRET_KEY == 'django-insecure-dev-key-change-this':
            issues_found.append('Set a proper SECRET_KEY in environment variables')
        
        if issues_found:
            for i, issue in enumerate(issues_found, 1):
                self.stdout.write(f'   {i}. {issue}')
        else:
            self.stdout.write(self.style.SUCCESS('   ✅ No issues found! Configuration looks good.'))
        
        # 7. Environment Check
        self.stdout.write(f'\n🌍 Environment:')
        import os
        render_host = os.getenv('RENDER_EXTERNAL_HOSTNAME')
        if render_host:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Running on Render: {render_host}'))
        else:
            self.stdout.write('   ℹ️  Not running on Render (local development)')
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ Diagnosis complete!\n'))
