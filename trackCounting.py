def gt(l, r): return l > r
def geqt(l, r): return l >= r
def lt(l, r): return l < r
def leqt(l, r): return l <= r
def eq(l, r): return l == r
def neq(l, r): return l != r

class trackCutSelector:
    def __init__(cuts):
        self.cuts = cuts

    def evaluate(tree, trackN):
        bool selected = True:
        for cut in self.cuts:
            value = tree.__getattr__(cut[0])[trackN]
            if not cut[1]( value, cut[2] ):
                return False
        return True

def trackMVASelector:
    def __init__(path, name, cut, trackVars):
        self.name = name
        self.path = path
        self.reader = ROOT.TMVA.Reader
        self.trackVars = { var: array("f", [0]) for var in trackVars }
        for name, var in trackVars.items():
            reader.AddVariable(name, var)
        self.reader.BookMVA(self.name, self.path)

    def sync(tree, trackN):
        for name, var in trackVars.items():
            var = tree.__getattr__(name)[trackN]

    def getValue(tree, trackN):
        self.sync(tree, trackN)
        return self.reader.EvaluateMVA(self.name)

    def evaluate(tree, trackN):
        return self.getValue(tree, trackN) > self.cut
