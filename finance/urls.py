from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
  TokenObtainPairView, TokenRefreshView)

urlpatterns = [
  path('transactions/',views.TokenObtainPairView.as_view(),name='transaction-list'),
  path('transactions/<int:pk>/',view. TokenRefreshView.as_view(),name='transaction-detail'),
  
  ]
  