from django.urls import path
from . import views

urlpatterns = [
    path('<int:id_>/', views.track, name='track')
]
