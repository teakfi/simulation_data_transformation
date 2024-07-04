"""Apply required transformations to muon data"""

from .floattransformlog import FloatTransform as ftl
from .pixelcmtransform import locationTransform as pt
import numpy as np
import warnings

class Transform():

    def __init__(self, opt):
        self.pixelize = pt(opt)
        self.energyscaling = ftl(opt)
        self.eventsize = opt.max_event_size
        self.randomsize = opt.random_size

    def Eventize(self, muons):
        """Divide muons to events"""

        count = 0
        events = []
        event = []
        hits_in_event=self.eventsize
        if self.randomsize:
            hits_in_event = np.random.randint(1,self.eventsize)

        for data in muons:
            count += 1
            event.append(data)
            if count==hits_in_event:
                events.append(event)
                event = []
                count = 0
                if self.randomsize:
                    hits_in_event = np.random.randint(1,self.eventsize)
        
        if event:
            events.append(event)

        return events

    def PixelizeEvent(self, event):
        """pixelize muon data"""

        shiftedmuons = []
        for muon in event:
            if muon[3] == -50:
                posin,posout = self.pixelize.randomPosMove((0,0),(muon[1],muon[2]))
                try:
                    posin,posout = self.pixelize.toPixel(posin,posout)
                except RuntimeWarning:
                    muonevent = [0,posin[0],posin[1],posout[0],posout[1],muon[4]]
                else:
                    muonevent = [muon[0],posin[0],posin[1],posout[0],posout[1],muon[4]]

            else:
                muonevent = [0,posin[0],posin[1],posout[0],posout[1],muon[4]]

            shiftedmuons.append(muonevent)

        return shiftedmuons

    def EnergyTransformEvent(self, event):
        """Do energy transformation for normalizing values between 0 and 1"""

        floatevent = []
        for muon in event:
            intEin = self.energyscaling.to_pixel_value(muon[5]*1e9) # GeV to eV 
            intEout = self.energyscaling.to_pixel_value(muon[0]*1e9)
            transformed = [intEout,muon[3],muon[4],muon[1],muon[2],intEin]
            # data order now: muon E after, x out pixel, y out pixel, x in, y in, E in
            floatevent.append(transformed)

        return floatevent
    
    def Run(self, muons):
        events = self.Eventize(muons)

        pixeled = []

        for event in events:
            shiftedevent = self.PixelizeEvent(event)
            pixeled.append(shiftedevent)

        del events

        fullytransformed = []

        for event in pixeled:
            transformed = self.EnergyTransformEvent(event)
            fullytransformed.append(transformed)
        
        return fullytransformed
    
