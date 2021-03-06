import ROOT as r
from supy import analysisStep
import supy
from math import fabs, pi

# for all the deltas, the first value is the reference one, so
# delta = val_i+1 - val_1
# deltaFrac = (val_i+1 - val_1)/val_1

MeV2GeV = 1.0e-3
def phi_mpi_pi(value) :
    "same as r.Math.GenVector.VectorUtil.Phi_mpi_pi (for some reason cannot import it...)"
    pi = r.TMath.Pi()
    if value > pi and value <= pi:
        return value
    while value <= -pi: value = value+2.*pi
    while value >  +pi: value = value-2.*pi
    return value
class attribute(analysisStep) :
    def __init__(self, attrName='', coll='', nTh=None, nX=100,xLo=-5.0,xUp=5.0,title="",label='') :
        for item in ['attrName', 'coll', 'nTh', 'nX','xLo','xUp','title','label'] : setattr(self,item,eval(item))
        self.hName = '%s_%s%s'%(coll,attrName,label)
    def uponAcceptance(self, eventVars) :
        coll = eventVars[self.coll]
        for i, elem in enumerate(coll) :
            if self.nTh!=None and self.nTh!=i : continue
            self.book.fill(getattr(elem,self.attrName), self.hName, self.nX, self.xLo, self.xUp, title=self.title)
