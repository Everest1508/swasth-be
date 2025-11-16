from rest_framework import views, permissions
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import DoctorAvailabilityMetric, HealthIssueMetric, PharmacyStockMetric, TeleconsultationMetric
from .serializers import (
    DoctorAvailabilityMetricSerializer,
    HealthIssueMetricSerializer,
    PharmacyStockMetricSerializer,
    TeleconsultationMetricSerializer
)


class AnalyticsDashboardView(views.APIView):
    """
    Admin dashboard analytics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=403)
        
        # Date range (last 30 days)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Doctor availability vs demand
        doctor_metrics = DoctorAvailabilityMetric.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).aggregate(
            total_slots=Sum('total_slots'),
            booked_slots=Sum('booked_slots'),
            available_slots=Sum('available_slots')
        )
        
        # Most common health issues
        common_issues = HealthIssueMetric.objects.filter(
            date__gte=start_date
        ).values('issue_name').annotate(
            total_count=Sum('patient_count')
        ).order_by('-total_count')[:10]
        
        # Pharmacy stock trends
        low_stock_count = PharmacyStockMetric.objects.filter(
            date__gte=start_date,
            stock_quantity__lte=10
        ).count()
        
        # Teleconsultation success metrics
        teleconsultation_stats = TeleconsultationMetric.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).aggregate(
            total_consultations=Count('id'),
            successful_consultations=Count('id', filter=Q(was_successful=True)),
            avg_duration=Avg('consultation_duration')
        )
        
        return Response({
            'doctor_availability': doctor_metrics,
            'common_health_issues': list(common_issues),
            'pharmacy_stock': {
                'low_stock_alerts': low_stock_count
            },
            'teleconsultation': teleconsultation_stats
        })


class DoctorAvailabilityView(views.APIView):
    """
    Doctor availability analytics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        doctor_id = request.query_params.get('doctor_id')
        queryset = DoctorAvailabilityMetric.objects.all()
        
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        serializer = DoctorAvailabilityMetricSerializer(queryset, many=True)
        return Response(serializer.data)


class HealthIssuesView(views.APIView):
    """
    Health issues analytics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        queryset = HealthIssueMetric.objects.all().order_by('-patient_count', '-date')
        serializer = HealthIssueMetricSerializer(queryset, many=True)
        return Response(serializer.data)
