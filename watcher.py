#coding: utf-8

import datetime
import urllib
import os, os.path
import sys

import animation#

#coding: utf-8
from quakesnapshot import QuakeSnapshot

def watch(tasks,interval_sec=2):
    lastupdate = datetime.datetime.combine(datetime.date(2000,1,1),datetime.time(0,0))

    sec = datetime.timedelta(seconds=interval_sec)
    while True:
        now = datetime.datetime.now()
        dt = now-lastupdate
        if dt > sec:
            #try:
            lastupdate = now
            try:
                snapshot = QuakeSnapshot(now)

                #apply snapshot to all tasks
                for task in tasks:
                    task(snapshot)
            except IOError as e:
                print e.message


            #except:
            #    print sys.exc_info()
            #    pass
        else:
            import time
            time.sleep(0.2)

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


#test() 

from earthquake_detection import EarthquakeDetector
detector = EarthquakeDetector()
def print_score(snapshot):
    detector(snapshot)
    print snapshot.timestr, "\t", detector.detector.score

tasks = [print_score]
watch(tasks)


