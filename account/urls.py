
from django.urls import path
from .views import *



urlpatterns = [
    path('reg',UserRegView.as_view(),name='reg'),
    path('lgout',LgoutView.as_view(),name='lgout'),
]