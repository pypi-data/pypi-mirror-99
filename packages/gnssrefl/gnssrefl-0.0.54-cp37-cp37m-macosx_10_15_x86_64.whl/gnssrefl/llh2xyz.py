# -*- coding: utf-8 -*-
"""
converts XYZ to latlonht
kristine larson
"""
import argparse
import sys

import gnssrefl.gps as g

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("lat", help="latitude (deg) ", type=float)
    parser.add_argument("lon", help="longitude (deg) ", type=float)
    parser.add_argument("height", help="ellipsoidal height (m) ", type=float)
    args = parser.parse_args()

    ie = False
    lat=args.lat; lon=args.lon; height=args.height
    if (lat > 90) or (lat < -90):
        print('invalid latitude. Exiting.') ; ie = True
    if (lon > 360) or (lon < -180):
        print('invalid longitude. Exiting.'); ie = True
    if (height > 10000) or (height < -1000):
        print('Very large or very small height. Exiting.'); ie = True
    if ie:
        sys.exit()

    x,y,z = g.llh2xyz(lat,lon,height)
    print("XYZ (meters) %15.4f %15.4f %15.4f " % ( x,y,z) )

if __name__ == "__main__":
    main()
