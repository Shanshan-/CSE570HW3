import matplotlib.pyplot as plt
import matplotlib
from random import *
import numpy as np
import math
from scipy.optimize import curve_fit

""" CLASSES """


""" FUNCTIONS """
#parses the indicated file and stores the contents into six different lists based on QoS type and statistic type
def parseFile(filename, nulVal):
    #set up for parsing file
    _latency = []
    _loss = []
    _throughput = []
    _avglatency = []
    _avgloss = []
    _avgthroughput = []

    #read in each QoS line, and store appropriately
    for line in open(filename):
        cur = line.split(" ")

        #determine QoS type
        if not cur: # list is empty
            print "Finished parsing file"
        elif cur[0] == "latency":
            qos = _latency
            avgqos = _avglatency
        elif cur[0] == "loss":
            qos = _loss
            avgqos = _avgloss
        elif cur[0] == "throughput":
            qos = _throughput
            avgqos = _avgthroughput
        else:
            continue

        #parse line and store
        tupx = cur[1]
        sum = 0
        total = int(cur[2])
        for num in range(3, int(cur[2]) + 3): # range is inclusive, and starts from cur[2]
            val = float(cur[num])
            if val == nulVal:
                total -= 1;
                continue
            qos.append((tupx, val))
            sum += val
        if total != 0:
            avgqos.append((tupx, (sum / total)))

    return _latency, _loss, _throughput, _avglatency, _avgloss, _avgthroughput

#splits a list of tuples into two lists
def splitList(sourceList):
    listx = []
    listy = []
    for num in range(0, len(sourceList)):
        listx.append(sourceList[num][0]) #qos value for analysis 1
        listy.append(sourceList[num][1]) #qoe value for analysis 2
    return listx, listy

#plot the average QoE values for each individual QoS
def analyzeAvg(_latency, _loss, _throughput, title):
    #generate datasets
    plotLatencyx, plotLatencyy = splitList(_latency)
    plotLossx, plotLossy = splitList(_loss)
    plotThroughputx, plotThroughputy = splitList(_throughput)
    plt.figure(figsize=(15, 10))
    plt.suptitle(title)

    #display latency
    plt.subplot(221)
    plt.title("Latency")
    plt.xlabel("QoS value (ms)")
    plt.ylabel("Average QoE (ms)")
    plt.plot(np.asarray(plotLatencyx), np.asarray(plotLatencyy), label = "Latency")


    #display loss
    plt.subplot(222)
    plt.title("Loss")
    plt.xlabel("QoS value (%)")
    plt.ylabel("average QoE (ms)")
    plt.plot(np.asarray(plotLossx), np.asarray(plotLossy), label = "Loss")

    #display throughput
    plt.subplot(223)
    plt.title("Throughput")
    plt.xlabel("QoS value (Mbps)")
    plt.ylabel("average QoE (ms)")
    plt.plot(np.asarray(plotThroughputx), np.asarray(plotThroughputy), label = "Throughput")

    #display all together
    plt.subplot(224)
    plt.title("All")
    plt.xlabel("QoS value")
    plt.ylabel("average QoE")
    plt.plot(np.asarray(plotLatencyx), np.asarray(plotLatencyy), label = "Latency (ms)")
    plt.plot(np.asarray(plotLossx), np.asarray(plotLossy), label = "Loss (%)")
    plt.plot(np.asarray(plotThroughputx), np.asarray(plotThroughputy), label = "Throughput (Mbps)")
    plt.legend(loc = "center right", fontsize = "small")

    #show all
    plt.subplots_adjust(hspace = .5)
    plt.savefig(title + " QoS effect on QoE.jpg")
    #plt.show()
    return

