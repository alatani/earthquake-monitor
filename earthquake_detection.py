import numpy
from PIL import Image

from detect_sample_points import DetectSamplePoints
from statespacemodel import LocalLevelModel


class MultinomialProcess:
    counts = {}
    smoothing = 10
    categories = None

    def __init__(self,categories):
        self.categories = categories
        pass

    def update(self,value):
        c = self.counts.get(value, self.smoothing)
        self.counts[value] = c + 1

    def negative_log_likelihood(self,value):
        import math
        total = 0
        for k,v in self.counts.iteritems():
            total += v

        total += (self.categories - len(self.counts)) * self.smoothing 
        count = self.counts.get(value,self.smoothing)
        return  - math.log( count ) + math.log( total )


class IidMultinomialsAnomaryDetection:
    smoothing = 10
    score = 0
    detected = False

    def __init__(self, dimension, categories = 9):
        self.multinomial_processes = \
            [ MultinomialProcess(categories) for i in xrange(dimension)]
        pass

    def update(self,feature):
        for mp,v in zip(self.multinomial_processes,feature):
            mp.update(v)
        total_negative_log_liklihood = sum(
            p.negative_log_likelihood(v) for p,v in zip(self.multinomial_processes, feature) 
        )

        self.score = total_negative_log_liklihood


#observer pattern
class EarthquakeSignal:
    earthquake_observers = set()

    def addObserver(self,observer):
        self.earthquake_observers.add(observer)

    def notifyEarthquakeEmergence(self,snapshot):
        for obs in self.earthquake_observers:
            obs.earhquake_emerge(snapshot)

    def notifyEarthquakeFinish(self,snapshot):
        for obs in self.earthquake_observers:
            obs.earhquake_finish(snapshot)

    def notifyModelState(self,data):
        for obs in self.earthquake_observers:
            obs.update_modelstate(data)



class TwoStage_EarthquakeDetector():
    signal = EarthquakeSignal()

    representative_points = None
    local_level_model = None

    threshold = 3500
    score = 0
    previous_score = 0

    def __init__(self):
        self.representative_points = list(DetectSamplePoints().representative_points())
        dimension = len(self.representative_points)
        self.detector = IidMultinomialsAnomaryDetection(dimension)

        p=2500
        ep=0.05
        et=2500
        self.local_level_model = LocalLevelModel(p,ep,et)

    def _get_quaking_colors(self,image):
        arr = numpy.asarray(image)
        feature = [ arr[x,y] for x,y in self.representative_points]
        return feature

    def update_snapshot(self,snapshot):
        image = snapshot.image
        feature = self._get_quaking_colors(image)

        self.detector.update(feature)
        multinomial_score = self.detector.score

        self.local_level_model.update(multinomial_score)
        score = self.local_level_model.score

        if score > self.threshold and self.previous_score <= self.threshold:
            #earthquake!
            self.signal.notifyEarthquakeEmergence(snapshot)

        if score <= self.threshold and self.previous_score > self.threshold:
            self.signal.notifyEarthquakeFinish(snapshot)

        self.previous_score = self.score
        self.score = score

        self.signal.notifyModelState((snapshot,self))

    def addObserver(self,obs):
        self.signal.addObserver(obs)



