from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='main_home'),
    path('about', views.about),
    path('like/<int:track>/', views.like),
    path('liked/', views.liked)
]
