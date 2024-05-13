import time
import joblib
import faiss
from Music_recommendation import Extractor

exctractor = joblib.load('exctractor_test.pkl')

dim = 1000000
k = 5  # количество кластеров. С меньшим количеством кластеров время обучения уменьшается
quantiser = faiss.IndexFlatL2(dim)
index = faiss.IndexIVFFlat(quantiser, dim, k)

# Запускаем обучение:
study_start = time.time()

index.train(exctractor.song_vectors_np)  # Train на нашем наборе векторов

study_end = time.time()
print('Время на обучение', study_end - study_start)  # 11.788739681243896

index.add(exctractor.song_vectors_np)

start = time.time()
topn = 7
D, I = index.search(exctractor.song_vectors_np[30:31], topn)  # Возвращает результат: Distances, Indices
print(I)
print(D)
end = time.time()
print('Время поиска', end-start)  # 0.026042699813842773



