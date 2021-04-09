from django.urls import path

from . import views

# Map the Urls Paths to the views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('game/', views.game, name='game'),
]