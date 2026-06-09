"""
Management command to setup and verify session configuration for Render deployment
"""
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db import connection


class Command(BaseCommand):
    help = 'Setup and verify database sessions for production deployment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Setting up database sessions...'))
        
        # Check if session table exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='django_session'
            """)
            table_exists = cursor.fetchone()
        
        if table_exists:
            self.stdout.write(self.style.SUCCESS('✅ Session table exists'))
            
            # Clean up expired sessions
            expired_count = Session.objects.filter(expire_date__lt=timezone.now()).count()
            if expired_count > 0:
                Session.objects.filter(expire_date__lt=timezone.now()).delete()
                self.stdout.write(self.style.SUCCESS(f'🧹 Cleaned up {expired_count} expired sessions'))
            
            # Show current session count
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now()).count()
            self.stdout.write(self.style.SUCCESS(f'📊 Active sessions: {active_sessions}'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Session table does not exist. Run: python manage.py migrate'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Session setup complete!'))
        self.stdout.write(self.style.SUCCESS('📝 Remember to run this after each deployment:'))
        self.stdout.write('   python manage.py migrate')
        self.stdout.write('   python manage.py setup_sessions')
