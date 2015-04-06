# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import numpy
import csv
from optparse import OptionParser
import sys
import os
from prettytable import PrettyTable

from sensorimotor.orphan_temporal_memory import OrphanTemporalMemory
from nupic.research.monitor_mixin.temporal_memory_monitor_mixin import (
  TemporalMemoryMonitorMixin)

class MonitoredTemporalMemory(TemporalMemoryMonitorMixin, OrphanTemporalMemory): pass

#########################################################################
#
# Sequence generation routines

def letterSequence(letters, w=40):
  """
  Return a list of input vectors corresponding to sequence of letters.
  The vector for each letter has w contiguous bits ON and represented as a
  sequence of non-zero indices.
  """
  sequence = []
  for letter in letters:
    i = ord(letter) - ord('A')
    sequence.append(set(range(i*w,(i+1)*w)))
  return sequence


def getRandomVector(w=40, n=2048):
  "Return a list of w random indices out of a vector of n elements"
  return set(numpy.random.permutation(n)[0:w])


def getHighOrderSequenceChunk(it, switchover=1000, w=40, n=2048):
  """
  Given an iteration index, returns a list of vectors to be appended to the
  input stream, as well as a string label identifying the sequence. This
  version generates a bunch of high order sequences. The first element always
  provides sufficient context to predict the rest of the elements.

  After switchover iterations, it will generate a different set of sequences.
  """
  if it%10==3:
    s = numpy.random.randint(5)
    if it <= switchover:
      if s==0:
        label="XABCDE"
      elif s==1:
        label="YCBEAF"
      elif s==2:
        label="GHIJKL"
      elif s==3:
        label="WABCMN"
      else:
        label="ZDBCAE"
    else:
      if s==0:
        label="XCBEAF"
      elif s==1:
        label="YABCDE"
      elif s==2:
        label="GABCMN"
      elif s==3:
        label="WHIJKL"
      else:
        label="ZDHICF"

    vecs = letterSequence(label)
  else:
    vecs= [getRandomVector(w, n)]
    label="."

  return vecs,label

def addNoise(vecs, percent=0.1, w=40, n=2048):
  """
  Add noise to the given sequence of vectors and return the modified  sequence.
  A percentage of the input bits will be flipped from 0 to 1.
  """
  noisyVecs = []
  for vec in vecs:
    for v in vec:
      print v

  return noisyVecs



#########################################################################
#
# Core experiment routines

def computePredictionAccuracy(pac, pic):
  """
  Given a temporal memory instance return the prediction accuracy. The accuracy
  is computed as 1 - (#correctly predicted cols / # predicted cols). The
  accuracy is 0 if there were no predicted columns.
  """
  pcols = float(pac + pic)
  if pcols == 0:
    return 0.0
  else:
    return (pac / pcols)


def runExperiment1(csvWriter, options):
  numpy.random.seed(42)

  tm = MonitoredTemporalMemory(minThreshold=20,
                              activationThreshold=20,
                              maxNewSynapseCount=40,
                              cellsPerColumn=options.cells,
                              learnOnOneCell = False,
                              permanenceOrphanDecrement = 0.01,
                              columnDimensions=(2048,),
                              learningRadius=2048,
                              initialPermanence=0.21,
                              connectedPermanence=0.50,
                              permanenceIncrement=0.10,
                              permanenceDecrement=0.10,
                              seed=42,
                              )

  printOptions(options, tm)

  # Run the simulation using the given parameters
  sequenceString = ""
  i=0
  while i < options.iterations:
    if i%100==0:
      print "i=",i

    if options.simulation == "normal":
      vecs,label = getHighOrderSequenceChunk(i, options.switchover)
    else:
      raise Exception("Unknown simulation: " + options.simulation)

    sequenceString += label

    for xi,vec in enumerate(vecs):
      tm.compute(vec, learn=True)
      i += 1


  # Create CSV file with detailed trace of predictions, missed predictions,
  # and accuracy
  pac = tm.mmGetTracePredictedActiveColumns()
  pic = tm.mmGetTracePredictedInactiveColumns()
  upac = tm.mmGetTraceUnpredictedActiveColumns()

  accuracies = numpy.zeros(len(pac.data))
  am = 0
  csvWriter.writerow(["time", "element", "pac", "pic", "upac", "a",
                      "am", "accuracy","sum"])
  for i,j in enumerate(pac.data):
    if i>0:
      # Compute instantaneous and average accuracy.
      a = computePredictionAccuracy(len(j), len(pic.data[i]))

      #  We compute an exponential plus a windowed average to get curve
      #  looking nice and smooth for the paper.
      am = 0.99*am + 0.01*a
      accuracies[i] = am
      i0 = max(0, i-60+1)
      accuracy = numpy.mean(accuracies[i0:i+1])

      row=[i, sequenceString[i],len(j),len(pic.data[i]),
              len(upac.data[i]), a, am,
              accuracy,
              numpy.sum(accuracies[i0:i+1])]
      csvWriter.writerow(row)
      #print row


