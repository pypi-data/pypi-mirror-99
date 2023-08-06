"""
Unit test for the lsl.common.stations module.
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
import sys
if sys.version_info < (3,):
    range = xrange
    
import os
import ephem
import pickle
import unittest
from datetime import datetime

from lsl.common.paths import DATA_BUILD
from lsl.common import stations, dp, mcs, sdf, metabundle, sdm


__version__  = "0.4"
__author__    = "Jayce Dowell"


class stations_tests(unittest.TestCase):
    """A unittest.TestCase collection of unit tests for the lsl.common.stations
    module."""

    def test_station(self):
        """Test retrieving stations from the stations module."""

        lwa1 = stations.lwa1
        self.assertTrue(isinstance(lwa1, stations.LWAStation))
        
        lwasv = stations.lwasv
        self.assertTrue(isinstance(lwasv, stations.LWAStation))
        
    def test_observer(self):
        """Test the ephem.Observer portion of an LWAStation."""
        
        lwa1 = stations.lwa1
        jov = ephem.Jupiter()
        
        lwa1.date = '2013/7/10 22:07:07'
        lwa1.compute(jov)
        
        # RA/Dec
        self.assertAlmostEqual(jov.ra,  ephem.hours('6:14:41.01'), 6)
        self.assertAlmostEqual(jov.dec, ephem.degrees('23:11:49.1'), 6)
        
        #Az/Alt
        self.assertAlmostEqual(jov.az,  ephem.degrees('274:40:27.7'), 6)
        self.assertAlmostEqual(jov.alt, ephem.degrees( '37:24:10.5'), 6)
        
    def test_pickle(self):
        """Test pickling of LWAStation instances."""
        
        lwa1 = stations.lwa1
        
        # Pickle and re-load
        out  = pickle.dumps(lwa1)
        lwa1Prime = pickle.loads(out)
        
        # Test similarity
        self.assertAlmostEqual(lwa1.lat, lwa1Prime.lat)
        self.assertAlmostEqual(lwa1.long, lwa1Prime.long)
        self.assertAlmostEqual(lwa1.elev, lwa1Prime.elev)
        for i in range(520):
            self.assertEqual(lwa1.antennas[i].id, lwa1Prime.antennas[i].id)
            self.assertEqual(lwa1.antennas[i].stand.id, lwa1Prime.antennas[i].stand.id)
            self.assertEqual(lwa1.antennas[i].digitizer, lwa1Prime.antennas[i].digitizer)
        self.assertEqual(lwa1.interface.mcs, lwa1Prime.interface.mcs)
        self.assertEqual(lwa1.interface.sdf, lwa1Prime.interface.sdf)
        
        # Check independence
        lwa1Prime.antennas[100].stand.id = 888
        self.assertTrue(lwa1.antennas[100].stand.id != lwa1Prime.antennas[100].stand.id)
        
        lwasv = stations.lwasv
        
        # Pickle and re-load
        out  = pickle.dumps(lwasv)
        lwasvPrime = pickle.loads(out)
        
        # Test similarity
        self.assertAlmostEqual(lwasv.lat, lwasvPrime.lat)
        self.assertAlmostEqual(lwasv.long, lwasvPrime.long)
        self.assertAlmostEqual(lwasv.elev, lwasvPrime.elev)
        for i in range(512):
            self.assertEqual(lwasv.antennas[i].id, lwasvPrime.antennas[i].id)
            self.assertEqual(lwasv.antennas[i].stand.id, lwasvPrime.antennas[i].stand.id)
            self.assertEqual(lwasv.antennas[i].digitizer, lwasvPrime.antennas[i].digitizer)
        self.assertEqual(lwasv.interface.mcs, lwasvPrime.interface.mcs)
        self.assertEqual(lwasv.interface.sdf, lwasvPrime.interface.sdf)
        
        # Check independence
        lwasvPrime.antennas[100].stand.id = 888
        self.assertTrue(lwasv.antennas[100].stand.id != lwasvPrime.antennas[100].stand.id)
        
    def test_strings(self):
        """Test string representations in the stations module."""
        
        lwa1 = stations.lwa1
        str(lwa1)
        repr(lwa1)
        
        str(lwa1.antennas[0])
        repr(lwa1.antennas[0])
        
        str(lwa1.antennas[0].fee)
        repr(lwa1.antennas[0].fee)
        
        str(lwa1.antennas[0].stand)
        repr(lwa1.antennas[0].stand)
        
        str(lwa1.antennas[0].cable)
        repr(lwa1.antennas[0].cable)
        
        str(lwa1.antennas[0].arx)
        repr(lwa1.antennas[0].arx)
        
        str(lwa1.interface)
        repr(lwa1.interface)
        
    def test_ecef_conversion(self):
        """Test the stations.geo_to_ecef() function."""

        lat = 0.0
        lng = 0.0
        elev = 0.0
        x, y, z = stations.geo_to_ecef(lat, lng, elev)
        self.assertAlmostEqual(x, 6378137.0)
        self.assertAlmostEqual(y, 0.0)
        self.assertAlmostEqual(z, 0.0)
        
    def test_interfaces(self):
        """Test retrieving LSL interface information."""
        
        lwa1 = stations.lwa1
        self.assertEqual(lwa1.interface.backend, 'lsl.common.dp')
        self.assertEqual(lwa1.interface.mcs, 'lsl.common.mcs')
        self.assertEqual(lwa1.interface.sdf, 'lsl.common.sdf')
        self.assertEqual(lwa1.interface.metabundle, 'lsl.common.metabundle')
        self.assertEqual(lwa1.interface.sdm, 'lsl.common.sdm')
        
        lwasv = stations.lwasv
        self.assertEqual(lwasv.interface.backend, 'lsl.common.adp')
        self.assertEqual(lwasv.interface.mcs, 'lsl.common.mcsADP')
        self.assertEqual(lwasv.interface.sdf, 'lsl.common.sdfADP')
        self.assertEqual(lwasv.interface.metabundle, 'lsl.common.metabundleADP')
        self.assertEqual(lwasv.interface.sdm, 'lsl.common.sdmADP')
        
        lwana = stations.lwana
        self.assertEqual(lwana.interface.backend, None)
        self.assertEqual(lwana.interface.mcs, None)
        self.assertEqual(lwana.interface.sdf, None)
        self.assertEqual(lwana.interface.metabundle, None)
        self.assertEqual(lwana.interface.sdm, None)
        
    def test_interface_modules(self):
        """Test retrieving LSL interface modules."""
        
        lwa1 = stations.lwa1
        self.assertEqual(lwa1.interface.get_module('backend'), dp)
        self.assertEqual(lwa1.interface.get_module('mcs'), mcs)
        self.assertEqual(lwa1.interface.get_module('sdf'), sdf)
        self.assertEqual(lwa1.interface.get_module('metabundle'), metabundle)
        self.assertEqual(lwa1.interface.get_module('sdm'), sdm)
        
        lwasv = stations.lwasv
        self.assertFalse(lwasv.interface.get_module('backend') == dp)
        self.assertFalse(lwasv.interface.get_module('mcs') == mcs)
        self.assertFalse(lwasv.interface.get_module('sdf') == sdf)
        self.assertFalse(lwasv.interface.get_module('metabundle') == metabundle)
        self.assertFalse(lwasv.interface.get_module('sdm') == sdm)
        
    def test_ssmif_text(self):
        """Test the text SSMIF parser."""
        
        ssmifFile = os.path.join(DATA_BUILD, 'lwa1-ssmif.txt')
        out = stations.parse_ssmif(ssmifFile)
        
    def test_ssmif_test_adp(self):
        """Test the text SSMIF parser for ADP-based stations."""
        
        ssmifFile = os.path.join(DATA_BUILD, 'lwasv-ssmif.txt')
        out = stations.parse_ssmif(ssmifFile)
        
    def test_ssmif_binary(self):
        """Test the binary SSMIF parser."""
        
        ssmifFile = os.path.join(DATA_BUILD, 'tests', 'ssmif.dat')
        out = stations.parse_ssmif(ssmifFile)
        
    def test_ssmif_binary_adp(self):
        """Test the binary SSMIF parser for ADP-based stations."""
        
        ssmifFile = os.path.join(DATA_BUILD, 'tests', 'ssmif-adp.dat')
        out = stations.parse_ssmif(ssmifFile)
        
    def test_responses(self):
        """Test the various frequency responses."""
        
        lwa1 = stations.lwa1
        lwa1[0].fee.response()
        lwa1[0].cable.response()
        for filt in ('split', 'full', 'reduced', 'split@3MHz', 'full@3MHz'):
            lwa1[0].arx.response(filt)
            
        lwasv = stations.lwasv
        lwasv[0].fee.response()
        lwasv[0].cable.response()
        for filt in ('split', 'full', 'reduced', 'split@3MHz', 'full@3MHz'):
            lwasv[0].arx.response(filt)


class stations_test_suite(unittest.TestSuite):
    """A unittest.TestSuite class which contains all of the lsl.common.stations
    module unit tests."""
    
    def __init__(self):
        unittest.TestSuite.__init__(self)
        
        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(stations_tests)) 


if __name__ == '__main__':
    unittest.main()
