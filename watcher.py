#coding: utf-8

from datetime import datetime, date, time, timedelta
import urllib

import os, os.path


import animation#


class QuakeSnapshot:
    path = None
    time = None
    image = None

    base_dir = "./snapshot"
    def __init__(self,time):
        self.time = time

        self.retrieve_image()

    def get_url(self):
        base_url = "http://realtime-earthquake-monitor.bosai.go.jp/realtimeimage/acmap_s/%s.acmap_s.gif"
        return base_url % self.time.strftime("%Y%m%d%H%M%S")

    def _get_savepath(self):
        savepath = os.path.join(self.base_dir, self.time.strftime("%Y%m%d%H%M%S") + ".gif")
        self.savepath = savepath
        return savepath


    def retrieve_image(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        savepath = self._get_savepath()
        if not os.path.exists(savepath):
            url = self.get_url()
            urllib.urlretrieve(url, savepath)
            print "retrieved ",savepath

        #if not self.image:
        #    savepath = self._get_savepath()
        #    self.image = Image.open( savepath )

def test():
    d = date(2013,11,10)

    t = time(7,38)
    start = datetime.combine(d,t)
    now = start

    t = time(7,39)
    end = datetime.combine(d,t)

    delta = timedelta(seconds=2)

    snapshots = []
    while now < end:
        snapshot = QuakeSnapshot(now)
        #print snapshot.get_url()
        #snapshot.retrieve_image()
        snapshots.append(snapshot)

        now += delta

    animation.write_animatedgif( snapshots, "hoge.gif" )


test() 


