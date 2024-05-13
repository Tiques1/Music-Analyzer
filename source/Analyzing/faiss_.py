import numpy as np
dim = 512  # рассмотрим произвольные векторы размерности 512
nb = 10000  # количество векторов в индексе
nq = 5  # количество векторов в выборке для поиска
np.random.seed(228)
vectors = np.random.random((nb, dim)).astype('float32')
query = np.random.random((nq, dim)).astype('float32')

""" Создаем Flat индекс и добавляем векторы без обучения: 
Flat. Он лишь хранит в себе все вектора, а поиск по заданному вектору осуществляется полным перебором, 
поэтому обучать его не нужно (но об обучении ниже). На маленьком объеме данных такой простой индекс может вполне 
покрыть нужды поиска."""
# То есть время затрачиваемое на обучение других индексов, значительно больше, чем работа flat

import faiss
index = faiss.IndexFlatL2(dim)
print(index.ntotal)  # пока индекс пустой
index.add(vectors)
print(index.ntotal)  # теперь в нем 10 000 векторов

""" Теперь найдем 7 ближайших соседей для первых пяти векторов из vectors: """

topn = 7
D, I = index.search(vectors[:5], topn)  # Возвращает результат: Distances, Indices
print(I)
print(D)

""" Видим, что самые близкие соседи с расстоянием 0 – это сами векторы, остальные отранжированы по 
увеличению расстояния. Проведем поиск по нашим векторам из query: """

D, I = index.search(query, topn)
print(I)
print(D)

""" Индекс можно сохранить на диск и затем загрузить с диска: """

faiss.write_index(index, "flat.index")
index = faiss.read_index("flat.index")

"""FAISS IVF index
В этом и состоит идея IVF индекса: сгруппируем большой набор векторов по частям с помощью алгоритма k-means, 
 каждой части поставив в соответствие центроиду, – вектор, являющийся выбранным центром для данного кластера. 
Поиск будем осуществлять через минимальное расстояние до центроид, и только потом искать минимальные расстояния среди
 векторов в том кластере, что соответствует данной центроиде. Взяв k равным sqrt{n}, где n – количество векторов 
 в индексе, мы получим оптимальный поиск на двух уровнях – сначала среди sqrt{n} центроид, затем среди sqrt{n} 
 векторов в каждом кластере. Поиск по сравнению с полным перебором ускоряется в разы, что решает одну из наших проблем 
 при работе с множеством миллионов векторов."""

dim = 512
k = 1000  # количество “командиров”
quantiser = faiss.IndexFlatL2(dim)
index = faiss.IndexIVFFlat(quantiser, dim, k)
vectors = np.random.random((1000000, dim)).astype('float32')  # 1 000 000 “воинов”

""" А можно это записать куда более элегантно, воспользовавшись удобной штукой FAISS для построения индекса: """

index = faiss.index_factory(dim, "IVF1000, Flat")
# Запускаем обучение:
print(index.is_trained)  # False.
index.train(vectors)  # Train на нашем наборе векторов

# Обучение завершено, но векторов в индексе пока нет, так что добавляем их в индекс:
print(index.is_trained)  # True
print(index.ntotal)  # 0
index.add(vectors)
print(index.ntotal)  # 1000000

"""Скорость в разы меньше, по сравнению с полным перебором """
D, I = index.search(query, topn)
print(I)
print(D)

""" Но есть одно «но» – точность поиска, как и скорость, будет зависеть от количества посещаемых кластеров, 
которое можно задать с помощью параметра nprobe: """

print(index.nprobe)  # 1 – заходим только в один кластер и ведем поиск только в нём
index.nprobe = 16  # Проходим по топ-16 центроид для поиска top-n ближайших соседей
D, I = index.search(query, topn)
print(I)
print(D)

""" Конкретно для нашей задачи основное преимущество FAISS – в возможности хранить Inverted Lists IVF индекса на диске, 
загружая в RAM только метаданные.

Как мы создаем такой индекс: обучаем indexIVF с нужными параметрами на максимально возможном объеме данных, 
который влезает в память, затем в обученный индекс по частям добавляем векторы (побывавшие в обучении и не только) и
записываем на диск индекс для каждой из частей. """

index = faiss.index_factory(512, ",IVF65536, Flat", faiss.METRIC_L2)

""" Крайне желательно, чтобы обучающая выборка была максимально репрезентативна и имела равномерное распределение, 
поэтому мы заранее составляем обучающий датасет из необходимого количества векторов, рандомно выбирая их из всего 
датасета. """

train_vectors = ...  # предварительно сформированный датасет для обучения
index.train(train_vectors)

# Сохраняем пустой обученный индекс, содержащий только параметры:
faiss.write_index(index, "trained_block.index")

# Поочередно создаем новые индексы на основе обученного
# Блоками добавляем в них части датасета:
for bno in range(first_block, last_block+ 1):
    block_vectors = vectors_parts[bno]
    block_vectors_ids = vectors_parts_ids[bno]  # id векторов, если необходимо
    index = faiss.read_index("trained_block.index")
    index.add_with_ids(block_vectors, block_vectors_ids)
    faiss.write_index(index, "block_{}.index".format(bno))

"""После этого объединяем все Inverted Lists воедино. Это возможно, так как каждый из блоков, по сути, 
является одним и тем же обученным индексом, просто с разными векторами внутри."""

ivfs = []
for bno in range(first_block, last_block+ 1):
    index = faiss.read_index("block_{}.index".format(bno), faiss.IO_FLAG_MMAP)
    ivfs.append(index.invlists)
    # считать index и его inv_lists независимыми
    # чтобы не потерять данные во время следующей итерации:
    index.own_invlists = False

# создаем финальный индекс:
index = faiss.read_index("trained_block.index")

# готовим финальные invlists
# все invlists из блоков будут объединены в файл merged_index.ivfdata
invlists = faiss.OnDiskInvertedLists(index.nlist, index.code_size, "merged_index.ivfdata")
ivf_vector = faiss.InvertedListsPtrVector()

for ivf in ivfs:
    ivf_vector.push_back(ivf)

ntotal = invlists.merge_from(ivf_vector.data(), ivf_vector.size())
index.ntotal = ntotal  # заменяем листы индекса на объединенные
index.replace_invlists(invlists)
faiss.write_index(index, data_path + "populated.index")  # сохраняем всё на диск

"""В populated.index записан первоначальный полный путь к файлу с Inverted Lists, поэтому, если путь к файлу ivfdata 
по какой-то причине изменится, при чтении индекса потребуется использовать флаг faiss.IO_FLAG_ONDISK_SAME_DIR, 
который позволяет искать ivfdata файл в той же директории, что и populated.index:
"""
index = faiss.read_index('populated.index', faiss.IO_FLAG_ONDISK_SAME_DIR)


