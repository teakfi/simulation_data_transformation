"""This module provides a transformation for cm to square image pixels and vice versa.

Used for muon-transportation data with muon locations in 2D for going in material and coming
out at the bottom of the material.
"""

import numpy as np
import warnings

class locationTransform():
    """This class is for providing the transform cm to image pixel and vice versa.

    Data for transformation is two 2-D matrixes of muon locations in 2D before and after their
    transportation through block of matter.
    
    Transform is based on origo shift and scaling.
    Origo is moved from (0,0) to center of the square image as (0,0) is left
    top corner in image formats.
    Scaling is also available.

    It can also be used to add random uniform shift in 2D.
    """
    
    """maxMove is the maximum absolute shift in any direction for random shift"""
    maxMove = 0
    """outputsize is the amount of pixels in one side of the square"""
    outputsize = 0
    """scale is scaling from cm to pixels"""
    scale = 1
    rng = np.random.default_rng()

    
    def __init__(self,opt):
        """Initialize transformer.

        Keyword arguments:
        outputsize -- the pixel count in one dimension for square image
        scale -- scaling factor (default=1), optional
        maxMove -- random move in cm (default=0), optional
        """
        """checking if the transformation values are usable"""
        maxMove = opt.maxMove
        outputsize = opt.pixels
        scale = opt.scaling
        
        if maxMove<0:
            raise ValueError("negative absolute maximum move")
        if not isinstance(outputsize,int):
            raise ValueError("outputsize must be integer")
        if outputsize<maxMove*scale:
            raise ValueError("outputsize in pixels than maximum allowed move multiplied by scaling")
        if scale <= 0:
            raise ValueError("negative or zero scaling not allowed")
            
        self.maxMove=maxMove
        self.outputsize=outputsize
        self.scale = scale

    def randomPosMove(self,inpos,outpos):
        """Random move for position.

        Same random move is used for input and output locations

        Keyword arguments:
        inpos -- 2-D array of (muon) locations (above the block of material)
        outpos -- 2-D array of (muon) locations (belove the block of material)

        Returns:
        inpos,oupos -- two 2-D arrays with values moved in both by same random move
        """
        """check the input shape for errors"""
        if np.shape(outpos)!=(2,):
            raise ValueError("the output position does not have x and y locations")
        if np.shape(inpos)!=(2,):
            raise ValueError("the input position does not have x and y locations")

        """generate random moves"""
        xmove, ymove = self.rng.uniform(-self.maxMove,self.maxMove,2)
        moves = np.array((xmove,ymove))

        """applying move"""
        positionout = np.array(outpos) + moves
        positionin = np.array(inpos) + moves
        
        return positionin,positionout
    
    def toPixel(self,inpos,outpos):
        """Convert cm-based value to pixels.

        Conversion: scaling + origo-transform + flooring and change to integer.

        Keyword arguments:
        inpos -- 2-D array of (muon) locations in cm (above the block of material)
        outpos -- 2-D array of (muon) locations in cm (belove the block of material)

        Returns:
        inpos,oupos -- two 2-D arrays corresponding ingoing and outgoing muons 
                                with same transform applied to both
        """

        """check the shape of input"""
        if np.shape(outpos)!=(2,):
            raise ValueError("the output position does not have x and y locations")
        if np.shape(inpos)!=(2,):
            raise ValueError("the input position does not have x and y locations")

        hitposition = np.array(inpos)
        position = np.array(outpos)

        """applying scaling"""
        position = position*self.scale
        hitposition = hitposition*self.scale

        """applying origo transform"""
        position = position+self.outputsize/2
        hitposition = hitposition+self.outputsize/2

        """flooring values to integers"""
        position = np.floor(position).astype(int)
        hitposition = np.floor(hitposition).astype(int)

        """enforcing size of the image and returning warnings when enforced"""
        if position[0]<0:
            position[0]=0
            warnings.warn("x pixel location less than 0, value set to 0",RuntimeWarning)
        if position[0]>=self.outputsize:
            position[0]=self.outputsize-1
            warnings.warn("x pixel location higher than outputsize, value set to max",RuntimeWarning)
        if position[1]<0:
            position[1]=0
            warnings.warn("y pixel location less than 0, value set to 0",RuntimeWarning)
        if position[1]>=self.outputsize:
            position[1]=self.outputsize-1
            warnings.warn("y pixel location higher than outputsize, value set to max",RuntimeWarning)

        return hitposition,position

    def tocm(self,inpixel,outpixel):
        """Convert pixels to cm-based.

        Conversion: origo-transform + reverse scaling.

        Keyword arguments:
        inpixel -- 2-D array of (muon) locations in pixels (above the block of material)
        outpixel -- 2-D array of (muon) locations in pixels (belove the block of material)

        Returns:
        inpos,oupos -- two 2-D arrays with same transform applied to both corresponding
                            ingoing and outgoing muons
        """
        """check if input is in correct format"""
        if np.shape(inpixel)!=(2,):
            raise ValueError("the input position does not have x and y locations")
        if np.shape(outpixel)!=(2,):
            raise ValueError("the output position does not have x and y locations")
        if min(inpixel)<0 or max(inpixel)>self.outputsize:
            raise ValueError("the input position is outside of the bounds")
        if min(outpixel)<0 or max(outpixel)>self.outputsize:
            raise ValueError("the output position is outside of the bounds")

        """move origo from center of the image to 0,0"""
        inpos = np.array(inpixel)-self.outputsize/2
        outpos = np.array(outpixel)-self.outputsize/2

        """remove scaling"""
        inpos = inpos/self.scale
        outpos = outpos/self.scale
        
        return inpos,outpos