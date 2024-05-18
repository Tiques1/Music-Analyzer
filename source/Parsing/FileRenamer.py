import os
import glob
import time


class FileRenamer:
    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.last_downloaded = None

    def rename(self, id_: str):
        self.last_downloaded = id_

    def mainloop(self):
        while True:
            try:
                list_of_files = glob.glob(f'{self.file_dir}*.mp3')
                latest_file = max(list_of_files, key=os.path.getctime)
            except (ValueError, FileNotFoundError):
                continue
            try:
                os.rename(latest_file, self.file_dir + self.last_downloaded + '.mp3')
                self.last_downloaded = None
            except (TypeError, FileExistsError):
                continue
            time.sleep(0.01)
