from django.urls import path

from login import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('user/<str:user_id>/', views.user_home, name='user_home'),
    path('send_email/', views.send_email, name='send_email'),
    path('new_psw/', views.psw_rst, name='psw_rst'),
]
