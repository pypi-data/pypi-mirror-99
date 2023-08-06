#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#   Copyright (C) 2021  Andrew Bauer
#   Copyright (C) 2014  Enno Rodegerdts

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
# 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.

# Standard library imports
import os
import sys
from sysconfig import get_path  # new in python 3.2
import site
import time
import datetime

# Local application imports
from sfalmanac.lib import tables as tables
from sfalmanac.lib import suntables as suntables
from sfalmanac.lib import config as config
from sfalmanac.lib import increments as increments
from sfalmanac.lib.alma_skyfield import init_sf as init_sf

##Main##
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

if config.ephndx not in set([0, 1, 2]):
    print("Error - Please choose a valid ephemeris in config.py")
    sys.exit(0)

d = datetime.datetime.utcnow().date()
first_day = datetime.date(d.year, d.month, d.day)

#first_day = datetime.date(2023, 6, 24)	# for testing a specific date
#d = first_day							# for testing a specific date

sday = "{:02d}".format(d.day)       # sday = "%02d" % d.day
smth = "{:02d}".format(d.month)     # smth = "%02d" % d.month
syr  = "{}".format(d.year)          # syr  = "%s" % d.year
symd = syr + smth + sday
sdmy = sday + "." + smth + "." + syr
yrmin = config.ephemeris[config.ephndx][1]
yrmax = config.ephemeris[config.ephndx][2]

mfp = sys.modules['__main__'].__file__  # main module filepath
pkg = mfp.split(os.path.sep)[-2]        # this package name

spad = ""
spdf = ""
spcf = ""
if sys.platform.startswith('win'):  # Windows 10 (also in 'venv' virtual environment)
    spad = sys.exec_prefix + "\\Lib\\site-packages\\" + pkg + "\\astro-data\\"  # path to downloaded data
    spdf = sys.exec_prefix + "\\Lib\\site-packages\\" + pkg + "\\data\\"  # path to data files
    spcf = sys.exec_prefix + "\\Lib\\site-packages\\" + pkg + "\\lib\\"   # path to config.py
else:                               # POSIX (Linux & Mac OS X)
    if site.ENABLE_USER_SITE:
        spad = site.USER_SITE + "/" + pkg + "/astro-data/"
        spdf = site.USER_SITE + "/" + pkg + "/data/"
        spcf = site.USER_SITE + "/" + pkg + "/lib/"
    else:   # in case we're in a virtual environment (venv)
        spad = get_path("purelib") + "/" + pkg + "/astro-data/"
        spdf = get_path("purelib") + "/" + pkg + "/data/"
        spcf = get_path("purelib") + "/" + pkg + "/lib/"

dfra = spdf + "Ra.jpg"
dfcm = spdf + "croppedmoon.png"
df180 = spdf + "A4chart0-180_P.pdf"
df360 = spdf + "A4chart180-360_P.pdf"

ts = init_sf(spad)      # in alma_skyfield
print(" Path to config.py:  {}".format(spcf))
print(" Downloaded data in: {}".format(spad))

if config.pgsz not in set(['A4', 'Letter']):
    print("Please choose a valid paper size in config.py")
    sys.exit(0)

s = input("""\nWhat do you want to create?:\n
    1   Full nautical almanac   (for a year)
    2   Just tables for the sun (for a year)
    3   Nautical almanac   - 6 days from today
    4   Tables for the sun - 30 days from today
    5   "Increments and Corrections" tables (static data)
""")

if s in set(['1', '2', '3', '4', '5']):
    if int(s) < 3:
        print("Please enter the year you want to create the nautical almanac")
        years = input("  for as yyyy ... or the FIRST and LAST year as yyyy-yyyy\n")
        if len(years)== 4:
            yearfr = years
            yearto = years
        elif len(years) == 9 and years[4] == '-':
            yearfr = years[0:4]
            yearto = years[5:9]
        else:
            print("Error! Invalid format")
            sys.exit(0)
        
        if str(yearfr).isnumeric():
            if yrmin <= int(yearfr) <= yrmax:
                first_day = datetime.date(int(yearfr), 1, 1)
            else:
                print("!! Please pick a year between {} and {} !!".format(yrmin,yrmax))
                sys.exit(0)
        else:
            print("Error! First year is not numeric")
            sys.exit(0)

        if str(yearto).isnumeric():
            if yrmin <= int(yearto) <= yrmax:
                first_day_to = datetime.date(int(yearto), 1, 1)
            else:
                print("!! Please pick a year between {} and {} !!".format(yrmin,yrmax))
                sys.exit(0)
            if int(yearto) < int(yearfr):
                print("Error! The LAST year must be later than the FIRST year")
                sys.exit(0)
        else:
            print("Error! Last year is not numeric")
            sys.exit(0)

    if s != '5':
        tsin = input("""What table style is required?:\n
        t   Traditional
        m   Modern
""")
        ff = '_'
        DecFmt = ''
        config.tbls = tsin[0:1]	# table style
        config.decf = tsin[1:2]	# Declination format
        if config.tbls != 'm':
            config.tbls = ''		# anything other than 'm' is traditional
            ff = ''
        if config.decf != '+':		# Positive/Negative Declinations
            config.decf = ''		# USNO format for Declination
        else:
            DecFmt = '[old]'

    if s == '1':
        print("Take a break - this computer needs some time for cosmic meditation.")
