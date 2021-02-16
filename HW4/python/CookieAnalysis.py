#! /usr/bin/env python

# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker

from scipy.special import erf


# import our MySort class from python/MySort.py file
from MySort import MySort

# main function for our CookieAnalysis Python code
if __name__ == "__main__":

    haveInput = False

    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            continue

        InputFile = sys.argv[i]
        haveInput = True

    if '-h' in sys.argv or '--help' in sys.argv or not haveInput:
        print ("Usage: %s [options] [input file]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print
        sys.exit(1)

    Nmeas = 1
    times = []
    times_avg = []
    lt = 0
    lt_avg = 0

    need_rate = True

    with open(InputFile) as ifile:
        for line in ifile:
            if need_rate:
                need_rate = False
                rate = float(line)
                continue

            lineVals = line.split()
            Nmeas = len(lineVals)
            t_avg = 0
            for v in lineVals:
                t_avg += float(v)
                times.append(float(v))
                lt += 1

            t_avg /= Nmeas
            times_avg.append(t_avg)
            lt_avg += 1

    Sorter = MySort()

    times = Sorter.DefaultSort(times)
    times_avg = Sorter.DefaultSort(times_avg)
    # try some other methods! see how long they take
    # times_avg = Sorter.BubbleSort(times_avg)
    # times_avg = Sorter.InsertionSort(times_avg)
    # times_avg = Sorter.QuickSort(times_avg)

    # should move below snippets to functions or maybe another module

    # calculate and store indexes of quantiles (tq[0] being the index of
    # times[] containing median -3sigma, tq[1] -> -2sigma, ...)
    tq_avg = []
    tq = []
    for sigma in range(1,4):
        IDR = erf(sigma/math.sqrt(2))/2
        tq_avg.insert(0,int(lt_avg*(0.5-IDR)))
        tq_avg.append(  int(lt_avg*(0.5+IDR)))
        tq.    insert(0,int(lt*(0.5-IDR)))
        tq.    append(  int(lt*(0.5+IDR)))

    # calculate FD bin-widths
    # bw_avg = 2*(times[int(lt_avg*0.75)] - times[int(lt_avg*0.25)]) / np.cbrt(lt_avg)
    # bw     = 2*(times[int(lt*0.75)]     - times[int(lt*0.25)])     / np.cbrt(lt)
    # number of bins from bw's
    # num_bins_avg = int((times_avg[lt_avg-1] - times_avg[0]) / bw_avg)
    # num_bins     = int((times[lt-1]         - times[0])     / bw)

    # can't get axvline label text to print for some reason, been at this for HOURS, so I'm giving up
    # configure and save times_avg plot
    plt.figure(1)
    plt.hist(times_avg, 200, density = 1, alpha = 0.5)
    for sigma in range (-3,4):
        if sigma < 0:
            plt.axvline(times_avg[tq_avg[sigma+3]])
            #plt.text(times_avg[tq_avg[sigma+3]] + 0.1, 0, '{}σ = {}'.format(sigma, times_avg[tq_avg[sigma+3]]),rotation=90)
        elif sigma == 0:
            plt.axvline(times_avg[int(lt_avg*0.5)])
            #plt.text(times_avg[int(lt_avg*0.5)] + 0.1, 0, 'median = {}'.format(times_avg[int(lt_avg*0.5)]),rotation=90)
        else:
            plt.axvline(times_avg[tq_avg[sigma+2]])
            #plt.text(times_avg[tq_avg[sigma+2]] + 0.1, 0, '{}σ = {}'.format(sigma, times_avg[tq_avg[sigma+2]]),rotation=90)
    plt.yscale('log')
    plot_title = "{} measurements / experiment with rate {}".format(Nmeas, rate)
    plt.title(plot_title)
    plt.xlabel('Average time between missing cookies [days]')
    plt.ylabel('Probability')
    plt.savefig('times_avg.png')

    # configure and save times plot
    plt.figure(2)
    plt.hist(times, 200, density = 1, alpha = 0.5)
    plt.yscale('log')
    plot_title = "rate of {} cookies / day".format(rate)
    plt.title(plot_title)
    plt.xlabel('Time between missing cookies [days]')
    plt.ylabel('Probability')
    plt.savefig('times.png')
