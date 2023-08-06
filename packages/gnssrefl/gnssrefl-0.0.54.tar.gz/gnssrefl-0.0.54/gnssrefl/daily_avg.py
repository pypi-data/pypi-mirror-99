# very simple code to pick up all the RH results and make a plot.
# only getting rid of the biggest outliers using a median filter
# Kristine Larson May 2019
import argparse
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

from datetime import date

# my code
import gnssrefl.gps as g
#
# changes to output requested by Kelly Enloe for JN
# two text files will now always made - but you can override the name of the average file via command line

def main():
#   make surer environment variables are set 
    g.check_environ_variables()
    xdir = os.environ['REFL_CODE'] 

# must input start and end year
    parser = argparse.ArgumentParser()
    parser.add_argument("station", help="station name", type=str)
    parser.add_argument("medfilter", help="Median filter for daily RH (m). Start with 0.25 ", type=float)
    parser.add_argument("ReqTracks", help="required number of tracks", type=int)
    parser.add_argument("-txtfile", default=None, type=str, help="Set your own output filename")
    parser.add_argument("-plt", default=None, type=str, help="plt to screen: True or False")
    parser.add_argument("-extension", default=None, type=str, help="extension for solution names")
    parser.add_argument("-year1", default=None, type=str, help="restrict to years starting with")
    parser.add_argument("-year2", default=None, type=str, help="restrict to years ending with")
    parser.add_argument("-fr", default=0, type=int, help="frequency, default is to use all")
    parser.add_argument("-csv", default=None, type=str, help="True if you want csv instead of plain text")
    args = parser.parse_args()
#   these are required
    station = args.station
    medfilter= args.medfilter
    ReqTracks = args.ReqTracks

    fr = args.fr
    if args.csv == None:
        csvformat = False
    else:
        csvformat = True

#   default is to show the plot 
    if (args.plt == None) or (args.plt == 'True'):
        plt2screen = True 
    else:
        plt2screen = False

    if args.extension == None:
        extension = ''
    else:
        extension = args.extension

    if args.year1 == None:
        year1 = 2005
    else:
        year1=int(args.year1)

    if args.year2 == None:
        year2 = 2021
    else:
        year2=int(args.year2)

# where the summary files will be written to
    txtdir = xdir + '/Files' 

    if not os.path.exists(txtdir):
        print('make an output directory', txtdir)
        os.makedirs(txtdir)

    if csvformat:
        alldatafile = txtdir + '/' + station + '_allRH.csv' 
    else:
        alldatafile = txtdir + '/' + station + '_allRH.txt' 

    print('all RH will be written to: ', alldatafile) 
    allrh = open(alldatafile, 'w+')
    allrh.write(" {0:s}  \n".format('% year,doy, RH(m), Month, day, azimuth(deg),freq, satNu, LSP amp,peak2noise' ))
# outliers limit, defined in meters
    howBig = medfilter;
    k=0
# added standard deviation 2020 feb 14, changed n=6
    n=7