##        config.initLOG()		# initialize log file
        for yearint in range(int(yearfr),int(yearto)+1):
            start = time.time()
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the nautical almanac for the year {}".format(year)
            print(msg)
##            config.writeLOG(msg)
            first_day = datetime.date(yearint, 1, 1)
            filename = "almanac{}{}.tex".format(ff,year+DecFmt)
            outfile = open(filename, mode="w", encoding="utf8")
            outfile.write(tables.almanac(first_day,122,df180,df360,dfcm))
            outfile.close()
            stop = time.time()
            msg = "execution time = {:0.2f} seconds".format(stop-start) # msg = "execution time = %0.2f seconds" %(stop-start)
            print(msg)
##            config.writeLOG("\n\n" + msg + "\n")
            print()
            command = 'pdflatex {}'.format(filename)
            os.system(command)
            print("finished creating nautical almanac for {}".format(year))
            os.remove(filename)
            if os.path.isfile("almanac{}{}.log".format(ff,year+DecFmt)):
                os.remove("almanac{}{}.log".format(ff,year+DecFmt))
            if os.path.isfile("almanac{}{}.aux".format(ff,year+DecFmt)):
                os.remove("almanac{}{}.aux".format(ff,year+DecFmt))
##        config.closeLOG()

    elif s == '2':
        for yearint in range(int(yearfr),int(yearto)+1):
            year = "{:4d}".format(yearint)  # year = "%4d" %yearint
            msg = "\nCreating the sun tables only for the year {}".format(year)
            print(msg)
            first_day = datetime.date(yearint, 1, 1)
            filename = "sunalmanac{}{}.tex".format(ff,year+DecFmt)
            outfile = open(filename, mode="w", encoding="utf8")
            outfile.write(suntables.almanac(first_day,25,dfra))
            outfile.close()
            command = 'pdflatex {}'.format(filename)
            os.system(command)
            print("finished creating sun tables for {}".format(year))
            os.remove(filename)
            if os.path.isfile("sunalmanac{}{}.log".format(ff,year+DecFmt)):
                os.remove("sunalmanac{}{}.log".format(ff,year+DecFmt))
            if os.path.isfile("sunalmanac{}{}.aux".format(ff,year+DecFmt)):
                os.remove("sunalmanac{}{}.aux".format(ff,year+DecFmt))

    elif s == '3':
##        config.initLOG()		# initialize log file
        start = time.time()
        config.stopwatch = 0.0      # 00000
        msg = "\nCreating nautical almanac tables - from {}".format(sdmy)
        print(msg)
        filename = "almanac{}{}.tex".format(ff,symd+DecFmt)
        outfile = open(filename, mode="w", encoding="utf8")
        outfile.write(tables.almanac(first_day,2,df180,df360,dfcm))
        outfile.close()
        stop = time.time()
        msg1 = "execution time = {:0.2f} seconds".format(stop-start) # msg1 = "execution time = %0.2f seconds" %(stop-start)
        print(msg1)
        msg2 = "stopwatch      = {:0.2f} seconds".format(config.stopwatch)
        print(msg2)                 # 00000
        msg3 = "(stopwatch shows the time spent in the 'almanac.find_discrete' function)"
        print(msg3)
        print()
##        config.writeLOG('\n\n' + msg1 + '\n' + msg2 + '\n' + msg3)
##        config.closeLOG()
        command = 'pdflatex {}'.format(filename)
        os.system(command)
        print("finished")
        os.remove(filename)
        if os.path.isfile("almanac{}{}.log".format(ff,symd+DecFmt)):
            os.remove("almanac{}{}.log".format(ff,symd+DecFmt))
        if os.path.isfile("almanac{}{}.aux".format(ff,symd+DecFmt)):
            os.remove("almanac{}{}.aux".format(ff,symd+DecFmt))

    elif s == '4':
        msg = "\nCreating the sun tables only - from {}".format(sdmy)
        print(msg)
        filename = "sunalmanac{}{}.tex".format(ff,symd+DecFmt)
        outfile = open(filename, mode="w", encoding="utf8")
        outfile.write(suntables.almanac(first_day,2,dfra))
        outfile.close()
        command = 'pdflatex {}'.format(filename)
        os.system(command)
        print("finished")
        os.remove(filename)
        if os.path.isfile("sunalmanac{}{}.log".format(ff,symd+DecFmt)):
            os.remove("sunalmanac{}{}.log".format(ff,symd+DecFmt))
        if os.path.isfile("sunalmanac{}{}.aux".format(ff,symd+DecFmt)):
            os.remove("sunalmanac{}{}.aux".format(ff,symd+DecFmt))

    elif s == '5':
        msg = "\nCreating the Increments and Corrections tables"
        print(msg)
        fn = "inc"
        filename = fn + ".tex"
        outfile = open(filename, mode="w", encoding="utf8")
        outfile.write(increments.makelatex())
        outfile.close()
        command = 'pdflatex {}'.format(filename)
        os.system(command)
        print("finished")
        os.remove(fn + ".tex")
        os.remove(fn + ".log")
        os.remove(fn + ".aux")

else:
    print("Error! Choose 1, 2, 3, 4 or 5")
