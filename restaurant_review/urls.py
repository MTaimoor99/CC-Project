from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attendance_history',views.attendance_history, name='attendance_history'),
    path('analytics_dashboard',views.analytics_dashboard, name='analytics_dashboard'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout_user,name='logout'),
]
