import numpy
from quakesnapshot import QuakeSnapshot
from PIL import Image


class DetectSamplePoints:
    snapshots = None
    pixel_tensor = None
    def __init__(self,snapshots):
        self.snapshots = snapshots
        self.pixel_tensor = self._get_pixel_tensor(snapshots)

    def _get_pixel_tensor(self,snapshots):
        image_arrays =[ numpy.asarray( ss.image ) for ss in snapshots]
        tensor = numpy.array(image_arrays)
        return tensor

    def _transparent_pixel(self,feature):
        return 255 in feature or 10 in feature or 11 in feature

    def cluster_pixels(self):
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

    def representative_points(self):
        for cluster in self.cluster_pixels():
            point = iter(cluster).next()
            yield point




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
    detection.cluster_pixels()
