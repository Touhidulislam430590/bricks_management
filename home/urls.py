from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('company_profile/', views.company, name="company"),
    path('login/', views.login_page, name="login"),
    path('new_season/', views.new_season, name="new_season"),
    path('password_required_form/', views.password_required_form, name="password_required_form"),
]