class deltaEta(analysisStep) :
    def __init__(self, matchCollPair='',N=100,low=-0.5,up=+0.5,title="#Delta #eta") :
        for item in ['matchCollPair','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEta%s'%matchCollPair
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(elem2.eta - elem1.eta, self.hName, self.N, self.low, self.up, title=self.title)
class deltaPhi(analysisStep) :
    def __init__(self, matchCollPair='',N=100,low=-0.5,up=+0.5,title="#Delta #phi") :
        for item in ['matchCollPair','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaPhi%s'%matchCollPair
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(elem2.phi - elem1.phi, self.hName, self.N, self.low, self.up, title=self.title)
class deltaR(analysisStep) :
    def __init__(self, matchCollPair='',N=100,low=0.0,up=0.5,title="#Delta R") :
        for item in ['matchCollPair','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaR%s'%matchCollPair
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            j1lv = supy.utils.root.LorentzV(elem1.et, elem1.eta, elem1.phi, 0.)
            j2lv = supy.utils.root.LorentzV(elem2.et, elem2.eta, elem2.phi, 0.)
            self.book.fill(r.Math.VectorUtil.DeltaR(j1lv, j2lv), self.hName, self.N, self.low, self.up, title=self.title)
class deltaEt(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None,N=100,low=-50.0,up=50.0,title="#Delta E_{T}") :
        for item in ['matchCollPair','nTh', 'N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEt%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if self.nTh :
            self.hName += "_%dthJet"%self.nTh
            self.title += "(%dth jet)"%self.nTh
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i, pair in enumerate(matchCollPair) :
            if self.nTh and self.nTh!=i : continue
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(MeV2GeV*(elem2.et - elem1.et), self.hName, self.N, self.low, self.up, title=self.title)
class deltaEtFrac(analysisStep) :
    # todo: merge it with deltaEt
    def __init__(self, matchCollPair='',nTh=None,N=100,low=-2.0,up=2.0,title="#Delta E_{T}/E_{T}") :
        for item in ['matchCollPair', 'nTh', 'N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtFrac%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if self.nTh :
            self.hName += "_%dthJet"%self.nTh
            self.title += "(%dth jet)"%self.nTh
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i, pair in enumerate(matchCollPair) :
            if self.nTh and self.nTh!=i : continue
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            et1, et2 = elem1.et, elem2.et
            if et1 :
                self.book.fill((et2-et1)/et1, self.hName, self.N, self.low, self.up, title=self.title)

class etaPhiMap(analysisStep) :
    def __init__(self, coll='', nTh=None, nX=100,xLo=-5.0,xUp=5.0,nY=100,yLo=-pi,yUp=+pi,title="") :
        for item in ['coll','nTh','nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = "etaPhiMap%s%s"%(coll, "_%dthJet"%nTh if nTh else "")
    def uponAcceptance(self, eventVars) :
        coll = eventVars[self.coll]
        for i,elem in enumerate(coll) :
            if self.nTh and not self.nTh==i : continue
            self.book.fill((elem.eta, phi_mpi_pi(elem.phi)),
                           "%s_eta_phi"%self.coll,
                           (self.nX, self.nY), (self.xLo, self.yLo), (self.xUp, self.yUp),
                           title="%s;#eta;#phi"%self.title)

class deltaEtaVsEtaMap(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, nX=100,xLo=-5.0,xUp=5.0,nY=100,yLo=-0.5,yUp=+0.5,title="") :
        for item in ['matchCollPair','nTh','nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtaVsEtaMap%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if not self.title : self.title = "%s;#eta; #Delta #eta"%self.hName
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            # the first collection is the one best precision (reference)
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 : continue
            if not elem2 : continue
            self.book.fill((elem1.eta, elem1.eta-elem2.eta),
                           self.hName,
                           (self.nX, self.nY),
                           (self.xLo, self.yLo),
                           (self.xUp, self.yUp),
                           title=self.title)
class deltaEtFracVsEtaMap(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, nX=100,xLo=-5.0,xUp=5.0,nY=100,yLo=-5.0,yUp=+5.0,title="") :
        for item in ['matchCollPair', 'nTh', 'nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtFracVsEtFracMap%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if not self.title : self.title = "%s;#eta; #Delta E_{T}/E_{T}"%self.hName
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            # the first collection is the one best precision (reference)
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 : continue
            if not elem2 : continue
            etRef = elem1.et
            if not etRef : continue
            self.book.fill((elem1.eta, (elem2.et - etRef)/etRef),
                           self.hName,
                           (self.nX, self.nY),
                           (self.xLo, self.yLo),
                           (self.xUp, self.yUp),
                           title="%s;#eta; #Delta E_{T}/E_{T}"%self.hName if not self.title else self.title)
class deltaEtFracVsEtMap(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, nX=100,xLo=0.0,xUp=200.0,nY=100,yLo=-2.0,yUp=+2.0,title="") :
        for item in ['matchCollPair', 'nTh', 'nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtFracVsEtFracMap%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if not self.title : self.title = "%s;#eta; #Delta E_{T}/E_{T}"%self.hName
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i, (elem1, elem2) in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            if not elem1 or not elem2: continue
            etRef = elem1.et
            if not etRef : continue
            self.book.fill((etRef*MeV2GeV, (elem2.et - etRef)/etRef),
                           self.hName,
                           (self.nX, self.nY),
                           (self.xLo, self.yLo),
                           (self.xUp, self.yUp),
                           title="%s;E_{T, ref}; #Delta E_{T}/E_{T}"%self.hName if not self.title else self.title)

class deltaEtFracVsMinDrMap(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, nX=100,xLo=0.,xUp=5.0,nY=100,yLo=-5.0,yUp=+5.0,title="") :
        for item in ['matchCollPair', 'nTh', 'nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtFracVsMinDrMap%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if not self.title : self.title = "#Delta(E_{t})/E_{T} %s;#min #Delta R; #Delta E_{T}/E_{T}"%("" if not nTh else "%dth jet"%(nTh+1))
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            # the first collection is the one with minDr
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 : continue
            if not elem2 : continue
            etRef = elem1.et
            self.book.fill((elem1.minDr, (elem2.et - etRef)/etRef),
                           self.hName,
                           (self.nX, self.nY),
                           (self.xLo, self.yLo),
                           (self.xUp, self.yUp),
                           title=self.title)

class matchingEffVsEt(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, N=100,low=0.0,up=100.0,title="matching efficiency vs. E_{T}") :
        for item in ['matchCollPair','nTh','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'matchingEffVsEt%s%s'%(matchCollPair,"_%dthJet"%nTh if nTh else "")
        self.numTitle = 'num_%s'%self.hName
        self.denTitle = 'den_%s'%self.hName
        self.effTitle = 'eff_%s'%self.hName

    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            elem1 = pair[0]
            elem2 = pair[1]
            # the first collection is the one with higher eff (denominator)
            if not elem1 : continue
            self.book.fill(MeV2GeV*elem1.et, self.denTitle, self.N, self.low, self.up, title="denominator: %s;E_{T};jets"%self.denTitle)
            if not elem2 : continue
            self.book.fill(MeV2GeV*elem1.et, self.numTitle, self.N, self.low, self.up, title="numerator: %s;E_{T};jets"%self.numTitle)
    def mergeFunc(self, products) :
        num = r.gDirectory.Get(self.numTitle)
        den = r.gDirectory.Get(self.denTitle)
        if not num and den : return
        eff = num.Clone(self.effTitle)
        eff.SetTitle(self.title)
        eff.Divide(num,den,1,1,"B")
        for bin in [0,self.N+1] :
            eff.SetBinContent(bin,0)
            eff.SetBinError(bin,0)
        eff.Write()

class turnOnJet(analysisStep) :
    """Turn on for a multijet trigger.
    You need to specify: the jet collection, the trigger, and the Nth jet whose E_T is to be used on the x-axis.
    You can specify the following parameters:
    (1) min/max eta of the Nth jet (by default any eta is accepted)
    (2) min/max deltaR: requirement for the Nth jet, or for any jet if drAnyJet=True)
    Note that in case (2) the jets must have a minDr attribute.
    """
    def __init__(self, jetColl='', trigger='', passedTriggers='PassedTriggers', nTh=None,
                 emulated=False,
                 drMin=None, drMax=None,
                 drAnyJet=None,
                 etaMin=None, etaMax=None,
                 N=60,low=0.0,up=120.0,title='') :
        requiredPars = ['jetColl', 'trigger', 'passedTriggers', 'nTh', 'emulated']
        filterPars = ['drMin', 'drMax', 'etaMin', 'etaMax']
        otherPars = ['drAnyJet']
        histPars = ['N','low','up','title']
        for item in requiredPars + filterPars + otherPars + histPars : setattr(self,item,eval(item))
        self.hName = ('turnOn%s%s'%(trigger, jetColl)
                      +("_%dthJet"%nTh if nTh else "")
                      +('_'.join(['']+['%s_%.1f'%(k,v) for k,v in
                                       zip(filterPars,
                                           [getattr(self,x) if hasattr(self,x) else None for x in filterPars]) if v])))
        self.numName = 'num_%s'%self.hName
        self.denName = 'den_%s'%self.hName
        self.effName = 'eff_%s'%self.hName
        self.moreName = trigger
        if not self.title :
            reqLabel = ', '.join(['%s=%.1f'%(k,v) for k,v in zip(filterPars, [getattr(self,x) if hasattr(self,x) else None for x in filterPars]) if v])
            self.title = "%s efficiency %s; %sth jet E_{T} [GeV];eff"%(trigger, "" if not reqLabel else "(%s)"%reqLabel, nTh+1)
    def uponAcceptance(self, eventVars) :
        jetColl = eventVars[self.jetColl]
        if self.nTh >= len(jetColl) : return
        jet = jetColl[self.nTh]
        if self.drAnyJet and (self.drMin or self.drMax):
            if any((self.drMin and j.minDr and j.minDr < self.drMin)
                   or
                   (self.drMax and j.minDr and j.minDr > self.drMax)
                   for j in jetColl) : return
        else :
            if self.drMin and jet.minDr and jet.minDr < self.drMin : return
            if self.drMax and jet.minDr and jet.minDr > self.drMax : return
        if self.etaMin and fabs(jet.eta) < self.etaMin : return
        if self.etaMax and fabs(jet.eta) > self.etaMax : return
        jetEt = jet.et*MeV2GeV
        self.book.fill(jetEt, self.denName, self.N, self.low, self.up, title="denominator: %s;E_{T};jets"%self.denName)
        if self.trigger in eventVars[self.passedTriggers] \
               or \
               self.emulated and eventVars[self.trigger] :
            self.book.fill(jetEt, self.numName, self.N, self.low, self.up, title="numerator: %s;E_{T};jets"%self.numName)
    def mergeFunc(self, products) :
        num = r.gDirectory.Get(self.numName)
        den = r.gDirectory.Get(self.denName)
        if not num : return
        if not den : return
        eff = num.Clone(self.effName)
        if not eff : return
        eff.SetTitle(self.title)
        eff.Divide(num,den,1,1,"B")
        for bin in [0,self.N+1] :
            eff.SetBinContent(bin,0)
            eff.SetBinError(bin,0)
        eff.Write()

class value2d(analysisStep) :
    def __init__(self, xvar, xn, xmin, xmax, yvar, yn, ymin, ymax, title="",label='') :
        for item in ['xvar', 'xn', 'xmin', 'xmax', 'yvar', 'yn', 'ymin', 'ymax', 'title', 'label'] : setattr(self, item, eval(item))
        self.moreName = "%s:%s"%(xvar, yvar)
        self.histoName = "%s_vs_%s%s"%(xvar, yvar,label)
        if not self.title : self.title = "%s vs. %s; %s; %s"%(yvar, xvar, xvar, yvar)
    def uponAcceptance(self,eventVars) :
        vx, vy = eventVars[self.xvar], eventVars[self.yvar]
        if not vx or not vy : return
        self.book.fill((vx, vy),
                       self.histoName,
                       (self.xn, self.yn),
                       (self.xmin, self.ymin),
                       (self.xmax, self.ymax),
                       title=self.title)
