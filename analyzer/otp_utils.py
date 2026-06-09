"""
OTP utilities for password reset functionality
"""

import random
import string
import logging
from datetime import timedelta

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import PasswordResetOTP

logger = logging.getLogger(__name__)


def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    return ''.join(random.choices(string.digits, k=length))


def get_from_email():
    """Return a FROM address that matches the authenticated SMTP account."""
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', '') or ''
    host_user = getattr(settings, 'EMAIL_HOST_USER', '') or ''
    if not from_email or 'noreply' in from_email.lower():
        return f'PaperAIzer <{host_user}>' if host_user else from_email
    return from_email


def _is_email_configured():
    """Check if real SMTP email credentials are configured"""
    host_user = getattr(settings, 'EMAIL_HOST_USER', '')
    host_pass = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    return bool(host_user and host_pass)


def send_otp_email(email, otp):
    """Send OTP email - uses real SMTP if configured, else logs for local dev"""
    subject = "PaperAIzer - Password Reset OTP"
    message = f"""Hello,

Your One-Time Password (OTP) for resetting your PaperAIzer password is:

  {otp}

This OTP is valid for 10 minutes. Do not share this with anyone.

If you did not request this, please ignore this email.

Best regards,
PaperAIzer Team"""

    try:
        logger.info(f"Processing OTP email request for {email}")

        if not _is_email_configured():
            sep = "=" * 60
            logger.warning(sep)
            logger.warning("  LOCAL OTP SIMULATOR")
            logger.warning(f"  Email : {email}")
            logger.warning(f"  OTP   : {otp}")
            logger.warning("  Valid : 10 minutes")
            logger.warning(sep)
            if settings.DEBUG:
                print(f"\n{sep}")
                print("  LOCAL OTP SIMULATOR")
                print(f"  Email : {email}")
                print(f"  OTP   : {otp}")
                print("  (copy this code to the verify page)")
                print(f"{sep}\n")
            return True

        from_email = get_from_email()

        logger.info(f"Attempting to send OTP email via SMTP to {email}")
        logger.info(
            f"SMTP Config: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}, "
            f"TLS={settings.EMAIL_USE_TLS}, FROM={from_email}"
        )

        try:
            result = send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[email],
                fail_silently=False,
            )

            if result == 1:
                logger.info(f"OTP email sent successfully to {email}")
                return True
            logger.error(f"Email sending returned {result} (expected 1)")
            return False

        except Exception as smtp_error:
            logger.error(f"SMTP error sending OTP to {email}: {smtp_error}", exc_info=True)

            error_str = str(smtp_error).lower()
            if 'authentication' in error_str or 'username' in error_str or 'password' in error_str:
                logger.error("Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct")
                logger.error("For Gmail, use App Password: https://myaccount.google.com/apppasswords")
            elif 'timeout' in error_str:
                logger.error("SMTP connection timeout - check firewall or EMAIL_TIMEOUT setting")
            elif 'connection refused' in error_str:
                logger.error("Connection refused - check EMAIL_HOST and EMAIL_PORT")
            elif 'tls' in error_str or 'ssl' in error_str:
                logger.error("TLS/SSL error - verify EMAIL_USE_TLS and EMAIL_USE_SSL settings")

            return False

    except Exception as e:
        logger.error(f"Unexpected error processing OTP email for {email}: {e}", exc_info=True)
        return False


def create_and_send_otp(email):
    """Create OTP record and trigger delivery. Returns (reset_otp_obj, email_sent_bool)."""
    try:
        existing = PasswordResetOTP.objects.filter(
            email=email,
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first()

        if existing:
            otp = existing.otp
            reset_otp = existing
            logger.info(f"Reusing existing valid OTP for {email}")
        else:
            PasswordResetOTP.objects.filter(email=email).delete()

            otp = generate_otp()
            expires_at = timezone.now() + timedelta(minutes=10)
            reset_otp = PasswordResetOTP.objects.create(
                email=email,
                otp=otp,
                expires_at=expires_at
            )
            logger.info(f"Created new OTP for {email}")

        if settings.DEBUG:
            print(f"\n{'='*50}")
            print(f"  OTP FOR {email}: {otp}")
            print(f"{'='*50}\n")

        email_sent = send_otp_email(email, otp)
        return reset_otp, email_sent

    except Exception as e:
        logger.error(f"Error in create_and_send_otp for {email}: {e}", exc_info=True)
        return None, False


def verify_otp(email, otp):
    """Verify OTP code for a given email"""
    try:
        reset_otp = PasswordResetOTP.objects.get(email=email, otp=otp)
        if reset_otp.is_valid():
            return True, reset_otp
        return False, None
    except PasswordResetOTP.DoesNotExist:
        return False, None


def mark_otp_as_used(email, otp):
    """Mark OTP as used after successful password reset"""
    try:
        reset_otp = PasswordResetOTP.objects.get(email=email, otp=otp)
        reset_otp.is_used = True
        reset_otp.save()
        return True
    except PasswordResetOTP.DoesNotExist:
        return False
