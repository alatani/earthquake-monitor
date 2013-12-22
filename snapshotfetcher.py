#coding: utf-8

import datetime

import animation#

#coding: utf-8
from earthquakesnapshot import QuakeSnapshot

#observer pattern
class SnapshotSignal:
    observers = set()

    def __init__(self,observers=None):
      for obs in observers:
        self.observers.add(obs)

    def addObserver(self,observer):
        self.add(observer)

    def notifySnapshot(self,snapshot):
        for obsrever in self.observers:
            observer.update_snapshot(snapshot)



class PeriodicREMonitorFetcher():
    signal = SnapshotSignal()
    
    def startFetchingSnapshot(self):
        self.watch()

    def addObserver(self,obs):
        self.signal.addObserver(obs)

    def watch(interval_sec=2):
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
                    #notify snapshot to all observers
                    self.signal.notifySnapshot(snapshot)
                except IOError as e:
                    print e.message
            else:
                import time
                time.sleep(0.2)





