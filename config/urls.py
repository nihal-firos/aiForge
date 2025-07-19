# config/urls.py
from django.contrib import admin
from django.urls import path, include
from users.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('worksheets/', include('worksheets.urls')),
    path('exams/', include('exams.urls')),
    path('accounts/', include('users.urls')),
]