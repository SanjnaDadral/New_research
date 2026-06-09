"""
Management command to clean up expired sessions
Run this periodically (daily/weekly) to keep session table clean
"""
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db.models import Count


class Command(BaseCommand):
    help = 'Clean up expired sessions and show statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS('🧹 Session Cleanup Report'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        # Get current time
        now = timezone.now()
        
        # Count active sessions
        active_sessions = Session.objects.filter(expire_date__gte=now).count()
        self.stdout.write(f'✅ Active sessions: {active_sessions}')
        
        # Count expired sessions
        expired_sessions = Session.objects.filter(expire_date__lt=now)
        expired_count = expired_sessions.count()
        self.stdout.write(f'❌ Expired sessions: {expired_count}')
        
        # Total sessions
        total_sessions = Session.objects.count()
        self.stdout.write(f'📊 Total sessions: {total_sessions}')
        
        if expired_count > 0:
            if dry_run:
                self.stdout.write(self.style.WARNING(f'\n🔍 DRY RUN: Would delete {expired_count} expired sessions'))
            else:
                deleted_count, _ = expired_sessions.delete()
                self.stdout.write(self.style.SUCCESS(f'\n✅ Deleted {deleted_count} expired sessions'))
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ No expired sessions to clean up'))
        
        # Show remaining active sessions
        remaining_active = Session.objects.filter(expire_date__gte=now).count()
        self.stdout.write(f'\n📈 Remaining active sessions: {remaining_active}')
        
        # Calculate oldest and newest session
        oldest_session = Session.objects.filter(expire_date__gte=now).order_by('expire_date').first()
        newest_session = Session.objects.filter(expire_date__gte=now).order_by('-expire_date').first()
        
        if oldest_session:
            self.stdout.write(f'⏰ Oldest active session expires: {oldest_session.expire_date}')
        if newest_session:
            self.stdout.write(f'⏰ Newest active session expires: {newest_session.expire_date}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Cleanup complete!'))
        
        # Recommendations
        if remaining_active > 1000:
            self.stdout.write(self.style.WARNING(
                f'\n⚠️  Warning: {remaining_active} active sessions. '
                'Consider running cleanup more frequently.'
            ))
