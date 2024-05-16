from django.shortcuts import render
from django.http import HttpResponse
import sys

sys.path.append('D:\\Python\\Music-Analyzer\\source\\Parsing')

from DBHelper import DBHelper


def index(request):
    # data = {'title': 'Главная страница!!!',
    #         'values': ('1', '2', '3'),
    #         'dict': {'cat': 'orange',
    #                  'dog': 'black'},
    #         }
    # tracks = Track.objects.all()
    # tracks = Track.objects.order_by('name')
    name = request.GET.get('name')
    if not name:
        return render(request, "main/layout.html", {'track_list': ['NOT FOUND']})

    # return render(request, "tracks/track.html", {'tracks': tracks})
    db = DBHelper(database="music", user="postgres", password="1111", host='localhost')

    db.exec(f"(select * from track where name like '%{name}%')")
    tracks = db.fetch_all()
    tracks_list = ()
    if tracks:
        tracks_list = tracks

    db.exec(f"select * from artist where name like '%{name}%'")
    artists = db.fetch_all()
    artist_list = ()
    if artists:
        artist_list = artists

    db.exec(f"""SELECT track.*
    FROM track
    INNER JOIN autorship ON track.id = autorship.track
    INNER JOIN artist ON autorship.artist = artist.id
    WHERE artist.name like '%{name}%';
        """)
    authorship = db.fetch_all()
    authorship_list = ()
    if authorship:
        authorship_list = authorship

    return render(request, "main/layout.html", {'track_list': tracks_list, 'artist_list': artist_list,
                                                'authorship_list': authorship_list})


def about(request):
    return render(request, 'main/about.html')