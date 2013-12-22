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
    from earthquake_detection import TwoStage_EarthquakeDetector
    detector = TwoStage_EarthquakeDetector()

    def update_snapshot(self,snapshot):
        self.detector.update(snapshot)
        print snapshot.timestr, "\t", self.detector.score


class GifAnimationConstructor:
    def update_snapshot(self,snapshot):
        pass

    def earhquake_emerge(snapshot):
        pass
    def earhquake_finish(snapshot):
        pass


if __name__ == "__main__":
    #bootstrap

    print_score = PrintScore()

    from earthquake_detection import TwoStage_EarthquakeDetector
    detector = TwoStage_EarthquakeDetector()


    from snapshotfetcher import PeriodicREMonitorFetcher

    watcher = PeriodicREMonitorFetcher(snapshot_observers)
    watcher.addObserver(print_score)
    watcher.addObserver(detector)

    watcher.startFetchingSnapshot()