#plot the QoE values for each individual QoS, and fit the IQX hypothesis to it
def analyzeScatter(_latency, _loss, _throughput, title):
    #generate datasets
    plotLatencyx, plotLatencyy = splitList(_latency)
    plotLossx, plotLossy = splitList(_loss)
    plotThroughputx, plotThroughputy = splitList(_throughput)
    plt.figure(figsize=(15, 10))
    plt.suptitle(title)

    #display latency
    plotx = np.asarray(plotLatencyx)
    ploty = np.asarray(plotLatencyy)
    plt.subplot(221)
    plt.title("Latency")
    plt.xlabel("QoS value (ms)")
    plt.ylabel("Average QoE (ms)")
    plt.scatter(plotx, ploty, label = "Latency")
    plt.legend()

    #display loss
    plt.subplot(222)
    plt.title("Loss")
    plt.xlabel("QoS value (%)")
    plt.ylabel("average QoE (ms)")
    plt.scatter(np.asarray(plotLossx), np.asarray(plotLossy), label = "Loss")

    #display throughput
    plt.subplot(223)
    plt.title("Throughput")
    plt.xlabel("QoS value (Mbps)")
    plt.ylabel("average QoE (ms)")
    plt.scatter(np.asarray(plotThroughputx), np.asarray(plotThroughputy), label = "Throughput")

    #display all together
    plt.subplot(224)
    plt.title("All")
    plt.xlabel("QoS value")
    plt.ylabel("average QoE")
    plt.scatter(np.asarray(plotLatencyx), np.asarray(plotLatencyy), label = "Latency (ms)", color = "blue")
    plt.scatter(np.asarray(plotLossx), np.asarray(plotLossy), label = "Loss (%)", color = "green")
    plt.scatter(np.asarray(plotThroughputx), np.asarray(plotThroughputy), label = "Throughput (Mbps)", color = "red")
    plt.legend(loc = "center right", fontsize = "small")

    #show all
    plt.subplots_adjust(hspace = .5)
    plt.savefig(title + " QoS effect on QoE.jpg")
    #plt.show()
    return

#IQX hypothesis
def func(x, a, b, c):
    return a + b * ( math.e ** ( -c * x ))
    return a * ( math.e ** ( -b * x )) + c

#plot the QoE values for each individual QoS, and fit the IQX hypothesis to it
def analyzePlot(_latency, _loss, _throughput, title):
    #generate datasets
    plotLatencyx, plotLatencyy = splitList(_latency)
    plotLossx, plotLossy = splitList(_loss)
    plotThroughputx, plotThroughputy = splitList(_throughput)
    plt.figure(figsize=(15, 10))
    plt.suptitle(title)

    #display latency
    ploty = np.asarray(plotLatencyx, dtype = float)
    plotx = np.asarray(plotLatencyy, dtype = float)
    plt.subplot(221)
    plt.title("Latency")
    plt.xlabel("QoS value (ms)")
    plt.ylabel("Average QoE (ms)")
    popt, pcov = curve_fit(func, plotx, ploty)
    plt.plot(plotx, ploty, label = "Latency")
    print popt
    plt.plot(plotx, func(plotx, *popt), label = "Fitted Latency")
    plt.legend()

    #display loss
    ploty = np.asarray(plotLossx, dtype = float)
    plotx = np.asarray(plotLossy, dtype = float)
    plt.subplot(222)
    plt.title("Loss")
    plt.xlabel("QoS value (%)")
    plt.ylabel("average QoE (ms)")
    popt, pcov = curve_fit(func, plotx, ploty)
    plt.plot(plotx, ploty, label = "Loss")
    print popt
    plt.plot(plotx, func(plotx, *popt), label = "Fitted Loss")
    plt.legend()

    #display throughput
    ploty = np.asarray(plotThroughputx, dtype = float)
    plotx = np.asarray(plotThroughputy, dtype = float)
    plt.subplot(223)
    plt.title("Throughput")
    plt.xlabel("QoS value (Mbps)")
    plt.ylabel("average QoE (ms)")
    popt, pcov = curve_fit(func, plotx, ploty)
    plt.plot(plotx, ploty, label = "Throughput")
    print popt
    plt.plot(plotx, func(plotx, *popt), label = "Fitted Throughput")
    plt.legend()

    #show all
    plt.subplots_adjust(hspace = .5)
    plt.savefig(title + " test.jpg")
    #plt.show()
    return

""" PROGRAM BEGINS HERE """
"""
#question 1
latency, loss, throughput, avglatency, avgloss, avgthroughput = parseFile("video_startupdelays.txt", 20000)
analyzeAvg(avglatency, avgloss, avgthroughput, "Average Video")
analyze(latency, loss, throughput, "Video")
latency, loss, throughput, avglatency, avgloss, avgthroughput = parseFile("webpage_loadtimes.txt", 30000)
analyzeAvg(avglatency, avgloss, avgthroughput, "Average Web")
analyze(latency, loss, throughput, "Web")
"""

#question 3
latency, loss, throughput, avglatency, avgloss, avgthroughput = parseFile("video_startupdelays.txt", 20000)
analyzePlot(avglatency, avgloss, avgthroughput, "Plotting")