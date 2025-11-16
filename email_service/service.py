import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from .models import SMTPConfiguration
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Custom email service using SMTP configuration
    """
    
    @staticmethod
    def get_active_smtp_config():
        """
        Get active SMTP configuration
        """
        try:
            # First try to get an active configuration
            config = SMTPConfiguration.objects.filter(is_active=True).first()
            
            # If no active config, try to get any configuration
            if not config:
                config = SMTPConfiguration.objects.first()
                if config:
                    logger.warning(f"No active SMTP configuration found. Using first available: {config.name}")
            
            # Log all configurations for debugging
            all_configs = SMTPConfiguration.objects.all()
            if all_configs.exists():
                logger.info(f"Available SMTP configurations: {[(c.name, c.is_active) for c in all_configs]}")
            
            return config
        except Exception as e:
            logger.error(f"Error getting SMTP config: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def send_email(to_email, subject, html_content, text_content=None):
        """
        Send email using configured SMTP
        """
        smtp_config = EmailService.get_active_smtp_config()
        
        if not smtp_config:
            logger.error("No SMTP configuration found. Please configure SMTP settings in the admin dashboard.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{smtp_config.from_name} <{smtp_config.from_email}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server
            if smtp_config.use_ssl:
                server = smtplib.SMTP_SSL(smtp_config.host, smtp_config.port)
            else:
                server = smtplib.SMTP(smtp_config.host, smtp_config.port)
            
            if smtp_config.use_tls and not smtp_config.use_ssl:
                server.starttls()
            
            # Login and send
            server.login(smtp_config.username, smtp_config.password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_approval_email(email, name, user_type, login_credentials=None):
        """
        Send approval email to doctor/pharmacist
        """
        subject = f"Welcome to Nabha Health Connect - Your {user_type.title()} Account is Approved"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                .credentials {{ background-color: #fff; padding: 15px; border-left: 4px solid #4CAF50; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Nabha Health Connect!</h1>
                </div>
                <div class="content">
                    <p>Dear {name},</p>
                    <p>Congratulations! Your {user_type} application has been approved.</p>
                    <p>You can now access the platform and start serving patients in rural areas.</p>
                    """
        
        if login_credentials:
            html_content += f"""
                    <div class="credentials">
                        <h3>Your Login Credentials:</h3>
                        <p><strong>Email:</strong> {login_credentials['email']}</p>
                        <p><strong>Password:</strong> {login_credentials['password']}</p>
                        <p><em>Please change your password after first login.</em></p>
                    </div>
                    """
        
        html_content += f"""
                    <p>Click the button below to access your dashboard:</p>
                    <a href="http://localhost:8000/login/" class="button">Login to Dashboard</a>
                    <p>If you have any questions, please contact our support team.</p>
                    <p>Best regards,<br>Nabha Health Connect Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Dear {name},
        
        Congratulations! Your {user_type} application has been approved.
        You can now access the platform and start serving patients.
        
        Login URL: http://localhost:8000/login/
        
        Best regards,
        Nabha Health Connect Team
        """
        
        return EmailService.send_email(email, subject, html_content, text_content)
    
    @staticmethod
    def send_rejection_email(email, name, user_type, reason):
        """
        Send rejection email
        """
        subject = f"Nabha Health Connect - Application Status Update"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Application Status Update</h1>
                </div>
                <div class="content">
                    <p>Dear {name},</p>
                    <p>Thank you for your interest in joining Nabha Health Connect.</p>
                    <p>Unfortunately, your {user_type} application could not be approved at this time.</p>
                    <p><strong>Reason:</strong> {reason}</p>
                    <p>If you have any questions or would like to reapply, please contact our support team.</p>
                    <p>Best regards,<br>Nabha Health Connect Team</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return EmailService.send_email(email, subject, html_content)

