from django.contrib import admin
from django.urls import path, include
from backend.views import erro_403

handler403 = "backend.views.erro_403"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('', include('backend.urls')),
]
