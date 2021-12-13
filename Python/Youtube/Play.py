import pafy


class Play():
    def __init__(self, odtwarzacz, kolejkaOdt, rozmiarKolejki, czasTrwania,
                 terazOdt, Instance, pasekProgresu, id, title, time, czyPom,
                 parent=None):
        self.odtwarzacz = odtwarzacz
        self.kolejkaOdt = kolejkaOdt
        self.rozmiarKolejki = rozmiarKolejki
        self.czasTrwania = czasTrwania
        self.terazOdt = terazOdt
        self.Instance = Instance
        self.pasekProgresu = pasekProgresu
        self.id = id
        self.title = title
        self.time = time
        self.czyPom = czyPom

        self._pl()

    def _pl(self):
        if self.odtwarzacz.is_playing() and self.czyPom == 0:
            self.kolejkaOdt.append(self.id)
            self.kolejkaOdt.append(self.title)
            self.kolejkaOdt.append(self.time)
            self.rozmiarKolejki.setText("W kolejce: "
                                        + str(int(len(self.kolejkaOdt)/3)))
        else:
            self.czasTrwania = self.time
            self.terazOdt.setText("Teraz odtwarzane: " + self.title)
            video = pafy.new(self.id)
            best = video.getbest()
            playurl = best.url
            Media = self.Instance.media_new(playurl)
            Media.get_mrl()
            self.odtwarzacz.set_media(Media)
            self.odtwarzacz.play()
            self.pasekProgresu.setValue(0)
