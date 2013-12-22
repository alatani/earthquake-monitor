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


#test() 
class PrintScore:
    from earthquake_detection import EarthquakeDetector
    detector = EarthquakeDetector()

    def update(self,snapshot):
        self.detector.update(snapshot)
        print snapshot.timestr, "\t", self.detector.score


if __name__ == "__main__":
    #bootstrap

    print_score = PrintScore()
    observers = [print_score]

    from snapshotfetcher import PeriodicREMonitorFetcher

    watcher = PeriodicREMonitorFetcher(observers)
    watcher.startFetchingSnapshot()


