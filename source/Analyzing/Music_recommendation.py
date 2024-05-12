#!/usr/bin/env python
# coding: utf-8

import os
import librosa
import numpy as np
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

from diagrams import Model
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
        self.song_names = np.array([])
        self.song_vectors = []

        self.song_vectors_np = None

    def values_to_np(self):
        # Преобразование списков в массивы NumPy
        vectors_np = [np.array(vector) for vector in self.song_vectors]

        # Преобразование списка массивов NumPy в двумерный массив NumPy
        self.song_vectors_np = np.array(vectors_np)

    @staticmethod
    def add_zero(array):
        if len(array) > 1000000:
            return array[0:1000000]
        else:
            return np.append(array, np.array([0 for _ in range(0, 1000000-len(array))]))

    def extract_features(self, audio_path):
        y, sr = librosa.load(audio_path)

        # Извлечение MFCC, хромограммы, спектрального центроида, мел-спектрограммы и оценки глобального темпа
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
        melspectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

        # print(len(onset_env), len(tempo), len(melspectrogram), len(mfccs), len(chroma), len(spectral_centroid))
        # Создание признакового вектора путем объединения характеристик
        # features = [tempo[0], np.mean(melspectrogram), np.mean(mfccs), np.mean(chroma), np.mean(spectral_centroid)]
        features = np.concatenate((np.array([tempo[0]]), np.concatenate(melspectrogram), np.concatenate(mfccs),
                                   np.concatenate(chroma), np.concatenate(spectral_centroid)))

        return self.add_zero(features)

    def create_songs_base(self, music_files):
        for song in music_files:
            song_name = song.split("\\")[-1][0:-4]
            track_features = self.extract_features(song)

            self.song_names = np.append(self.song_names, song_name)
            self.song_vectors.append(track_features)


class Reccommender:
    def __init__(self, extractor_):
        self.extractor = extractor_
        self.similar_tracks = []

    # def recommend_song(self, users_song, songs_base):
    #     song_feature = self.extractor.extract_features(users_song)
    #     for track in songs_base:
    #         similarity = 1 - cosine(song_feature, track[1])
    #         if 0.6 <= similarity <= 1:  # 0.99992 <= similarity <= 1
    #             self.similar_tracks.append((track[0], similarity))

    def recommend_song(self, user_song, songs_base):
        pass


def find_nearest_points(embeddings, target_point, k=5):
    # Вычисление расстояний между целевой точкой и всеми другими точками
    # https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
    distances = np.linalg.norm(embeddings - target_point, axis=1)

    # Нахождение индексов точек с наименьшими расстояниями (кроме целевой точки)
    nearest_indices = np.argsort(distances)[1:k + 1]

    return nearest_indices


if __name__ == '__main__':
    # files = Files("D:\\Music\\Test")
    #
    # extractor = Extractor()
    # extractor.create_songs_base(files.list_files)
    # extractor.values_to_np()
    # joblib.dump(extractor, 'exctractor_test.pkl')


    # recommender = Reccommender(extractor)
    # recommender.recommend_song(r"D:\Music\Paul Mauriat and His Orchestra,Вольфганг Амадей Моцарт - Symphony No. 40 In G Minor K550_ 1. Molto Allegro.mp3",
    #                            extractor.couples_song_features)
    #
    # print(sorted(recommender.similar_tracks, reverse=True, key=lambda x: x[1]))
    # Преобразование одномерных векторов в двумерные с помощью TSNE
    extractor = joblib.load('exctractor_test.pkl')
    # Преобразование списков в массивы NumPy
    # song_vectors_np = [np.array(vector) for vector in extractor.song_vectors]
    #
    # # Преобразование списка массивов NumPy в двумерный массив NumPy
    # song_vectors_np = np.array(song_vectors_np)

    id = np.where(extractor.song_names == "Johann Sebastian Bach,Voque Session,Laysan Khusniyarova - Cello Suite No. 1 in G Major_ Prélude")
    print(extractor.song_names[id])
    print('Ближайшие к нему: ')
    nearest = find_nearest_points(extractor.song_vectors_np, extractor.song_vectors_np[id])
    for i in nearest:
        print(extractor.song_names[i])

    # # Создание объекта t-SNE
    # tsne = TSNE(n_components=2, random_state=42, perplexity=5)
    #
    # # Применение t-SNE к массиву векторов признаков
    # embeddings_2d = tsne.fit_transform(extractor.song_vectors_np)
    #
    # # Создание объекта KMeans для кластеризации
    # kmeans = KMeans(n_clusters=3, random_state=42)
    #
    # # Кластеризация вложений
    # clusters = kmeans.fit_predict(embeddings_2d)
    #
    # # Отрисовка графика с раскрашенными кластерами
    # plt.figure(figsize=(10, 10))
    #
    # # Раскрашиваем точки в соответствии с кластерами
    # plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=clusters, cmap='tab10')
    #
    # # Подписываем точки именами треков
    # for i, track_name in enumerate(extractor.song_names):
    #     plt.annotate(track_name, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
    #
    # plt.xlabel('TSNE Component 1')
    # plt.ylabel('TSNE Component 2')
    # plt.title('TSNE Visualization of Track Embeddings with KMeans Clusters')
    # plt.colorbar(label='Cluster')
    # plt.show()








    # tsne = TSNE(n_components=2, random_state=42, perplexity=3)
    # embeddings_2d = tsne.fit_transform(song_vectors_np)
    #
    # # Отрисовка графика
    # plt.figure(figsize=(10, 10))
    # plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
    #
    # # Добавление названий треков к точкам
    # for i, track_name in enumerate(extractor.song_names):
    #     plt.annotate(track_name, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
    #
    # plt.xlabel('TSNE Component 1')
    # plt.ylabel('TSNE Component 2')
    # plt.title('TSNE Visualization of Track Embeddings')
    # plt.show()

    pass