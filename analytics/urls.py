from django.urls import path
from .views import AnalyticsDashboardView, DoctorAvailabilityView, HealthIssuesView

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', AnalyticsDashboardView.as_view(), name='dashboard'),
    path('doctor-availability/', DoctorAvailabilityView.as_view(), name='doctor_availability'),
    path('health-issues/', HealthIssuesView.as_view(), name='health_issues'),
]

