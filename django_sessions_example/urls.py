# django_sessions_example/django_sessions_example/urls.py

from django.contrib import admin
from django.urls import path, include
from sessions_app import views # Importa las vistas directamente para el index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sessions/', include('sessions_app.urls')), # Todas las URLs de sessions_app bajo /sessions/
    path('', views.index, name='home'), # La URL raíz apunta directamente al index de la app de sesiones
]