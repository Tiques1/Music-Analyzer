import numpy as np
from scipy.spatial import KDTree

# Генерация случайной спектрограммы для примера
np.random.seed(42)
spectrogram = np.random.rand(100, 40)  # 100 временных отсечек, 40 частотных диапазонов

# Параметры временного отрезка
time_window_size = 10  # длина временного отрезка

# Построение k-d дерева
tree = KDTree([[]], leafsize=10)
for t in range(0, spectrogram.shape[0] - time_window_size + 1):
    time_slice = spectrogram[t:t + time_window_size].flatten()
    tree = tree.insert(np.array(time_slice))

# Определение вектора для поиска и диапазона
query_vector = spectrogram[35:35 + time_window_size].flatten()
tolerance = 0.4

# Поиск всех векторов в диапазоне
results = tree.query_ball_point(query_vector, tolerance)

print("Найденные временные отрезки:", results)
