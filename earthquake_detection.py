import numpy
from PIL import Image

from detect_sample_points import DetectSamplePoints


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



class EarthquakeDetector:
    representative_points = None

    def __init__(self):
        self.representative_points = list(DetectSamplePoints().representative_points())
        dimension = len(self.representative_points)
        self.detector = IidMultinomialsAnomaryDetection(dimension)

    def _get_quaking_colors(self,image):
        arr = numpy.asarray(image)
        feature = [ arr[x,y] for x,y in self.representative_points]
        return feature

    def __call__(self,snapshot):
        image = snapshot.image
        feature = self._get_quaking_colors(image)
        self.detector.update(feature)


