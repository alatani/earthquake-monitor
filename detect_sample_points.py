import numpy
from quakesnapshot import QuakeSnapshot
from PIL import Image

try:
    import cPickle as pickle
except:
    import pickle


class DetectSamplePoints:
    snapshots = None
    pixel_tensor = None
    def __init__(self,snapshots=None):
        self.snapshots = snapshots
        if snapshots:
            self.pixel_tensor = self._get_pixel_tensor(snapshots)

    def _get_pixel_tensor(self,snapshots):
        image_arrays =[ numpy.asarray( ss.image ) for ss in snapshots]
        tensor = numpy.array(image_arrays)
        return tensor

    def _transparent_pixel(self,feature):
        return 255 in feature or 10 in feature or 11 in feature

    def _cluster_pixels(self):
        tensor = self.pixel_tensor
        duration,width,height = tensor.shape

        toprocess = set()
        for x,y in ( (x,y) for x in xrange(width) for y in xrange(height) ):
            if y<251 and x<41:
                continue
            feature = tensor[:,x,y]
            if not self._transparent_pixel(feature):
                toprocess.add((x,y))
        print "successfully created the set of pixels to process with size", len(toprocess)

        def is_equivalant(f1,f2):
            diff = f1 - f2
            return abs(diff).sum() == 0

        def scan_equivalent_pixels(point,processed):
            equivalents = set()
            near = lambda p1,p2: abs(p1[0]-p2[0])<3 and abs(p1[1]-p2[1])<3

            feature = tensor[:,point[0],point[1]]
            for x,y in toprocess:
                if near(point,(x,y)) and not (x,y) in processed:
                    if is_equivalant(tensor[:,x,y],feature):
                        equivalents.add((x,y))
                        processed.add((x,y))
            return equivalents,processed

        processed = set()
        for x,y in toprocess:
            if (x,y) in processed:
                continue
            feature = tensor[:,x,y]
            print (x,y)
            equivalents,processed = scan_equivalent_pixels((x,y),processed)
            yield equivalents

    CACHE_FILE = "representative_points.dat"
    def representative_points(self,snapshots=None):
        if not snapshots:
            with open(self.CACHE_FILE,"rb") as f:
                points = pickle.load(f)
                for point in points:
                    yield point
        else:
            points = []
            for cluster in self._cluster_pixels():
                point = iter(cluster).next()
                yield point
                points.append(point)
            with open(self.CACHE_FILE,"wb") as f:
                pickle.dump(points, f)




def snapshots():
    from datetime import datetime, date, time, timedelta
    d = date(2013,11,17)
    t = time(8,36)
    start = datetime.combine(d,t)
    now = start

    t = time(8,38)
    #t = time(9,52)
    end = datetime.combine(d,t)

    delta = timedelta(seconds=2)

    snapshots = []
    while now < end:
        snapshot = QuakeSnapshot(now)
        snapshots.append(snapshot)
        now += delta
    return snapshots


if __name__=="__main__":
    snapshots = snapshots()
    detection = DetectSamplePoints(snapshots)
    points = detection.representative_points()
    print list(points)
