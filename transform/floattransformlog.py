""" This file is for transforming muon energy in GeVs to range of 0..1 as 32bit float with log transform.

Transformation is based on assumption that 2 TeV is the maximum muon energy.

"""
import numpy as np

class FloatTransform():
    """ This class provides a transformation of muon energy to pixel value in 32bit float.

    Log(E+1) = L x , x = pixel value from 0 to 1
    Log(maxE + 1) = L
    """
    maxE = 2e12
    L = np.log(maxE+1)

    def __init__(self, opt):
        """Initilize momentum transformer

        Keyword arguments:
        maxE -- the maximum muon energy in electron volts, must be larger than 0
        """
        self.maxE = opt.max_E
        if self.maxE <= 0:
            raise ValueError("Maximum muon energy has to be larger than 0 eV")
        
        self.L = np.log(self.maxE+1)

    def to_pixel_value(self,E):
        """Convert energy to float in range of 0-1.

        Keyword arguments:
        E -- the muon energy in eV, minimum 0, maximum 2 TeV

        Raises errors if value is not in the range.
        """

        if E<0:
            raise ValueError("negative muon energy")

        if E>self.maxE:
            raise ValueError("too large energy")

        output = np.log(E+1)/self.L

        return output


    def to_energy_value(self,pixelE):
        """Convert energy from pixel value to eV.

    

        Keyword arguments:
        pixelE -- the muon energy as pixel float in range 0-1

        Raises errors if value is not in the range.
        """
        if pixelE<0:
            raise ValueError("negative muon energy")
        if pixelE>1:
            raise ValueError("Muon energy above 2 TeV")

        output = np.exp(pixelE*self.L)-1

        return output
