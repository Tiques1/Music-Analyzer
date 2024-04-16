from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TRCK


def extract_mp3_metadata(file):
    try:
        audio = MP3(mp3_file, ID3=ID3)
        tags = audio.tags

        # Получение названия трека (Title)
        if "TIT2" in tags:
            title = tags["TIT2"].text[0]
        else:
            title = "Unknown Title"

        # Получение исполнителя (Artist)
        if "TPE1" in tags:
            artist = tags["TPE1"].text[0]
        else:
            artist = "Unknown Artist"

        # Получение альбома (Album)
        if "TALB" in tags:
            album = tags["TALB"].text[0]
        else:
            album = "Unknown Album"

        # Получение номера трека (Track Number)
        if "TRCK" in tags:
            track_number = tags["TRCK"].text[0]
        else:
            track_number = "Unknown Track Number"

        # Жанр (Genre)
        if "TCON" in tags:
            genre = tags["TCON"].text[0]
        else:
            genre = "No genre"

        # Вывод метаданных
        print("Название трека:", title)
        print("Исполнитель:", artist)
        print("Альбом:", album)
        print("Номер трека:", track_number)
        print("Жанр", genre)

        # Получение обложки (Cover Art)
        if "APIC:" in tags:
            for key in tags.keys():
                if "APIC:" in key:
                    with open("cover.jpg", "wb") as f:
                        f.write(tags[key].data)
                    print("Обложка сохранена в файл 'cover.jpg'")
                    break
        else:
            print("Обложка не найдена")

    except Exception as e:
        print("Произошла ошибка:", e)


# Пример использования
if __name__ == "__main__":
    # Укажите путь к вашему MP3 файлу
    mp3_file = "D:\\Music\\Unlike Pluto,Joanna Jones - No Scrubs (feat. Joanna Jones).mp3"
    extract_mp3_metadata(mp3_file)
