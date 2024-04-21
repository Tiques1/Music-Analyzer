from YaMusicParser import YaMusicParser
from metadata import Track
from db_writer import DBHelper
import os

parser = YaMusicParser()
parser.save_dir = 'D:\\Music\\'

with open('links.txt', 'r') as file:
    links = file.readlines()

for link in links:
    parser.url = link
    parser.download()

db = DBHelper('music.db')
for t in os.listdir(parser.save_dir):
    track = Track(t)
    db.exec(f'insert into tracks values ({track.title})')
