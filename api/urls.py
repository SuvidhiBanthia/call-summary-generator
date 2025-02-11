from django.urls import path
from .views import GenerateSummaryView

urlpatterns = [
    path('api/generate-summary/', GenerateSummaryView.as_view(), name='generate-summary'),
]