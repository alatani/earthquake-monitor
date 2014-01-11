from earthquakesnapshot import QuakeSnapshot

def test_animation():
    from datetime import date,time,timedelta
    import datetime
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

    import animation
    animation.write_animatedgif( snapshots, "hoge.gif" )



class DetectorLogger:
    def earhquake_emerged(self,snapshot): 
        print "::Emerged!"
    def earhquake_finished(self,snapshot): 
        print "::Finished!"

    def update_modelstate(self,data):
        snapshot,detector = data
        print snapshot.timestr, "\t", detector.score


class TwitterBot:
    def __init__(self):
        import twitterbot
        import datetime

        self.twitter = twitterbot.Twitter("alatani")
        self.lastupdate = datetime.datetime.fromtimestamp(0)

        self.interval = datetime.timedelta(seconds=60)

    def earhquake_emerged(self,snapshot): 
        import datetime

        now = datetime.datetime.now()
        if now > self.lastupdate + self.interval:
            print now
            timestr = now.strftime("%Y/%m/%d %H:%M:%S")
            message = "【自動】 ゆれ(?)  : " + timestr
            self.lastupdate = now
            self.twitter.post(message)


    def earhquake_finished(self,snapshot): 

        pass

    def update_modelstate(self,data):
        pass


class GifAnimationConstructor:
    def update_snapshot(self,snapshot):
        pass

    def earhquake_emerged(self,snapshot):
        pass
    def earhquake_finished(self,snapshot):
        pass

    def update_modelstate(self,data):
        snapshot,detector = data
        pass


if __name__ == "__main__":
    #bootstrap


    from earthquake_detection import TwoStage_EarthquakeDetector
    detector = TwoStage_EarthquakeDetector()

    from snapshotfetcher import PeriodicREMonitorFetcher
    watcher = PeriodicREMonitorFetcher()

    animator = GifAnimationConstructor()
    detectorlogger = DetectorLogger()
    twitterbot = TwitterBot()

    watcher.addObserver(detector)
    watcher.addObserver(animator)
    detector.addObserver(animator)
    detector.addObserver(detectorlogger)
    detector.addObserver(twitterbot)

    watcher.startFetchingSnapshot()


