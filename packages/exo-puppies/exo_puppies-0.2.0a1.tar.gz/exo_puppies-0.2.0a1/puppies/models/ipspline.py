import sys
import os
import numpy as np

#topdir = os.path.realpath(os.path.dirname(__file__) + "/../..")
#sys.path.append(topdir + "/puppies/lib")
#import _bilinint as bli


__all__ = ["ipspline"]

class ipspline():
  def __init__(self):
    self.name = "ipspline"
    self.type = "pixmap"
    self.pnames = ['yknots', 'xknots']
    self.npars = len(self.pnames)
    self.params = np.zeros(self.npars)
    self.pmin   = np.tile(-np.inf, self.npars)
    self.pmax   = np.tile( np.inf, self.npars)
    self.pstep  = np.zeros(self.npars)

  def __call__(self, params, x):
    return self.eval(params, x)


  def eval(self, params, x):
    flux, model = x
    args = (flux, model, self.knotpts, self.knotsize, self.kploc,
            self.binloc, self.ydist, self.xdist, xsize)
    # FINDME: retipsplinemap, retbinstd
    return bli.bilinint(params, args)


  def setup(self, y, x, ystep, xstep, minpt=1, verbose=False):
    """
    Set up the BLISS map variables.

    Parameters
    ----------
    y: 1D float ndarray
      Y-coordinate array of data set (zeroth index).
    x: 1D float ndarray
      X-coordinate array of data set (first index).
    ystep: Float
      Y-coordinate BLISS map grid size.
    xstep: Float
      X-coordinate BLISS map grid size.
    minpt: Integer
      Minimum number of points to accept in a BLISS map tile.

    Notes
    -----
    This method defines:
    self.: 1D integer ndarray
      Mask of accepted (1)/rejected (0) data-set points.
    """
    #  elif fit[j].model[k] in ['posfluxlinip', 'linip']:
    #    fit[j].wherepos   = []
    #    fit[j].meanypos   = []
    #    fit[j].meanxpos   = []
    #    for i in range(pup[j].npos):
    #      wherepos = np.where(fit[j].pos == i)[0]
    #      fit[j].wherepos.append(wherepos)
    #      fit[j].meanypos.append(np.mean(fit[j].position[0][wherepos]))
    #      fit[j].meanxpos.append(np.mean(fit[j].position[1][wherepos]))
    #    fit[j].funcx.  append([fit[j].position, fit[j].nobj,
    #                           fit[j].wherepos])
    #    fit[j].etc.append([fit[j].meanypos, fit[j].meanxpos])

    # y = event.y
    # mask = fit.clipmask

    quadrant = np.zeros(len(x))
    upq   = y-np.round(np.median(y)) > config[j].ydiv  # in Upper quad
    leftq = x-np.round(np.median(y)) < config[j].xdiv  # in Left  quad
    quadrant[np.where(  upq & 1-leftq)] = 1  # upper right
    quadrant[np.where(1-upq & 1-leftq)] = 2  # lower right
    quadrant[np.where(1-upq &   leftq)] = 3  # lower left

    position = np.array([y[clipmask], x[clipmask]])

    # Create knots for ipspline:
    numipyk, numipxk = self.pars
    self.etc.append(np.meshgrid(np.linspace(position[1].min(),
                                            position[1].max(), numipxk),
                                np.linspace(position[0].min(),
                                            position[0].max(), numipyk)))