# now require it as an input
# you can change this - trying out 80 for now
#ReqTracks = 80
# putting the results in a np.array, year, doy, RH, Nvalues, month, day
    tv = np.empty(shape=[0, n])
    obstimes = []; medRH = []; meanRH = [] 
    plt.figure()
    year_list = np.arange(year1, year2+1, 1)
    #print('Years to examine: ',year_list)
    for yr in year_list:
        direc = xdir + '/' + str(yr) + '/results/' + station + '/' + extension + '/'
        if os.path.isdir(direc):
            all_files = os.listdir(direc)
            print('Number of files in ', yr, len(all_files))
            for f in all_files:
                fname = direc + f
                L = len(f)
        # file names have 7 characters in them ... 
                if (L == 7):
        # check that it is a file and not a directory and that it has something/anything in it
                    try:
                        a = np.loadtxt(fname,skiprows=3,comments='%').T
                        numlines = len(a) 
                        if (len(a) > 0):
                            y = a[0] +a[1]/365.25; rh = a[2] ; doy = int(np.mean(a[1]))
                            frequency = a[10]; azimuth = a[5]; sat = a[3]; amplitude=a[6]
                            peak2noise = a[13]
        # change from doy to month and day in datetime
                            d = datetime.date(yr,1,1) + datetime.timedelta(doy-1)
                            medv = np.median(rh)
                            # 0 means use all frequencies.  otherwise, you can specify 
                            if fr == 0:
                                cc = (rh < (medv+howBig))  & (rh > (medv-howBig))
                            else:
                                cc = (rh < (medv+howBig))  & (rh > (medv-howBig)) & (frequency == fr)
                            good =rh[cc]; goodT =y[cc]
                            gazim = azimuth[cc]; gsat = sat[cc]; gamp = amplitude[cc]; gpeak2noise = peak2noise[cc]
                            gfreq = frequency[cc]
                            
                            NG = len(good)
                            if (NG > 0):
                                if csvformat:
                                    for ijk in range(0,NG):
                                        allrh.write(" {0:4.0f},  {1:3.0f},{2:7.3f}, {3:2.0f}, {4:2.0f},{5:6.1f},{6:4.0f},{7:4.0f},{8:6.2f},{9:6.2f}\n".format(yr, 
                                            doy, good[ijk],d.month, d.day, gazim[ijk], gfreq[ijk], gsat[ijk],gamp[ijk],gpeak2noise[ijk]))
                                else:
                                    for ijk in range(0,NG):
                                        allrh.write(" {0:4.0f}   {1:3.0f} {2:7.3f} {3:2.0f} {4:2.0f} {5:6.1f} {6:4.0f} {7:4.0f} {8:6.2f} {9:6.2f}\n".format(yr, 
                                            doy, good[ijk],d.month, d.day, gazim[ijk], gfreq[ijk], gsat[ijk],gamp[ijk],gpeak2noise[ijk]))

        # only save if there are some minimal number of values
                            if (len(good) > ReqTracks):
                                rh = good
                                obstimes.append(datetime.datetime(year=yr, month=d.month, day=d.day, hour=12, minute=0, second=0))
                                medRH =np.append(medRH, medv)
                                plt.plot(goodT, good,'b.')
            # store the meanRH after the outliers are removed using simple median filter
                                meanRHtoday = np.mean(good)
                                stdRHtoday = np.std(good)
                                meanRH =np.append(meanRH, meanRHtoday)
            # add month and day just cause some people like that instead of doy
            # added standard deviation feb14, 2020
                                newl = [yr, doy, meanRHtoday, len(rh), d.month, d.day, stdRHtoday]
                                tv = np.append(tv, [newl],axis=0)
                                k += 1
                            else:
                                print('not enough retrievals on ', yr, d.month, d.day, len(good))
                    except:
                        print('problem reading ', fname, ' so skipping it')
        else:
            abc = 0; # dummy line
            #print('that directory does not exist - so skipping')
    plt.ylabel('Reflector Height (m)')
    plt.title('GNSS station: ' + station)
    plt.gca().invert_yaxis()
    plt.grid()
    fig,ax=plt.subplots()
    ax.plot(obstimes,meanRH,'b.')
    fig.autofmt_xdate()
    plt.ylabel('Reflector Height (m)')
    today = str(date.today())
    plt.title(station.upper() + ': Daily Mean Reflector Height, Computed ' + today)
    plt.grid()
    plt.gca().invert_yaxis()
    pltname = txtdir + '/' + station + '_RH.png'
    plt.savefig(pltname)
    print('Daily average RH png file saved as: ', pltname)

    fig,ax=plt.subplots()
    plt.plot(obstimes, tv[:,3],'b.')
    fig.autofmt_xdate()
    plt.title('Number of values used in the daily average')
    plt.grid()
    

    # close the file with all the RH values'
    allrh.close()

    # default is to show the plot
    if plt2screen:
        plt.show()

    if args.txtfile == None:
        if csvformat:
            outfile = txtdir + '/' + station + '_dailyRH.csv' 
        else:
        # use default  filename for the average
            outfile = txtdir + '/' + station + '_dailyRH.txt' 
    else:
        txtfile = args.txtfile
        # use filename provided by the user
        outfile = txtdir + '/' + txtfile
    print('Daily average RH will be written to: ', outfile)
    # to avoid indenting again,  use True
    if True:
        # sort the time tags
        ii = np.argsort(obstimes)
    # apply time tags to a new variable
        ntv = tv[ii,:]
        N,M = np.shape(ntv)
        xxx = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        fout = open(outfile, 'w+')
    # change comment value from # to %
        fout.write("{0:28s} \n".format( '% calculated on ' + xxx ))
        fout.write("% year doy   RH    numval month day RH-sigma\n")
        fout.write("% year doy   (m)                      (m)\n")
        fout.write("% (1)  (2)   (3)    (4)    (5)  (6)   (7)\n")
        if csvformat:
            for i in np.arange(0,N,1):
                fout.write(" {0:4.0f},  {1:3.0f},{2:7.3f},{3:3.0f},{4:4.0f},{5:4.0f},{6:7.3f} \n".format(ntv[i,0], 
                    ntv[i,1], ntv[i,2],ntv[i,3],ntv[i,4],ntv[i,5],ntv[i,6]))
        else:
            for i in np.arange(0,N,1):
                fout.write(" {0:4.0f}   {1:3.0f} {2:7.3f} {3:3.0f} {4:4.0f} {5:4.0f} {6:7.3f} \n".format(ntv[i,0], 
                    ntv[i,1], ntv[i,2],ntv[i,3],ntv[i,4],ntv[i,5],ntv[i,6]))
        fout.close()

if __name__ == "__main__":
    main()
