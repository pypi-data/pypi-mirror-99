import sys
import os
import numpy as np

#topdir = os.path.realpath(os.path.dirname(__file__) + "/../..")
#sys.path.append(topdir + "/puppies/lib")
#import _bilinint as bli


__all__ = ["ballardip"]

class ballardip():
  def __init__(self):
    self.name = "ballardip"
    self.type = "pixmap"
    self.pnames = ["sigmay", "sigmax", "nbins"]
    self.npars = len(self.pnames)
    self.params = np.zeros(self.npars)
    self.pmin   = np.tile(-np.inf, self.npars)
    self.pmax   = np.tile( np.inf, self.npars)
    self.pstep  = np.zeros(self.npars)

  def __call__(self, params, x):
    return self.eval(params, x)


  def eval(self, params, position, ballardip, flux):
    args = None  # FINDME
    return bli.bilinint(params, args)


  def setup(self, flux=None, pup=None):
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
    self.ballardipmask: 1D integer ndarray
      Mask of accepted (1)/rejected (0) data-set points.
    self.ygrid: 1D float ndarray
      Array of Y-axis coordinates of the knot centers.
    self.xgrid: 1D float ndarray
      Array of X-axis coordinates of the knot centers.
    self.knotpts: 1D integer ndarray
      Data-point indices sorted by knot.
    self.knotsize: 1D integer ndarray
      Number of datapoints per knot.
    self.kploc:  1D integer ndarray
      Index of first data-point index of each knot.
    self.binloc:  1D float ndarray
      Index of the knot to the lower left of the data points.
    self.ydist: 1D float ndarray
      Normalized distance to the bottom knot (binloc).
    self.xdist: 1D float ndarray
      Normalized distance to the left knot (binloc).
    """
    if pup is not None:
      flux = pup.flux
    self.ballardip = np.ones(np.size(flux))
    self.position = fit.position, self.ballardip, flux

