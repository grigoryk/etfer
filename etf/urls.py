from django.urls import path

from . import views

urlpatterns = [
    path('portfolio/<int:portfolio_id>/', views.portfolio),
]