from django.urls import path
from .views import *

urlpatterns = [
    path('faturas/', faturas, name='faturas')
]
