from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SMTPConfiguration
from .serializers import SMTPConfigurationSerializer
from .service import EmailService


class SMTPConfigurationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SMTP Configuration management
    """
    serializer_class = SMTPConfigurationSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = SMTPConfiguration.objects.all()
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """
        Test SMTP configuration by sending a test email
        """
        smtp_config = self.get_object()
        
        test_email = request.data.get('test_email', request.user.email)
        if not test_email:
            return Response(
                {'error': 'test_email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Temporarily set this config as active for testing
        original_active = SMTPConfiguration.objects.filter(is_active=True).exclude(id=smtp_config.id).first()
        if original_active:
            original_active.is_active = False
            original_active.save()
        smtp_config.is_active = True
        smtp_config.save()
        
        try:
            # Send test email
            subject = "Test Email - Nabha Health Connect"
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
                    .content { padding: 20px; background-color: #f9f9f9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Test Email</h1>
                    </div>
                    <div class="content">
                        <p>This is a test email from Nabha Health Connect.</p>
                        <p>If you received this email, your SMTP configuration is working correctly!</p>
                        <p>Best regards,<br>Nabha Health Connect Team</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            success = EmailService.send_email(
                to_email=test_email,
                subject=subject,
                html_content=html_content,
                text_content="This is a test email from Nabha Health Connect. If you received this, your SMTP configuration is working correctly!"
            )
            
            # Restore original active config
            smtp_config.is_active = False
            smtp_config.save()
            if original_active:
                original_active.is_active = True
                original_active.save()
            
            if success:
                return Response({
                    'message': f'Test email sent successfully to {test_email}'
                })
            else:
                return Response(
                    {'error': 'Failed to send test email. Please check your SMTP configuration.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            # Restore original active config
            smtp_config.is_active = False
            smtp_config.save()
            if original_active:
                original_active.is_active = True
                original_active.save()
            
            return Response(
                {'error': f'Error sending test email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

