"""
Management command to test email configuration
Run this to verify your email setup is working
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import sys


class Command(BaseCommand):
    help = 'Test email configuration and send a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📧 Email Configuration Test'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # 1. Check email settings
        self.stdout.write(self.style.SUCCESS('\n1. EMAIL CONFIGURATION:'))
        
        email_backend = settings.EMAIL_BACKEND
        email_host = getattr(settings, 'EMAIL_HOST', 'Not set')
        email_port = getattr(settings, 'EMAIL_PORT', 'Not set')
        email_use_tls = getattr(settings, 'EMAIL_USE_TLS', False)
        email_use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
        email_host_user = getattr(settings, 'EMAIL_HOST_USER', '')
        email_host_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        email_timeout = getattr(settings, 'EMAIL_TIMEOUT', 10)
        
        self.stdout.write(f'   Backend: {email_backend}')
        self.stdout.write(f'   Host: {email_host}')
        self.stdout.write(f'   Port: {email_port}')
        self.stdout.write(f'   TLS: {email_use_tls}')
        self.stdout.write(f'   SSL: {email_use_ssl}')
        self.stdout.write(f'   Timeout: {email_timeout}s')
        
        # Check if credentials are set
        if email_host_user:
            self.stdout.write(f'   User: {email_host_user}')
        else:
            self.stdout.write(self.style.ERROR('   User: ❌ NOT SET'))
        
        if email_host_password:
            self.stdout.write(f'   Password: {"*" * 20} (set)')
        else:
            self.stdout.write(self.style.ERROR('   Password: ❌ NOT SET'))
        
        if default_from_email:
            self.stdout.write(f'   From Email: {default_from_email}')
        else:
            self.stdout.write(self.style.WARNING('   From Email: Not set (will use EMAIL_HOST_USER)'))
        
        # 2. Validate configuration
        self.stdout.write(self.style.SUCCESS('\n2. VALIDATION:'))
        
        issues = []
        
        if email_backend == 'django.core.mail.backends.console.EmailBackend':
            self.stdout.write(self.style.WARNING('   ⚠️  Using console backend (emails printed to console)'))
        elif email_backend == 'django.core.mail.backends.dummy.DummyEmailBackend':
            self.stdout.write(self.style.ERROR('   ❌ Using dummy backend (emails discarded)'))
            issues.append('Change EMAIL_BACKEND to django.core.mail.backends.smtp.EmailBackend')
        elif email_backend != 'django.core.mail.backends.smtp.EmailBackend':
            self.stdout.write(self.style.WARNING(f'   ⚠️  Using custom backend: {email_backend}'))
        else:
            self.stdout.write(self.style.SUCCESS('   ✅ Using SMTP backend (correct)'))
        
        if not email_host or email_host == 'localhost':
            issues.append('Set EMAIL_HOST to your SMTP server (e.g., smtp.gmail.com)')
            self.stdout.write(self.style.ERROR('   ❌ EMAIL_HOST not configured'))
        else:
            self.stdout.write(self.style.SUCCESS(f'   ✅ EMAIL_HOST configured: {email_host}'))
        
        if not email_host_user:
            issues.append('Set EMAIL_HOST_USER environment variable')
            self.stdout.write(self.style.ERROR('   ❌ EMAIL_HOST_USER not set'))
        else:
            self.stdout.write(self.style.SUCCESS(f'   ✅ EMAIL_HOST_USER configured'))
        
        if not email_host_password:
            issues.append('Set EMAIL_HOST_PASSWORD environment variable')
            self.stdout.write(self.style.ERROR('   ❌ EMAIL_HOST_PASSWORD not set'))
        else:
            self.stdout.write(self.style.SUCCESS('   ✅ EMAIL_HOST_PASSWORD configured'))
        
        # Check Gmail-specific settings
        if 'gmail' in email_host.lower():
            self.stdout.write(self.style.SUCCESS('\n   📝 Gmail Detected:'))
            if email_port != 587:
                self.stdout.write(self.style.WARNING(f'      ⚠️  Port is {email_port}, Gmail typically uses 587'))
            if not email_use_tls:
                self.stdout.write(self.style.ERROR('      ❌ TLS should be enabled for Gmail'))
                issues.append('Set EMAIL_USE_TLS=True for Gmail')
            else:
                self.stdout.write(self.style.SUCCESS('      ✅ TLS enabled'))
            
            self.stdout.write(self.style.WARNING('      💡 Remember to use App Password, not regular Gmail password!'))
            self.stdout.write('      Generate at: https://myaccount.google.com/apppasswords')
        
        # 3. Test email sending
        if issues:
            self.stdout.write(self.style.ERROR(f'\n❌ {len(issues)} configuration issue(s) found:'))
            for i, issue in enumerate(issues, 1):
                self.stdout.write(f'   {i}. {issue}')
            self.stdout.write(self.style.WARNING('\n⚠️  Fix issues above before sending test email'))
            sys.exit(1)
        
        # Send test email if recipient provided
        recipient = options.get('to')
        if recipient:
            self.stdout.write(self.style.SUCCESS('\n3. SENDING TEST EMAIL:'))
            self.stdout.write(f'   To: {recipient}')
            
            try:
                send_mail(
                    subject='PaperAIzer - Email Configuration Test',
                    message=f'''Hello,

This is a test email from your PaperAIzer application.

If you're reading this, your email configuration is working correctly!

Configuration:
- Host: {email_host}
- Port: {email_port}
- TLS: {email_use_tls}
- Time: {timezone.now()}

Best regards,
PaperAIzer Team''',
                    from_email=default_from_email or email_host_user,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS('\n   ✅ TEST EMAIL SENT SUCCESSFULLY!'))
                self.stdout.write(f'   Check inbox for: {recipient}')
                self.stdout.write('   (Also check spam folder)')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'\n   ❌ FAILED TO SEND EMAIL: {str(e)}'))
                self.stdout.write(self.style.WARNING('\n   Common causes:'))
                self.stdout.write('   1. Wrong email/password credentials')
                self.stdout.write('   2. Using Gmail password instead of App Password')
                self.stdout.write('   3. Less secure apps disabled (for Gmail)')
                self.stdout.write('   4. Firewall blocking SMTP port')
                self.stdout.write('   5. Wrong SMTP host or port')
                sys.exit(1)
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ Configuration looks good!'))
            self.stdout.write(self.style.WARNING('\n💡 To send a test email, run:'))
            self.stdout.write('   python manage.py test_email --to your@email.com')
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ Email test complete!\n'))
