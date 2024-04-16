import pyaudio
import wave
import io


# Функция для записи аудиопотока в файл
def save_audio_stream(url, output_file, duration=10):
    # Параметры для записи звука
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = duration

    # Инициализация объекта PyAudio
    audio = pyaudio.PyAudio()

    # Открытие потока для записи звука
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Запись аудиопотока...")

    frames = []

    # Запись звука в буфер
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Запись завершена.")

    # Остановка и закрытие потока
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Создание байтового потока из записанного аудиопотока
    audio_data = b''.join(frames)

    # Сохранение записанного аудиопотока в файл
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)

    print(f"Аудиопоток сохранен в файл: {output_file}")


# Пример использования
if __name__ == "__main__":
    # URL трека на Яндекс.Музыке (или другом источнике)
    track_url = "https://music.yandex.ru/track/1234567890"

    # Название файла для сохранения аудиопотока
    output_file = "audio_stream.wav"

    # Вызов функции для записи аудиопотока в файл
    save_audio_stream(track_url, output_file, duration=30)
