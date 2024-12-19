from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('delete-task/<int:id>/', views.delete_task, name='delete'),
    path('update/<int:id>/', views.update, name='update')
]