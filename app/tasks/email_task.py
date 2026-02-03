import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.celery_app import celery_app
from app.core.logger import setup_logger
from app.core.config import settings

logger = setup_logger()

@celery_app.task
def send_welcome_email(email_to: str):
    logger.info(f"📧 Sending welcome email to {email_to}...")
    
    subject = "Welcome to FastAPI MariaDB App!"
    body = f"Hello {email_to},\n\nWelcome to our service! We are glad to have you."
    
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USER
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        if settings.SMTP_SSL:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            if settings.SMTP_TLS:
                server.starttls()
        
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"✅ Email sent to {email_to} successfully!")
        return f"Email sent to {email_to}"
    except Exception as e:
        logger.error(f"❌ Failed to send email to {email_to}: {e}")
        return f"Failed to send email: {e}"

