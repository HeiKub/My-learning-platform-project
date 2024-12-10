from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
