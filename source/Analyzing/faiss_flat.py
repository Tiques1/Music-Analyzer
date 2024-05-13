import time
import joblib
import faiss
from Music_recommendation import Extractor

exctractor = joblib.load('exctractor_test.pkl')

index = faiss.IndexFlatL2(1000000)
print(index.ntotal)  # пока индекс пустой
index.add(exctractor.song_vectors_np)
print(index.ntotal)
start = time.time()
topn = 7
D, I = index.search(exctractor.song_vectors_np[30:31], topn)  # Возвращает результат: Distances, Indices
print(I)
print(D)
end = time.time()
print(end-start)
""" 0.09897446632385254 для пачки из 5 запросов
    0.027014732360839844 для одиночного запроса """


