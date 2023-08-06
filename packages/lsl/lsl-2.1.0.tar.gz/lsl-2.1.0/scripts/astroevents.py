#!/usr/bin/env python

"""
LWA_Common.astro module informal unit test / demo: give LWA-1 observation data
at current system clock time

Moved out of the lsl.astro module into this script and updated for LWA-1
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
import sys
if sys.version_info < (3,):
    range = xrange

import math    
import argparse

from lsl import astro
from lsl.common import stations

from lsl.misc import telemetry
telemetry.track_script()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('-s', '--site', type=str, default='LWA-1',
                        help='site name')
    args = parser.parse_args()
    
    # setup transform objects
    site = args.site.lower().replace('-', '')
    if site == 'lwa1':
        station = stations.lwa1
    elif site == 'lwasv':
        station = stations.lwasv
    elif site == 'ovrolwa':
        station = stations.lwa1
        station.name = 'OVRO-LWA'
        station.lat, station.long, station.elev = ('37.2397808', '-118.2816819', 1183.4839)
    else:
        raise RuntimeError("Unknown site name: %s" % site)
        
    nam = station.name
    lng = astro.deg_to_dms(station.long*180/math.pi)
    lat = astro.deg_to_dms(station.lat*180/math.pi)
    lwa_lnlat = astro.lnlat_posn(lng, lat)
    
    print('---------------------------------------------------------------')
    print('%s location' % nam)
    print('---------------------------------------------------------------')
    print('Longitude:         %s (%0.3f)' % (lng, lwa_lnlat.lng))
    print('Latitude:          %s (%0.3f)' % (lat, lwa_lnlat.lat)) 
        
    # calculate offset from GM
    
    lwa_gm_hms = astro.deg_to_hms(-lwa_lnlat.lng)
    lwa_gm_off = lwa_gm_hms.to_sec()
    print('GM Offset:         %s (%0.3f)' % (lwa_gm_hms, lwa_gm_off))
    
    # get current UTC time from system clock
    
    utc = astro.get_julian_from_sys()
    utcd = astro.get_date(utc)
    lcld = utcd.to_zone()
    unixt = astro.get_timet_from_julian(utc)
    
    # caculate sidereal times
    
    gm_sid = astro.get_apparent_sidereal_time(utc)
    lwa_sid = astro.get_local_sidereal_time(lwa_lnlat.lng, utc)
        
    print('---------------------------------------------------------------')
    print('Current time')
    print('---------------------------------------------------------------')
    print('UTC time:             %s (%0.3f)' % (utcd, utc))
    print('%s local time:     %s' % (nam, str(lcld)))
    print('GM sidereal time:     %0.3f' % gm_sid)
    print('%s sidereal time:  %0.3f' % (nam, lwa_sid))
    print('UNIX time:            %d' % unixt)   
    
    # calculate nutation
    
    nut = astro.get_nutation(utc)
    (nut_lng, nut_obl, nut_ecl) = nut.format()
    
    print('---------------------------------------------------------------')
    print('Nutation')
    print('---------------------------------------------------------------')
    print('Longitude nutation: %s (%0.4f)' % (nut_lng, nut.longitude))
    print('Obliquity nutation: %s (%0.4f)' % (nut_obl, nut.obliquity))
    print('Ecliptic obliquity: %s (%0.4f)' % (nut_ecl, nut.ecliptic))
    
    # calculate Solar phenomena
    
    sun_rst = astro.get_solar_rst(utc, lwa_lnlat)
    (sun_utc_rise, sun_utc_set, sun_utc_trans) = sun_rst.format()
    sun_lcl_rise = sun_utc_rise.to_zone()
    sun_lcl_trans = sun_utc_trans.to_zone()
    sun_lcl_set = sun_utc_set.to_zone()
    
    sun_equ = astro.get_solar_equ_coords(utc) 
    (sun_ra, sun_dec) = sun_equ.format()
    sun_hrz = sun_equ.to_hrz(lwa_lnlat, utc)
    sun_ecl = sun_equ.to_ecl(utc)
    (sun_lng, sun_lat) = sun_ecl.format()
    
    print('---------------------------------------------------------------')
    print('Sun')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (sun_ra, sun_equ.ra))
    print('DEC:               %s (%0.3f)' % (sun_dec, sun_equ.dec)) 
    print('Ecl longitude:     %s (%0.3f)' % (sun_lng, sun_ecl.lng))
    print('Ecl latitude:      %s (%0.3f)' % (sun_lat, sun_ecl.lat))             
    print('Rise:              %s (%0.3f) [%s]' % (sun_utc_rise, sun_rst.rise, sun_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (sun_utc_trans, sun_rst.transit, sun_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (sun_utc_set, sun_rst.set, sun_lcl_set))
    print('Azimuth:           %0.3f %s' % (sun_hrz.az, astro.hrz_to_nswe(sun_hrz)))
    print('Altitude:          %0.3f' % sun_hrz.alt)
    print('Zenith:            %0.3f' % sun_hrz.zen()) 
        
    
    # calculate Lunar phenomena
    
    moon_rst = astro.get_lunar_rst(utc, lwa_lnlat)
    (moon_utc_rise, moon_utc_set, moon_utc_trans) = moon_rst.format()
    moon_lcl_rise = moon_utc_rise.to_zone()
    moon_lcl_trans = moon_utc_trans.to_zone()
    moon_lcl_set = moon_utc_set.to_zone()
    
    moon_equ = astro.get_lunar_equ_coords(utc) 
    (moon_ra, moon_dec) = moon_equ.format()
    moon_hrz = moon_equ.to_hrz(lwa_lnlat, utc)
    moon_ecl = moon_equ.to_ecl(utc)
    (moon_lng, moon_lat) = moon_ecl.format()
    
    moon_sun_ang = sun_equ.angular_separation(moon_equ)
    
    print('---------------------------------------------------------------')
    print('Moon')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (moon_ra, moon_equ.ra))
    print('DEC:               %s (%0.3f)' % (moon_dec, moon_equ.dec)) 
    print('Ecl longitude:     %s (%0.3f)' % (moon_lng, moon_ecl.lng))
    print('Ecl latitude:      %s (%0.3f)' % (moon_lat, moon_ecl.lat))             
    print('Rise:              %s (%0.3f) [%s]' % (moon_utc_rise, moon_rst.rise, moon_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (moon_utc_trans, moon_rst.transit, moon_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (moon_utc_set, moon_rst.set, moon_lcl_set))
    print('Azimuth:           %0.3f %s' % (moon_hrz.az, astro.hrz_to_nswe(moon_hrz)))
    print('Altitude:          %0.3f' % moon_hrz.alt)
    print('Zenith:            %0.3f' % moon_hrz.zen())
    print('Sun angle:         %0.3f' % moon_sun_ang) 
    
    
    # calculate Venus phenomena
    
    venus_rst = astro.get_venus_rst(utc, lwa_lnlat)
    (venus_utc_rise, venus_utc_set, venus_utc_trans) = venus_rst.format()
    venus_lcl_rise = venus_utc_rise.to_zone()
    venus_lcl_trans = venus_utc_trans.to_zone()
    venus_lcl_set = venus_utc_set.to_zone()
    
    venus_equ = astro.get_venus_equ_coords(utc) 
    (venus_ra, venus_dec) = venus_equ.format()
    venus_hrz = venus_equ.to_hrz(lwa_lnlat, utc)
    venus_ecl = venus_equ.to_ecl(utc)
    (venus_lng, venus_lat) = venus_ecl.format()
    
    venus_sun_ang = sun_equ.angular_separation(venus_equ)
    venus_elong = sun_ecl.lng - venus_ecl.lng
    if venus_elong < 0:
        venus_dir = 'E'
    else:
        venus_dir = 'W'
    
    print('---------------------------------------------------------------')
    print('Venus')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (venus_ra, venus_equ.ra))
    print('DEC:               %s (%0.3f)' % (venus_dec, venus_equ.dec)) 
    print('Ecl longitude:     %s (%0.3f)' % (venus_lng, venus_ecl.lng))
    print('Ecl latitude:      %s (%0.3f)' % (venus_lat, venus_ecl.lat))             
    print('Rise:              %s (%0.3f) [%s]' % (venus_utc_rise, venus_rst.rise, venus_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (venus_utc_trans, venus_rst.transit, venus_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (venus_utc_set, venus_rst.set, venus_lcl_set))
    print('Azimuth:           %0.3f %s' % (venus_hrz.az, astro.hrz_to_nswe(venus_hrz)))
    print('Altitude:          %0.3f' % venus_hrz.alt)
    print('Zenith:            %0.3f' % venus_hrz.zen())
    print('Sun angle:         %0.3f' % venus_sun_ang)
    print('Elongation:        %s %s (%0.3f)' % (astro.deg_to_dms(venus_elong), venus_dir, venus_elong))
    
    
    # calculate Mars phenomena
    
    mars_rst = astro.get_mars_rst(utc, lwa_lnlat)
    (mars_utc_rise, mars_utc_set, mars_utc_trans) = mars_rst.format()
    mars_lcl_rise = mars_utc_rise.to_zone()
    mars_lcl_trans = mars_utc_trans.to_zone()
    mars_lcl_set = mars_utc_set.to_zone()
    
    mars_equ = astro.get_mars_equ_coords(utc) 
    (mars_ra, mars_dec) = mars_equ.format()
    mars_hrz = mars_equ.to_hrz(lwa_lnlat, utc)
    mars_ecl = mars_equ.to_ecl(utc)
    (mars_lng, mars_lat) = mars_ecl.format()
    
    mars_sun_ang = sun_equ.angular_separation(mars_equ)
    
    print('---------------------------------------------------------------')
    print('Mars')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (mars_ra, mars_equ.ra))
    print('DEC:               %s (%0.3f)' % (mars_dec, mars_equ.dec)) 
    print('Ecl longitude:     %s (%0.3f)' % (mars_lng, mars_ecl.lng))
    print('Ecl latitude:      %s (%0.3f)' % (mars_lat, mars_ecl.lat))             
    print('Rise:              %s (%0.3f) [%s]' % (mars_utc_rise, mars_rst.rise, mars_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (mars_utc_trans, mars_rst.transit, mars_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (mars_utc_set, mars_rst.set, mars_lcl_set))
    print('Azimuth:           %0.3f %s' % (mars_hrz.az, astro.hrz_to_nswe(mars_hrz)))
    print('Altitude:          %0.3f' % mars_hrz.alt)
    print('Zenith:            %0.3f' % mars_hrz.zen())
    print('Sun angle:         %0.3f' % mars_sun_ang)
    
    
    # calculate Jupiter phenomena
    
    jupiter_rst = astro.get_jupiter_rst(utc, lwa_lnlat)
    (jupiter_utc_rise, jupiter_utc_set, jupiter_utc_trans) = jupiter_rst.format()
    jupiter_lcl_rise = jupiter_utc_rise.to_zone()
    jupiter_lcl_trans = jupiter_utc_trans.to_zone()
    jupiter_lcl_set = jupiter_utc_set.to_zone()
    
    jupiter_equ = astro.get_jupiter_equ_coords(utc) 
    (jupiter_ra, jupiter_dec) = jupiter_equ.format()
    jupiter_hrz = jupiter_equ.to_hrz(lwa_lnlat, utc)
    jupiter_ecl = jupiter_equ.to_ecl(utc)
    (jupiter_lng, jupiter_lat) = jupiter_ecl.format()
    
    jupiter_sun_ang = sun_equ.angular_separation(jupiter_equ)
    
    print('---------------------------------------------------------------')
    print('Jupiter')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (jupiter_ra, jupiter_equ.ra))
    print('DEC:               %s (%0.3f)' % (jupiter_dec, jupiter_equ.dec)) 
    print('Ecl longitude:     %s (%0.3f)' % (jupiter_lng, jupiter_ecl.lng))
    print('Ecl latitude:      %s (%0.3f)' % (jupiter_lat, jupiter_ecl.lat))             
    print('Rise:              %s (%0.3f) [%s]' % (jupiter_utc_rise, jupiter_rst.rise, jupiter_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (jupiter_utc_trans, jupiter_rst.transit, jupiter_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (jupiter_utc_set, jupiter_rst.set, jupiter_lcl_set))
    print('Azimuth:           %0.3f %s' % (jupiter_hrz.az, astro.hrz_to_nswe(jupiter_hrz)))
    print('Altitude:          %0.3f' % jupiter_hrz.alt)
    print('Zenith:            %0.3f' % jupiter_hrz.zen())
    print('Sun angle:         %0.3f' % jupiter_sun_ang)
    
    
    # calculate Saturn phenomena
    
    saturn_rst = astro.get_saturn_rst(utc, lwa_lnlat)
    (saturn_utc_rise, saturn_utc_set, saturn_utc_trans) = saturn_rst.format()
    saturn_lcl_rise = saturn_utc_rise.to_zone()
    saturn_lcl_trans = saturn_utc_trans.to_zone()
    saturn_lcl_set = saturn_utc_set.to_zone()
    
    saturn_equ = astro.get_saturn_equ_coords(utc) 
    (saturn_ra, saturn_dec) = saturn_equ.format()
    saturn_hrz = saturn_equ.to_hrz(lwa_lnlat, utc)
    saturn_ecl = saturn_equ.to_ecl(utc)
    (saturn_lng, saturn_lat) = saturn_ecl.format()
    
    saturn_sun_ang = sun_equ.angular_separation(saturn_equ)
    
    print('---------------------------------------------------------------')
    print('Saturn')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (saturn_ra, saturn_equ.ra))
    print('DEC:               %s (%0.3f)' % (saturn_dec, saturn_equ.dec)) 
    print('Ecl longitude:     %s (%0.3f)' % (saturn_lng, saturn_ecl.lng))
    print('Ecl latitude:      %s (%0.3f)' % (saturn_lat, saturn_ecl.lat))             
    print('Rise:              %s (%0.3f) [%s]' % (saturn_utc_rise, saturn_rst.rise, saturn_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (saturn_utc_trans, saturn_rst.transit, saturn_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (saturn_utc_set, saturn_rst.set, saturn_lcl_set))
    print('Azimuth:           %0.3f %s' % (saturn_hrz.az, astro.hrz_to_nswe(saturn_hrz)))
    print('Altitude:          %0.3f' % saturn_hrz.alt)
    print('Zenith:            %0.3f' % saturn_hrz.zen())
    print('Sun angle:         %0.3f' % saturn_sun_ang)
    
    # calculate SgrA phenomena
    
    sgra_j2000_equ = astro.equ_posn(astro.hms(17, 42, 48.1), astro.dms(True, 28, 55, 8))
    sgra_equ = astro.get_apparent_posn(sgra_j2000_equ, utc)
    sgra_rst = astro.get_object_rst(utc, lwa_lnlat, sgra_equ)
    (sgra_utc_rise, sgra_utc_set, sgra_utc_trans) = sgra_rst.format()
    sgra_lcl_rise = sgra_utc_rise.to_zone()
    sgra_lcl_trans = sgra_utc_trans.to_zone()
    sgra_lcl_set = sgra_utc_set.to_zone()
    
    (sgra_ra, sgra_dec) = sgra_equ.format()
    sgra_hrz = sgra_equ.to_hrz(lwa_lnlat, utc)
    sgra_gal = sgra_equ.to_gal(utc)
    (sgra_l, sgra_b) = sgra_gal.format()
    
    sgra_sun_ang = sun_equ.angular_separation(sgra_equ)
    
    print('---------------------------------------------------------------')
    print('SgrA')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (sgra_ra, sgra_equ.ra))
    print('DEC:               %s (%0.3f)' % (sgra_dec, sgra_equ.dec)) 
    print('Gal longitude:     %s (%0.3f)' % (sgra_l, sgra_gal.l))
    print('Gal latitude:      %s (%0.3f)' % (sgra_b, sgra_gal.b))           
    print('Rise:              %s (%0.3f) [%s]' % (sgra_utc_rise, sgra_rst.rise, sgra_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (sgra_utc_trans, sgra_rst.transit, sgra_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (sgra_utc_set, sgra_rst.set, sgra_lcl_set))
    print('Azimuth:           %0.3f %s' % (sgra_hrz.az, astro.hrz_to_nswe(sgra_hrz)))
    print('Altitude:          %0.3f' % sgra_hrz.alt)
    print('Zenith:            %0.3f' % sgra_hrz.zen())
    print('Sun angle:         %0.3f' % sgra_sun_ang)
    
    # calculate CasA phenomena
    
    casa_j2000_equ = astro.equ_posn(astro.hms(23, 23, 22.7), astro.dms(False, 58, 49, 16))
    casa_equ = astro.get_apparent_posn(casa_j2000_equ, utc)
    
    (casa_ra, casa_dec) = casa_equ.format()
    casa_hrz = casa_equ.to_hrz(lwa_lnlat, utc)
    casa_gal = casa_equ.to_gal(utc)
    (casa_l, casa_b) = casa_gal.format()
    
    casa_sun_ang = sun_equ.angular_separation(casa_equ)
    
    print('---------------------------------------------------------------')
    print('CasA')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (casa_ra, casa_equ.ra))
    print('DEC:               %s (%0.3f)' % (casa_dec, casa_equ.dec)) 
    print('Gal longitude:     %s (%0.3f)' % (casa_l, casa_gal.l))
    print('Gal latitude:      %s (%0.3f)' % (casa_b, casa_gal.b))
    print('Rise:              Circumpolar')
    print('Transit:           -----------')
    print('Set:               Circumpolar')
    print('Azimuth:           %0.3f %s' % (casa_hrz.az, astro.hrz_to_nswe(casa_hrz)))
    print('Altitude:          %0.3f' % casa_hrz.alt)
    print('Zenith:            %0.3f' % casa_hrz.zen())
    print('Sun angle:         %0.3f' % casa_sun_ang)
        

    # calculate CygA phenomena
    
    cyga_j2000_equ = astro.equ_posn(astro.hms(19, 59, 27.8), astro.dms(False, 40, 44, 2))
    cyga_equ = astro.get_apparent_posn(cyga_j2000_equ, utc)
    cyga_rst = astro.get_object_rst(utc, lwa_lnlat, cyga_equ)
    (cyga_utc_rise, cyga_utc_set, cyga_utc_trans) = cyga_rst.format()
    cyga_lcl_rise = cyga_utc_rise.to_zone()
    cyga_lcl_trans = cyga_utc_trans.to_zone()
    cyga_lcl_set = cyga_utc_set.to_zone()
    
    (cyga_ra, cyga_dec) = cyga_equ.format()
    cyga_hrz = cyga_equ.to_hrz(lwa_lnlat, utc)
    cyga_gal = cyga_equ.to_gal(utc)
    (cyga_l, cyga_b) = cyga_gal.format()
    
    cyga_sun_ang = sun_equ.angular_separation(cyga_equ)
    
    print('---------------------------------------------------------------')
    print('CygA')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (cyga_ra, cyga_equ.ra))
    print('DEC:               %s (%0.3f)' % (cyga_dec, cyga_equ.dec)) 
    print('Gal longitude:     %s (%0.3f)' % (cyga_l, cyga_gal.l))
    print('Gal latitude:      %s (%0.3f)' % (cyga_b, cyga_gal.b))           
    print('Rise:              %s (%0.3f) [%s]' % (cyga_utc_rise, cyga_rst.rise, cyga_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (cyga_utc_trans, cyga_rst.transit, cyga_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (cyga_utc_set, cyga_rst.set, cyga_lcl_set))
    print('Azimuth:           %0.3f %s' % (cyga_hrz.az, astro.hrz_to_nswe(cyga_hrz)))
    print('Altitude:          %0.3f' % cyga_hrz.alt)
    print('Zenith:            %0.3f' % cyga_hrz.zen())
    print('Sun angle:         %0.3f' % cyga_sun_ang)
    
    
    # calculate TauA phenomena
    
    taua_j2000_equ = astro.equ_posn(astro.hms(5, 34, 32.0), astro.dms(False, 22, 00, 52.1))
    taua_equ = astro.get_apparent_posn(taua_j2000_equ, utc)
    taua_rst = astro.get_object_rst(utc, lwa_lnlat, taua_equ)
    (taua_utc_rise, taua_utc_set, taua_utc_trans) = taua_rst.format()
    taua_lcl_rise = taua_utc_rise.to_zone()
    taua_lcl_trans = taua_utc_trans.to_zone()
    taua_lcl_set = taua_utc_set.to_zone()
    
    (taua_ra, taua_dec) = taua_equ.format()
    taua_hrz = taua_equ.to_hrz(lwa_lnlat, utc)
    taua_gal = taua_equ.to_gal(utc)
    (taua_l, taua_b) = taua_gal.format()
    
    taua_sun_ang = sun_equ.angular_separation(taua_equ)
    
    print('---------------------------------------------------------------')
    print('TauA')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (taua_ra, taua_equ.ra))
    print('DEC:               %s (%0.3f)' % (taua_dec, taua_equ.dec)) 
    print('Gal longitude:     %s (%0.3f)' % (taua_l, taua_gal.l))
    print('Gal latitude:      %s (%0.3f)' % (taua_b, taua_gal.b))           
    print('Rise:              %s (%0.3f) [%s]' % (taua_utc_rise, taua_rst.rise, taua_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (taua_utc_trans, taua_rst.transit, taua_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (taua_utc_set, taua_rst.set, taua_lcl_set))
    print('Azimuth:           %0.3f %s' % (taua_hrz.az, astro.hrz_to_nswe(taua_hrz)))
    print('Altitude:          %0.3f' % taua_hrz.alt)
    print('Zenith:            %0.3f' % taua_hrz.zen())
    print('Sun angle:         %0.3f' % taua_sun_ang)

    # calculate B1919+21 phenomena
    
    b1919_j2000_equ = astro.equ_posn(astro.hms(19, 21, 44.80), astro.dms(False, 21, 53, 1.8))
    b1919_equ = astro.get_apparent_posn(b1919_j2000_equ, utc)
    b1919_rst = astro.get_object_rst(utc, lwa_lnlat, b1919_equ)
    (b1919_utc_rise, b1919_utc_set, b1919_utc_trans) = b1919_rst.format()
    b1919_lcl_rise = b1919_utc_rise.to_zone()
    b1919_lcl_trans = b1919_utc_trans.to_zone()
    b1919_lcl_set = b1919_utc_set.to_zone()
    
    (b1919_ra, b1919_dec) = b1919_equ.format()
    b1919_hrz = b1919_equ.to_hrz(lwa_lnlat, utc)
    b1919_gal = b1919_equ.to_gal(utc)
    (b1919_l, b1919_b) = b1919_gal.format()
    
    b1919_sun_ang = sun_equ.angular_separation(b1919_equ)
    
    print('---------------------------------------------------------------')
    print('B1919+21')
    print('---------------------------------------------------------------')
    print('RA:                %s (%0.3f)' % (b1919_ra, b1919_equ.ra))
    print('DEC:               %s (%0.3f)' % (b1919_dec, b1919_equ.dec)) 
    print('Gal longitude:     %s (%0.3f)' % (b1919_l, b1919_gal.l))
    print('Gal latitude:      %s (%0.3f)' % (b1919_b, b1919_gal.b))           
    print('Rise:              %s (%0.3f) [%s]' % (b1919_utc_rise, b1919_rst.rise, b1919_lcl_rise))
    print('Transit:           %s (%0.3f) [%s]' % (b1919_utc_trans, b1919_rst.transit, b1919_lcl_trans))
    print('Set:               %s (%0.3f) [%s]' % (b1919_utc_set, b1919_rst.set, b1919_lcl_set))
    print('Azimuth:           %0.3f %s' % (b1919_hrz.az, astro.hrz_to_nswe(b1919_hrz)))
    print('Altitude:          %0.3f' % b1919_hrz.alt)
    print('Zenith:            %0.3f' % b1919_hrz.zen())
    print('Sun angle:         %0.3f' % b1919_sun_ang)
    
