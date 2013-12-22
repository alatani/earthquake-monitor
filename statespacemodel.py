import math

class LocalLevelModel:
    mean = 0
    variance = 0
    score = 0
    def __init__(self,variance,eta=None,epsilon=None):
        self.variance = variance
        self.eta = eta
        self.epsilon = epsilon


    def _update(self,y,epsilon,eta):
        a,P = self.mean,self.variance

        v = y - a
        F = P + epsilon
        K = P / F

        a = a + K*v
        P = P*(1.0 - K) + eta

        self.mean, self.variance = a,P
        return a,P

    def update(self,y,epsilon=None,eta=None):
        epsilon = self.epsilon or epsilon
        eta = self.eta or eta

        self.score = self.score(y)

        mean,variance = self._update(y,epsilon,eta)
        return mean,variance


    def probability(self,x):
        mu = self.mean
        var = self.variance
        diff = x-mu
        inner =  - 0.5 * diff * diff / var
        return math.exp(inner) / math.sqrt( 2 * math.pi * var )

    def score(self,x):
        mu = self.mean
        var = self.variance
        diff = x-mu

        ninner = 0.5 * diff * diff / var
        return 0.5 * ( math.log( var ) + math.log( 2 * math.pi ) ) + ninner

def test(xs,p=2500,ep=0.05,et=2500):
    model = LocalLevelModel(p,ep,et)
    for x in xs:
        yield model.score(x)
        model.filter(x)


