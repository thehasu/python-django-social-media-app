from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('settings', views.settings, name="settings"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logout, name="logout"),

    path('user/<int:pk>/', views.person_update_view, name='update_profile'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX
]
