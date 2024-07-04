"""Data reader"""

import glob
import numpy as np
import re

"""code for first data format - ff1 in code

filename construct:
prefix_{a}{b}x_fort.60, where a codes the incoming muon energy and b is run number
a values: 1 -> 1 GeV, 2 -> 2 GeV, 3 -> 4 GeV, 4 -> 8 GeV

the actual data is in comma separated file in following format
event number, energy after block [GeV], xpos [cm], ypos [cm], zpos [cm]

Starting location for each muon is (0,0,50) cm and muons are going all towards (0,0,0) and the block ends at (0,0,-100) thus the muons are trying to go through 100cm block
"""
class DataReader():
    
    def ff1_filename_E_pairs(self, opt):
        pairs = []
        string_a_energy = {'1':1,'2':2,'3':4,'4':8}
        datadir = str(opt.datadir) + '/*'
        files = glob.glob(datadir)
        for file in files:
            match = re.match(r"[\\\/\w]*_([\d])[\d]{3}_fort.60$",file)
            if match:
                pairs.append((file,string_a_energy[match.group(1)]))
        return pairs

    def ff1_read_file(self, file, energy):
        events = np.loadtxt(file,usecols=(1,2,3,4))
        N = len(events)
        events = np.c_[events,energy*np.ones(N)] # adding energy information to event
        return events

    def ff1_read_data(self, opt):
        files = self.ff1_filename_E_pairs(opt)
        muons = [self.ff1_read_file(f[0],f[1]) for f in files]
        muons = np.concatenate(muons)
        if opt.rnd_order:
            np.random.shuffle(muons)
        return muons

    def __init__(self):
        self.data_read = False

    def read_data(self, opt):
        muons = self.ff1_read_data(opt)
        self.data_read = True
        return muons