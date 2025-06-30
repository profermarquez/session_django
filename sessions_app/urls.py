# sessions_app/urls.py

from django.urls import path
from . import views

app_name = 'sessions_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('set/', views.set_session_data, name='set_session'),
    path('get/', views.get_session_data, name='get_session'),
    path('delete/', views.delete_session_data, name='delete_session'),
    path('flush/', views.flush_session, name='flush_session'),
    path('test_cookies/', views.test_cookies, name='test_cookies'),
    path('check_test_cookie/', views.check_test_cookie, name='check_test_cookie'),
    path('delete_test_cookie_view/', views.delete_test_cookie_view, name='delete_test_cookie'),
    path('set_expiry_seconds/', views.set_expiry_seconds, name='set_expiry_seconds'),
    path('set_expiry_browser/', views.set_expiry_browser, name='set_expiry_browser'),
    path('set_expiry_none/', views.set_expiry_none, name='set_expiry_none'),
    path('session_info/', views.session_info, name='session_info'),
]