#!/usr/bin/env python

"""
Example script to read in the positions of stands at LWA-1 and make a plot
of the site.
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
import sys
if sys.version_info < (3,):
    range = xrange
    
import sys
import numpy
import argparse

from lsl.common import stations, metabundle, metabundleADP

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

from lsl.misc import telemetry
telemetry.track_script()


def main(args):
    # Parse command line
    toMark = numpy.array(args.stand)-1
    
    # Setup the LWA station information
    if args.metadata is not None:
        try:
            station = stations.parse_ssmif(args.metadata)
        except ValueError:
            try:
                station = metabundle.get_station(args.metadata, apply_sdm=True)
            except:
                station = metabundleADP.get_station(args.metadata, apply_sdm=True)
    elif args.lwasv:
        station = stations.lwasv
    else:
        station = stations.lwa1
    stands = station.stands
    stands.sort()

    # Load in the stand position data
    data = numpy.zeros((len(stands)//2,3))
    
    i = 0
    for stand in stands[::2]:
        data[i,0] = stand.x
        data[i,1] = stand.y
        data[i,2] = stand.z
        i += 1
        
    # Color-code the stands by their elevation
    color = data[:,2]
    
    # Plot the stands as colored circles
    fig = plt.figure(figsize=(8,8))
    
    ax1 = plt.axes([0.30, 0.30, 0.60, 0.60])
    ax2 = plt.axes([0.30, 0.05, 0.60, 0.15])
    ax3 = plt.axes([0.05, 0.30, 0.15, 0.60])
    ax4 = plt.axes([0.05, 0.05, 0.15, 0.15])
    c = ax1.scatter(data[:,0], data[:,1], c=color, s=40.0, alpha=0.50)	
    ax1.set_xlabel('$\Delta$X [E-W; m]')
    ax1.set_xlim([-80, 80])
    ax1.set_ylabel('$\Delta$Y [N-S; m]')
    ax1.set_ylim([-80, 80])
    ax1.set_title('%s Site:  %.3f$^\circ$N, %.3f$^\circ$W' % (station.name, station.lat*180.0/numpy.pi, -station.long*180.0/numpy.pi))
    
    ax2.scatter(data[:,0], data[:,2], c=color, s=40.0)
    ax2.xaxis.set_major_formatter( NullFormatter() )
    ax2.set_ylabel('$\Delta$Z [m]')
    ax3.scatter(data[:,2], data[:,1], c=color, s=40.0)
    ax3.yaxis.set_major_formatter( NullFormatter() )
    ax3.set_xlabel('$\Delta$Z [m]')
    
    # Explicitly mark those that need to be marked
    if toMark.size != 0:
        for i in range(toMark.size):
            ax1.plot(data[toMark[i],0], data[toMark[i],1], marker='x', linestyle=' ', color='black')
            ax2.plot(data[toMark[i],0], data[toMark[i],2], marker='x', linestyle=' ', color='black')
            ax3.plot(data[toMark[i],2], data[toMark[i],1], marker='x', linestyle=' ', color='black')
            
            if args.label:
                ax1.annotate('%i' % (toMark[i]+1), xy=(data[toMark[i],0], data[toMark[i],1]), xytext=(data[toMark[i],0]+1, data[toMark[i],1]+1))
                
    # Add and elevation colorbar to the right-hand side of the figure
    cb = plt.colorbar(c, cax=ax4, orientation='vertical', ticks=[-2, -1, 0, 1, 2])
    
    # Set the axis limits
    ax1.set_xlim([-60, 60])
    ax1.set_ylim([-60, 60])
    ax2.set_xlim( ax1.get_xlim() )
    ax3.set_ylim( ax1.get_ylim() )
    
    # Show n' save
    plt.show()
    if args.output is not None:
        fig.savefig(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='plot the x, y, and z locations of stands at an LWA station', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('stand', type=int, nargs='*', 
                        help='stand number to mark')
    parser.add_argument('-s', '--lwasv', action='store_true', 
                        help='use LWA-SV instead of LWA1')
    parser.add_argument('-m', '--metadata', type=str, 
                        help='name of the SSMIF or metadata tarball file to use for mappings')
    parser.add_argument('-l', '--label', action='store_true', 
                        help='label the specified stands with their ID numbers')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='run %(prog)s in verbose mode')
    parser.add_argument('-o', '--output', type=str, 
                        help='filename to save the plot to')
    args = parser.parse_args()
    main(args)
    
