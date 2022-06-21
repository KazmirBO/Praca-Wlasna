import yt_dlp
import platform
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

# Klasy i funkcje wykorzystywane do pobierania filmów/utworów.


class _DownloadMP3(QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, id, path, progresPob, parent=None):
        QThread.__init__(self, parent)
        self.platforma = platform.system()
        self.ident = id
        self.sciezka = path
        self.progresPob = progresPob

    def run(self):
        ydl_opts = {'outtmpl': self.sciezka + '%(title)s.%(ext)s',
                    'audio-format': 'bestaudio',
                    'progress_hooks': [self.my_hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }], }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.ident])

    def my_hook(self, d):
        if self.platforma == "Windows":
            self.file_tuple = d['filename'].split("\\")[-1]
        else:
            self.file_tuple = d['filename'].split("/")[-1]
        # self.file_tuple = os.path.split(os.path.abspath(d['filename']))
        if d['status'] == 'finished':
            self.progresPob.setText("Pobieranie zakończone.")
        if d['status'] == 'downloading':
            self.progresPob.setText(self.file_tuple + ", Pozostało: "
                                    + d['_percent_str'] + ", " + d['_eta_str'])


class _DownloadMP4(QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, id, path, progresPob, parent=None):
        QThread.__init__(self, parent)
        self.platforma = platform.system()
        self.ident = id
        self.sciezka = path
        self.progresPob = progresPob

    def run(self):
        ydl_opts = {'outtmpl': self.sciezka + '%(title)s.%(ext)s',
                    'progress_hooks': [self.my_hook],
                    'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.ident])

    def my_hook(self, d):
        if self.platforma == "Windows":
            self.file_tuple = d['filename'].split("\\")[-1]
        else:
            self.file_tuple = d['filename'].split("/")[-1]
        # self.file_tuple = os.path.split(os.path.abspath(d['filename']))
        if d['status'] == 'finished':
            self.progresPob.setText("Pobieranie zakończone.")
        if d['status'] == 'downloading':
            self.progresPob.setText(self.file_tuple + ", Pozostało: "
                                    + d['_percent_str'] + ", " + d['_eta_str'])
