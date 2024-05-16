from django.urls import path
from . import views

urlpatterns = [
    path("", views.tracks, name='home'),
    path('<str:pk>/', views.TrackDetailView.as_view(), name='detail_track')
]
