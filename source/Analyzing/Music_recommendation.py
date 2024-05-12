#!/usr/bin/env python
# coding: utf-8

import os
import librosa
import numpy as np
from scipy.spatial.distance import cosine
import scipy.stats


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield path + '\\' + file
list_files = []
for file in files("C:\\Users\\Leonochek\\Desktop\\music"):
       list_files.append(file)
print(list_files)


def extract_features(audio_path):
    y, sr = librosa.load(audio_path)

    # Извлечение MFCC, хромограммы, спектрального центроида, мел-спектрограммы и оценки глобального темпа
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
    melspectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    
    # Создание признакового вектора путем объединения характеристик
    features = [tempo[0], np.mean(melspectrogram), np.mean(mfccs), np.mean(chroma), np.mean(spectral_centroid)]
    return features

def create_songs_base(music_files):
    for song in music_files:
        audio_path = song
        song_name = audio_path.split("\\")[-1][0:-4]
        track_features = (extract_features(audio_path))
        couple_song_features = (song_name, track_features)
        couples_song_features.append(couple_song_features)
    return couples_song_features

#songs_base здесь - это список кортежей ("Название песни" - ["Объединенные характеристики в вектор"])
def recommend_song(users_song, songs_base):
        song_features = extract_features(users_song)
        for track in songs_base:
            similarity = 1 - cosine(song_features, track[1])
            if similarity > 0.99992 and similarity < 1 :
                similar_tracks.append(track[0])
        print('Песни с такими характеристиками Вам понравятся')
        return similar_tracks
    
similar_tracks = []
features_of_songs = []    
couples_song_features = []    

title_and_data = create_songs_base(list_files)

#Пример рекомендаций для одной из песен
print(recommend_song(r"C:\Users\Leonochek\Desktop\music\Bring Me The Horizon - Sleepwalking.mp3",title_and_data))



