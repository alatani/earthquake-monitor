import num
from PIL import Image

from detect_sample_points import DetectSamplePoints


class DescreteAnomaryDetection:
    smoothing = 10

    class SingleVariate:
        counts = {}
        smoothing = 10
        #forgetting_term = 3600 / 2 # 1hour
        def __init__(self):
            pass

        def update(self,value):
            c = self.counts.get(value, self.smoothing)
            self[value] = c + 1

        def score(self,value):
            total = 0
            for k,v in self.counts.iterelems():
                total += v
            count = self.counts.get(value,self.smoothing)

            return  - log( count ) + log( total )  #分母の計算にバグがある。


    def __init__(self, dimension):
        pass

    def __call__(self,feature):


class EarthquakeDetector:

    representative_points = None

    def __init__(self):
        self.representative_points = DetectSamplePoints().representative_points()

    def _get_quaking_colors(self,snapshot)
        arr = numpy.asarray(snapshot)
        feature = [ arr[x,y] for x,y in self.representative_points]
        return feature

    def __call__(self,snapshot):
        image = snapshot.image

