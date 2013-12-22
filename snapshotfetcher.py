#coding: utf-8

import datetime

import animation#

#coding: utf-8
from earthquakesnapshot import QuakeSnapshot

#observer pattern
class SnapshotWatcher:
    observers = []

    def __init__(self,observers=None):
        self.observers = observers 

    def addObservers(self,observer):
        self.append(observer)

    def notifyObservers(self,snapshot):
        for obsrever in self.observers:
            observer.update(snapshot)

    def startWatchingSnapshot(self):
        pass

class PeriodicREMonitorWatcher(SnapshotWatcher):

    def startWatchingSnapshot(self):
        self.watch()

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
                    self.notifyObservers(snapshot)
                except IOError as e:
                    print e.message
            else:
                import time
                time.sleep(0.2)




