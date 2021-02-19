from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),

]
