import youtube_dl
import os
import platform
from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class _DownloadMP3(QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, id, path, progresPob, parent=None):
        QThread.__init__(self, parent)
        self.platform = platform.system()
        self.id = id
        self.path = path
        self.progresPob = progresPob

    def run(self):
        ydl_opts = {'outtmpl': self.path + '%(title)s.%(ext)s',
                    'audio-format': 'bestaudio',
                    'progress_hooks': [self.my_hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.id])

    def my_hook(self, d):
        if self.platform == "Windows":
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
        self.id = id
        self.path = path
        self.progresPob = progresPob

    def run(self):
        ydl_opts = {'outtmpl': self.path + '%(title)s.%(ext)s',
                    'progress_hooks': [self.my_hook],
                    'format': 'best'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.id])

    def my_hook(self, d):
        if self.platform == "Windows":
            self.file_tuple = d['filename'].split("\\")[-1]
        else:
            self.file_tuple = d['filename'].split("/")[-1]
        # self.file_tuple = os.path.split(os.path.abspath(d['filename']))
        if d['status'] == 'finished':
            self.progresPob.setText("Pobieranie zakończone.")
        if d['status'] == 'downloading':
            self.progresPob.setText(self.file_tuple + ", Pozostało: "
                                    + d['_percent_str'] + ", " + d['_eta_str'])
