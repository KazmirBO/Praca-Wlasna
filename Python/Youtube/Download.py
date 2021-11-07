import youtube_dl
from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class _DownloadMP3(QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, id, path, parent=None):
        QThread.__init__(self, parent)
        self.id = id
        self.path = path

    def run(self):
        ydl_opts = {'outtmpl': self.path + '%(title)s.%(ext)s',
                    'audio-format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.id])


class _DownloadMP4(QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, id, path, parent=None):
        QThread.__init__(self, parent)
        self.id = id
        self.path = path

    def run(self):
        ydl_opts = {'outtmpl': self.path + '%(title)s.%(ext)s',
                    'format': 'best'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.id])
