from django.shortcuts import render
from .models import Track
from django.views.generic import DetailView
import sys
sys.path.append('D:\\Python\\Music-Analyzer\\source\\Parsing')

from DBHelper import DBHelper

# Create your views here.

# Здесь выводится список похожих и прочая информация
def track(request, id_):


    return render(request, "tracks/track.html")

