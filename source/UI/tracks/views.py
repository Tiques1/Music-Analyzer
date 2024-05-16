from django.shortcuts import render
from .models import Track
from django.views.generic import DetailView
import sys
sys.path.append('D:\\Python\\Music-Analyzer\\source\\Parsing')

from DBHelper import DBHelper

# Create your views here.


def tracks(request):
    # tracks = Track.objects.all()
    # tracks = Track.objects.order_by('name')
    name = request.GET.get('name')
    # return render(request, "tracks/track.html", {'tracks': tracks})
    db = DBHelper(database="music", user="postgres", password="1111", host='localhost')
    db.exec(f'select * from track where name like {name}')
    return render(request, "main/layout.html", {'tracks': db.fetch_many(10)})


class TrackDetailView(DetailView):
    model = Track
    template_name = 'tracks/view.html'
    context_object_name = 'track'
