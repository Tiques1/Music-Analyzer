# -*- coding: utf-8 -*-
"""
Created on Sat May 25 21:18:37 2024

@author: Leonochek
"""

import librosa
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA


class VectorFactory:
    def __init__(self, target_length=1000):
        self.target_length = target_length

    def load_audio(self, file_path):
        y, sr = librosa.load(file_path)
        return y, sr

    # 128 частотных диапазонов
    # Возращает массив длины 128, где каждый элемент имеет одинаковую длину в зависимости от длины трека
    def extract_mel_spectrogram(self, y, sr):
        return librosa.feature.melspectrogram(y=y, sr=sr)

    def extract_mfcc(self, y, sr):
        return librosa.feature.mfcc(y=y, sr=sr)

    def extract_chroma_stft(self, y, sr):
        return librosa.feature.chroma_stft(y=y, sr=sr)

    def extract_spectral_centroid(self, y, sr):
        return librosa.feature.spectral_centroid(y=y, sr=sr)

    # def interpolate_vector(self, vector):
    #     original_length = vector.shape[1]
    #     print(original_length)
    #     print(vector[0])
    #     # Создаем массив с новыми индексами
    #     new_indices = np.linspace(0, original_length - 1, num=self.target_length)
    #
    #     # Интерполируем вектор
    #     interpolated_vector = np.zeros((vector.shape[0], self.target_length))
    #     for i in range(vector.shape[0]):
    #         interpolated_vector[i, :] = np.interp(new_indices, np.arange(original_length), vector[i, :])
    #
    #     return interpolated_vector

    # 9.76 МБайт на каждый вектор
    def unify(self, vector):
        new = np.array([[None]*10000]*128)
        lenght = len(vector[0])
        if lenght < 10000:
            for i, v in enumerate(vector):
                new[i] = np.pad(v, (0, 10000 - lenght), mode='constant', constant_values=0.0)
        else:
            for i, v in enumerate(vector):
                new[i] = v[0:10000]

        return new.flatten()

    def create_vector(self, file_path, feature_type):
        y, sr = self.load_audio(file_path)

        if feature_type == 'mel_spectrogram':
            vector = self.extract_mel_spectrogram(y, sr)
        elif feature_type == 'mfcc':
            vector = self.extract_mfcc(y, sr)
        elif feature_type == 'chroma_stft':
            vector = self.extract_chroma_stft(y, sr)
        elif feature_type == 'spectral_centroid':
            vector = self.extract_spectral_centroid(y, sr)
        else:
            raise ValueError(f"Unknown feature type: {feature_type}")

        return self.unify(vector)


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


# Пример использования
if __name__ == "__main__":
    factory = VectorFactory()
    files = Files(r"D:\\Music\\Test")

    mel_vector = []

    for i in files.list_files[0:10]:
        mel_vector.append(factory.create_vector(i, 'mel_spectrogram'))
        print(len(mel_vector))

    X_pca = np.array(mel_vector)

    # pca = PCA(n_components=2)  # Выберите количество компонент для PCA
    # X_pca = pca.fit_transform(mel_vector)

    # Выполнение кластеризации с помощью KMeans
    kmeans = KMeans(n_clusters=3)  # Выберите количество кластеров
    kmeans.fit(X_pca)
    cluster_labels = kmeans.labels_

    # Визуализация результата
    plt.figure(figsize=(8, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis')
    plt.title('PCA Scatter Plot with Clusters')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.grid(True)
    plt.show()
    # # Визуализация результата
    # plt.figure(figsize=(8, 6))
    # plt.scatter(X_pca[:, 0], X_pca[:, 1])
    # plt.title('PCA Scatter Plot')
    # plt.xlabel('Principal Component 1')
    # plt.ylabel('Principal Component 2')
    # plt.grid(True)
    # plt.show()

    # # Создание объекта t-SNE
    # tsne = TSNE(n_components=2, random_state=42, perplexity=5)
    #
    # # Применение t-SNE к массиву векторов признаков
    # embeddings_2d = tsne.fit_transform(np.array(mel_vector))
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
    # #
    # # # Подписываем точки именами треков
    # # for i, track_name in enumerate(extractor.song_names):
    # #     if track_name in extractor.song_names[nearest]:
    # #         plt.annotate(track_name, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
    # #
    # plt.xlabel('TSNE Component 1')
    # plt.ylabel('TSNE Component 2')
    # plt.title('TSNE Visualization of Track Embeddings with KMeans Clusters')
    # plt.colorbar(label='Cluster')
    # plt.show()
