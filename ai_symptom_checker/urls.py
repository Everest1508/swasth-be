from django.urls import path
from .views import SymptomCheckerView, SymptomCheckHistoryView

app_name = 'ai_symptom_checker'

urlpatterns = [
    path('check/', SymptomCheckerView.as_view(), name='symptom_check'),
    path('history/', SymptomCheckHistoryView.as_view(), name='symptom_check_history'),
]

