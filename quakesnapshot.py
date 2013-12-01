import numpy
import os, os.path
from PIL import Image
import urllib

class QuakeSnapshot:
    path = None
    time = None
    image = None

    base_dir = "./snapshot"
    def __init__(self,time):
        self.time = time

        self._retrieve_image()

    def get_url(self):
        base_url = "http://realtime-earthquake-monitor.bosai.go.jp/realtimeimage/acmap_s/%s.acmap_s.gif"
        return base_url % self.time.strftime("%Y%m%d%H%M%S")

    def _get_savepath(self):
        savepath = os.path.join(self.base_dir, self.time.strftime("%Y%m%d%H%M%S") + ".gif")
        self.savepath = savepath
        return savepath


    def _retrieve_image(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        savepath = self._get_savepath()
        if not os.path.exists(savepath):
            url = self.get_url()
            urllib.urlretrieve(url, savepath)
            print "retrieved ",savepath

        if not self.image:
            savepath = self._get_savepath()
            self.image = Image.open( savepath )