#########################################################################
#
# Debugging routines

def printSegment(tm, segment, connections):
  cell = connections.cellForSegment(segment)
  synapses = connections.synapsesForSegment(segment)
  print "segment id=",segment
  print "   cell=",cell
  print "   col =",tm.columnForCell(cell)
  print "   synapses=",
  for synapse in synapses:
    synapseData = connections.dataForSynapse(synapse)
    permanence = synapseData.permanence
    presynapticCell = synapseData.presynapticCell
    print "%d:%g" % (presynapticCell,permanence),
  print


def printTemporalMemory(tm):
  """
  Given an instance of OrphanTemporalMemory, print out the relevant parameters
  """
  table = PrettyTable(["Parameter name", "Value", ])

  table.add_row(["columnDimensions", tm.columnDimensions])
  table.add_row(["cellsPerColumn", tm.cellsPerColumn])
  table.add_row(["activationThreshold", tm.activationThreshold])
  table.add_row(["minThreshold", tm.minThreshold])
  table.add_row(["maxNewSynapseCount", tm.maxNewSynapseCount])
  table.add_row(["permanenceIncrement", tm.permanenceIncrement])
  table.add_row(["permanenceDecrement", tm.permanenceDecrement])
  table.add_row(["initialPermanence", tm.initialPermanence])
  table.add_row(["connectedPermanence", tm.connectedPermanence])
  table.add_row(["permanenceOrphanDecrement", tm.permanenceOrphanDecrement])
  table.add_row(["learnOnOneCell", tm.learnOnOneCell])

  print table.get_string().encode("utf-8")


def printOptions(options, tm):
  """
  Pretty print the set of options
  """
  print "TM parameters:"
  printTemporalMemory(tm)
  print "Experiment parameters:"
  for k,v in options.__dict__.iteritems():
    print "  %s : %s" % (k,str(v))


if __name__ == '__main__':
  helpString = (
    "\n%prog [options] [uid]"
    "\n%prog --help"
    "\n"
    "\nRuns high and low order sequence simulations with artificial data."
  )

  # All the command line options
  parser = OptionParser(helpString)
  parser.add_option("--outputFile",
                    help="Output file. Results will be written to this file."
                    " (default: %default)",
                    dest="outputFile",
                    default=os.path.join('results',"output.csv"))
  parser.add_option("--iterations",
                    help="Number of iterations to run for. [default: %default]",
                    default=1000,
                    type=int)
  parser.add_option("--switchover",
                    help="Number of iterations after which to change "
                         "statistics. [default: %default]",
                    default=1000,
                    type=int)
  parser.add_option("--cells",
                    help="Number of per column. [default: %default]",
                    default=8,
                    type=int)
  parser.add_option("--simulation",
                    help="Which simulation to run: 'normal' or 'noisy'"
                    " (default: %default)",
                    default="normal",
                    type=str)

  options, args = parser.parse_args(sys.argv[1:])

  with open(options.outputFile,"wb") as outputFile:
    csvWriter = csv.writer(outputFile)
    runExperiment1(csvWriter, options)
