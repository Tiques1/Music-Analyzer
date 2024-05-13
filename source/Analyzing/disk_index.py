import time
import joblib
import faiss
from Music_recommendation import Extractor

exctractor = joblib.load('exctractor_test.pkl')
print('Загрузил exctractor')
dim = 1000000
k = 5  # количество “командиров”
quantiser = faiss.IndexFlatL2(dim)
index = faiss.IndexIVFFlat(quantiser, dim, k)
print('Создал index')
index.train(exctractor.song_vectors_np)
print('Обучил index')
# Сохраняем пустой обученный индекс, содержащий только параметры:
faiss.write_index(index, r".\indexes\trained_block.index")
print('Сохранил index')
# Поочередно создаем новые индексы на основе обученного
# Блоками добавляем в них части датасета:
for bno in range(0, 6):
    block_vectors = exctractor.song_vectors_np[bno*10:(bno+1)*10]
    block_vectors_ids = range(bno*10, (bno+1)*10)  # id векторов, если необходимо
    index = faiss.read_index(r".\indexes\trained_block.index")
    index.add_with_ids(block_vectors, block_vectors_ids)
    faiss.write_index(index, r".\indexes\block_{}.index".format(bno))
print('Сохранил индексы блоками')
# Объединяем воедино
ivfs = []
for bno in range(0, 6):
    index = faiss.read_index(r".\indexes\block_{}.index".format(bno))
    ivfs.append(index.invlists)
    # считать index и его inv_lists независимыми
    # чтобы не потерять данные во время следующей итерации:
    index.own_invlists = False
print('Объединил индексы')

# создаем финальный индекс:
index = faiss.read_index(r".\indexes\trained_block.index")

# готовим финальные invlists
# все invlists из блоков будут объединены в файл merged_index.ivfdata
invlists = faiss.OnDiskInvertedLists(index.nlist, index.code_size)
ivf_vector = faiss.InvertedListsPtrVector()

for ivf in ivfs:
    ivf_vector.push_back(ivf)

ntotal = invlists.merge_from(ivf_vector.data(), ivf_vector.size())
index.ntotal = ntotal  # заменяем листы индекса на объединенные
index.replace_invlists(invlists)
faiss.write_index(index, r".\indexes\populated.index")  # сохраняем всё на диск

"""В populated.index записан первоначальный полный путь к файлу с Inverted Lists, поэтому, если путь к файлу ivfdata 
по какой-то причине изменится, при чтении индекса потребуется использовать флаг faiss.IO_FLAG_ONDISK_SAME_DIR, 
который позволяет искать ivfdata файл в той же директории, что и populated.index:
"""
index = faiss.read_index(r'.\indexes\populated.index', faiss.IO_FLAG_ONDISK_SAME_DIR)

start = time.time()
topn = 7
D, I = index.search(exctractor.song_vectors_np[30:31], topn)  # Возвращает результат: Distances, Indices
print(I)
print(D)
end = time.time()
print('Время поиска', end-start)
