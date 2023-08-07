# Copyright (c) 2021 Patricio Cubillos
# puppies is open-source software under the MIT license (see LICENSE)

__all__ = ["offset"]

import sys
import os
import numpy as np


class AOR(object):
  """
  Ramp-model superclass.
  """
  def __init__(self, time=None, mask=None, params=None):
    self.type = "ramp"
    self.npars = len(self.pnames)
    self.params = np.ones(self.npars)
    if params is not None:
      self.params[:] = params
    self.pmin   = np.tile(-np.inf, self.npars)
    self.pmax   = np.tile( np.inf, self.npars)
    self.pstep  = np.zeros(self.npars)
    if time is not None:
      self.setup(time)


  def __call__(self, params, time=None, mask=None):
    """
    Call function with self values.
    Update defaults if necessary.
    """
    if time is not None:
      self.time = time
    if mask is not None:
      self.mask = mask
    return self.eval(params, self.time[self.mask])


  def setup(self, time=None, mask=None, obj=None):
    """
    Set default independent variables (when calling eval without args).
    """
    if obj is not None:
      time = obj.aor
      if mask is None:  # Input mask takes priority over pup.mask
        mask = obj.mask

    if mask is None:
      mask = np.ones(len(time), bool)

    self.time = time
    self.mask = mask



class offset(AOR):
  """
  Linear ramp model.
  Docstring me!

  Attributes
  ----------
  TBD

  Example
  -------
  TBD
  """
  def __init__(self, time=None, mask=None, params=None):
    self.name = "offset"
    self.pnames = ["aor1", "aor2", "aor3", "aor4", "aor5"]
    super(offset, self).__init__(time, mask, params)


  def eval(self, params, time):
    """
    Evaluate the ramp function at the specified times.
    """
    aor = np.ones(len(time))
    for i in np.arange(self.npars):
      if params[i] != 1.0:
        aor[time==i] = params[i]
    return aor

