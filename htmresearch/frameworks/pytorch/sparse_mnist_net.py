# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2018, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

from __future__ import print_function
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

from htmresearch.frameworks.pytorch.k_winners import KWinners

import matplotlib
matplotlib.use('Agg')

class SparseMNISTNet(nn.Module):

  def __init__(self, n=2000, k=200,
               weightSparsity=0.5,
               boostStrength=1.0,
               boostStrengthFactor=1.0):
    """
    A network with one hidden layer, which is a k-sparse linear layer, designed
    for MNIST.

    :param n:
      Number of units in the hidden layer

    :param k:
      Number of ON (non-zero) units per iteration

    :param weightSparsity:
      Pct of weights that are allowed to be non-zero

    :param boostStrength:
      boost strength (0.0 implies no boosting)

    :param boostStrengthFactor:
      boost strength is multiplied by this factor after each epoch.
      A value < 1.0 will decrement it every epoch.

    """
    super(SparseMNISTNet, self).__init__()

    assert(weightSparsity >= 0)

    self.k = k
    self.n = n
    self.l1 = nn.Linear(28*28, self.n)
    self.weightSparsity = weightSparsity   # Pct of weights that are non-zero
    self.zeroWts = []
    self.l2 = nn.Linear(self.n, 10)
    self.learningIterations = 0

    # Boosting related variables
    self.dutyCyclePeriod = 1000
    self.boostStrength = boostStrength
    self.boostStrengthFactor = boostStrengthFactor
    self.dutyCycle = torch.zeros(self.n)

    # For each L1 unit, decide which weights are going to be zero
    numZeros = int(round((1.0 - self.weightSparsity) * self.l1.weight.shape[1]))
    for i in range(self.n):
      self.zeroWts.append(
        np.random.permutation(self.l1.weight.shape[1])[0:numZeros])

    self.rezeroWeights()


  def rezeroWeights(self):
    # print("non zero before:",self.l1.weight.data.nonzero().shape)
    for i in range(self.n):
      self.l1.weight.data[i, self.zeroWts[i]] = 0.0
    # print("non zero after:",self.l1.weight.data.nonzero().shape)


  def postEpoch(self):
    """
    Call this once after each training epoch. Currently just updates
    boostStrength
    """
    self.boostStrength = self.boostStrength * self.boostStrengthFactor
    print("boostStrength is now:", self.boostStrength)


  def forward(self, x):

    # First hidden layer
    x = x.view(-1, 28*28)

    # Apply k-winner algorithm if k < n, otherwise default to standard RELU
    if self.k != self.n:
      x = KWinners.apply(self.l1(x), self.dutyCycle, self.k, self.boostStrength)
    else:
      x = F.relu(self.l1(x))

    if self.training:
      # Update moving average of duty cycle for training iterations only
      # During inference this is kept static.
      batchSize = x.shape[0]
      self.learningIterations += batchSize

      # Only need to update dutycycle if if k < n
      if self.k != self.n:
        period = min(self.dutyCyclePeriod, self.learningIterations)
        self.dutyCycle = (self.dutyCycle * (period - batchSize) +
                          ((x > 0).sum(dim=0)).float()) / period

    # Output layer
    x = self.l2(x)
    x = F.log_softmax(x, dim=1)

    return x

  def _apply(self, fn):
      ret = super(SparseMNISTNet, self)._apply(fn)
      self.dutyCycle = fn(self.dutyCycle)
      return ret

  def printMetrics(self):
    print("Learning Iterations:", self.learningIterations)
    print("non zero weights:", self.l1.weight.data.nonzero().shape,
          "all weights:", self.l1.weight.data.shape)
    print("duty cycles min/max/mean:",
          self.dutyCycle.min(), self.dutyCycle.max(), self.dutyCycle.mean())


  def printParameters(self):
    print("              k :", self.k)
    print("              n :", self.n)
    print(" weightSparsity :", self.weightSparsity)
    print("  boostStrength :", self.boostStrength)
    print("dutyCyclePeriod :", self.dutyCyclePeriod)
