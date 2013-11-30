#coding: utf-8

from datetime import datetime, date, time, timedelta
import urllib

import os, os.path


import animation#

#coding: utf-8
from quakesnapshot import QuakeSnapshot

def watch(tasks,interval_sec=2):
    lastupdate = datetime.datetime(2000,1,1)
    sec = datetime.timedelta(seconds=interval_sec)
    while True:
        now = datetime.datetime.now()
        dt = now-lastupdate
        if dt > sec:
            try:
                lastupdate = now
                snapshot = QuakeSnapshot(now)

                #apply snapshot to all tasks
                for task in tasks:
                    task(snapshot)

            except:
                print sys.exc_info()
                pass
        else:
            time.sleep(0.3)

def test():

def test_animation():
    d = date(2013,11,17)
    t = time(8,36)
    start = datetime.combine(d,t)
    now = start

    t = time(9,52)
    end = datetime.combine(d,t)

    delta = timedelta(seconds=2)

    snapshots = []
    while now < end:
        snapshot = QuakeSnapshot(now)
        print snapshot.get_url()
        snapshots.append(snapshot)
        now += delta

    animation.write_animatedgif( snapshots, "hoge.gif" )


test() 


