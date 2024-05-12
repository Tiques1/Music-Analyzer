#!/usr/bin/env python
# coding: utf-8

import os
import librosa
import numpy as np
from scipy.spatial.distance import cosine
# import scipy.stats


class Files:
    def __init__(self, path):
        self.list_files = []
        self.path = path

        for file in self.files(self.path):
            self.list_files.append(file)

    @staticmethod
    def files(path):
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                yield path + '\\' + f


class Extractor:
    def __init__(self):
        # (song_name, track_features)
        self.couples_song_features = []

    @staticmethod
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

    def create_songs_base(self, music_files):
        for song in music_files:
            song_name = song.split("\\")[-1][0:-4]
            track_features = (self.extract_features(song))
            self.couples_song_features.append((song_name, track_features))


class Reccommender:
    def __init__(self, extractor_):
        self.extractor = extractor_
        self.similar_tracks = []

    def recommend_song(self, users_song, songs_base):
        song_feature = self.extractor.extract_features(users_song)
        for track in songs_base:
            similarity = 1 - cosine(song_feature, track[1])
            if 0.99992 <= similarity <= 1:
                self.similar_tracks.append((track[0], similarity))


if __name__ == '__main__':
    files = Files("D:\\Music")

    extractor = Extractor()
    extractor.create_songs_base(files.list_files)

    recommender = Reccommender(extractor)
    recommender.recommend_song(r"D:\Music\Paul Mauriat and His Orchestra,Вольфганг Амадей Моцарт - Symphony No. 40 In G Minor K550_ 1. Molto Allegro.mp3",
                               extractor.couples_song_features)

    print(sorted(recommender.similar_tracks, reverse=True, key=lambda x: x[1]))
