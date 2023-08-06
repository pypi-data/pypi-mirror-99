#!/usr/bin/env python

"""
Utility for updating/changing the LSL telemetry setting.
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
import sys
if sys.version_info < (3,):
    range = xrange
    
import os
import sys
import argparse

from lsl.misc import telemetry
telemetry.track_script()


def main(args):
    # Toggle
    if args.enable:
        telemetry.enable()
    elif args.disable:
        telemetry.disable()
        
    # Report
    ## Status
    print("LSL Telemetry is %s" % ('active' if telemetry.is_active() else 'in-active'))
    
    ## Key
    if args.key:
        print("  Identification key: %s" % telemetry._INSTALL_KEY)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='update the LSL telemetry setting', 
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )
    tgroup = parser.add_mutually_exclusive_group(required=False)
    tgroup.add_argument('-e', '--enable', action='store_true', 
                        help='enable telemetry for LSL')
    tgroup.add_argument('-d', '--disable', action='store_true', 
                        help='disable telemetry for LSL')
    parser.add_argument('-k', '--key', action='store_true',
                        help='show install identification key')
    args = parser.parse_args()
    main(args)
