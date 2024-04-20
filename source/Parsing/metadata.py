from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TCON, TDRC, TextFrame


class Track:
    def __init__(self, mp3_file):
        self.__audio = MP3(mp3_file, ID3=ID3)
        self.__information = self.__text_metadata()

        self.title = self.__information.get(TIT2)
        self.artist = self.__information.get(TPE1).split('/')
        self.album = self.__information.get(TALB)
        self.alb_number = self.__information.get(TRCK)
        self.genre = self.__information.get(TCON)
        self.year = self.__information.get(TDRC)

        # https://mutagen.readthedocs.io/en/latest/api/mp3.html#mutagen.mp3.MPEGInfo
        self.file_info = self.__audio.info

    def __text_metadata(self):
        information = {}
        for tag in self.__audio.tags.values():
            try:
                if issubclass(type(tag), TextFrame):
                    information[type(tag)] = tag.text[0]
            finally:
                pass
        return information

    def cover(self, output=None):
        if "APIC:" not in self.__audio.tags:
            return
        if output is not None:
            with open(f"{output}", "wb") as f:
                f.write(self.__audio.tags["APIC:"].data)
        return self.__audio.tags["APIC:"].data


if __name__ == "__main__":
    file = r"D:\Music\Vxlious - Alright.mp3"
    track = Track(file)

    print(track.title)
    print(track.artist)
    print(track.genre)
    print(track.album)
    print(track.year)
    print(track.alb_number)
    bytes_image = track.cover('cover2.jpg')

    print(track.file_info.bitrate)
