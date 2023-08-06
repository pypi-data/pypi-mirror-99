# -*- coding: utf-8 -*-
"""
converts ymd to doy
kristine larson
Updated: April 3, 2019
"""
import argparse
import sys

import gnssrefl.gps as g

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="year ", type=int)
    parser.add_argument("doy", help="doy", type=int)

    args = parser.parse_args()
    year = args.year
    doy = args.doy
    if (year < 1977):
        print('Year has to be after first GPS satellite launch, but you chose ', year)
        sys.exit()
    if ((doy < 1) or (doy > 366)):
        print('Illegal day of year', doy)
        sys.exit()

    year,month,day=g.ydoy2ymd(year, doy)

    print('month ', month, ' day ', day)


if __name__ == "__main__":
    main()
