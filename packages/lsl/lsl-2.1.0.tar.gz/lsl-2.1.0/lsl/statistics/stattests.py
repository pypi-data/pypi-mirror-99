"""
Collection of statistical tests not found in any of the common
python libraries.
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
import sys
if sys.version_info < (3,):
    range = xrange
    
import numpy
from scipy.special import ndtr

from lsl.misc import telemetry
telemetry.track_module()


__version__ = '0.1'
__all__ = ['wald_wolfowitz',]


def _to_binary(inputData):
    """
    Convert a floating point data sequence (like the difference
    between the data and a model to a 1-bit data sequence.  Values
    <=0 are mapped to 0 and all others to 1.
    """
    
    data = inputData.ravel()
    binary = numpy.where( data > 0, 1, 0 )
    return binary.astype(numpy.int8)


def _count_runs(inputData):
    """
    Count the number of runs in a data set and returns a three-element
    tuple of the number of:
     * total runs
     * positive values (inputData > 0)
     * negative values ( inputData <= 0)
    Where a run is defined as sequential groups of two or more instances of
    the same value in the data.
    """
    
    data = _to_binary(inputData)
    
    tot = 1
    pos = 0
    neg = 0
    for c,p in zip(data[1:], data[0:-1]):
        if c == 1 and p == 1:
            pos = pos + 1
        elif c == 1 and p == 0:
            tot = tot + 1
            pos = pos + 1
        elif c == 0 and p == 1:
            tot = tot + 1
    pos = data.sum()
    neg = len(data) - pos
    
    return (tot, pos, neg)


def wald_wolfowitz(inputData):
    """
    Wald-Wolfowitz test of randomness.  Given a numpy array of values
    compute the probability that the values are mutially independent.
    
    .. seealso::
        http://en.wikipedia.org/wiki/Wald%E2%80%93Wolfowitz_runs_test
    """
    
    N, Np, Nn = _count_runs(inputData)
    mean = 2.0*Np*Nn/(Np+Nn) + 1.0
    vari = ((2.0*Np*Nn)*(2.0*Np*Nn-Np-Nn)) / ((Np+Nn)**2 * (Np+Nn-1))
    sigm = numpy.sqrt(vari)
    
    if N > 50:
        z = (N - mean) / sigm
    elif (N-mean) < 0:
        z = (N - mean + 0.5) /sigm
    else:
        z = (N - mean - 0.5) /sigm
        
    pValue = 2.0*(1-ndtr(numpy.abs(z)))
    return pValue
    
