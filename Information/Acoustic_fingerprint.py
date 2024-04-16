import librosa
from pydub import AudioSegment
from pydub.playback import play

# Функция для создания акустического отпечатка
def create_acoustic_fingerprint(audio_file):
    # Загружаем аудиофайл
    audio = AudioSegment.from_file(audio_file)

    # Преобразуем аудиофайл в numpy массив и получаем частоту дискретизации
    audio_array = audio.get_array_of_samples()
    sr = audio.frame_rate

    # Преобразуем аудио в моно звук
    if audio.channels > 1:
        audio_array = audio_array[::audio.channels]

    # Создаем mel-спектрограмму
    mel_spectrogram = librosa.feature.melspectrogram(y=audio_array, sr=sr)

    # Преобразуем мел-спектрограмму в дБ (логарифмическая шкала)
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Создаем акустический отпечаток (примерно)
    acoustic_fingerprint = hash(tuple(log_mel_spectrogram.flatten()))

    return acoustic_fingerprint

if __name__ == "__main__":
    audio_file = "your_audio_file.mp3"
    acoustic_fingerprint = create_acoustic_fingerprint(audio_file)
    print("Acoustic Fingerprint:", acoustic_fingerprint)
