import matplotlib.pyplot as plt
import matplotlib
from random import *
import numpy as np


""" CLASSES """


""" FUNCTIONS """
def parseFile(filename):
    #set up for parsing file
    _latency = []
    _loss = []
    _throughput = []
    _avglatency = []
    _avgloss = []
    _avgthroughput = []
    sum = 0

    #read in each QoS line, and store appropriately
    for line in open("video_startupdelays.txt"):
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
        for num in range(2, int(cur[2]) + 2 + 1): # range is inclusive, and starts from cur[2]
            qos.append((tupx, int(cur[num])))
            sum += int(cur[num])
        avgqos.append((tupx, (sum / int(cur[2]))))

    return _latency, _loss, _throughput, _avglatency, _avgloss, _avgthroughput

def splitList(sourceList):
    listx = []
    listy = []
    for num in range(0, len(sourceList)):
        listx.append(sourceList[num][1])
        listy.append(sourceList[num][0])
    print listy
    print listx
    print "============================"
    return listx, listy

def analyze1(_latency, _loss, _throughput):
    plt.title("Comparison type 1")
    plt.ylabel("QoS value")
    plt.xlabel("average QoE")
    print _latency
    plotx, ploty = splitList(_latency)
    plt.plot(np.asarray(plotx), np.asarray(ploty), label = "Latency")
    print _loss
    plotx, ploty = splitList(_loss)
    plt.plot(np.asarray(plotx), np.asarray(ploty), label = "Loss")
    print _throughput
    plotx, ploty = splitList(_throughput)
    plt.plot(np.asarray(plotx), np.asarray(ploty), label = "Throughput")
    plt.legend()
    plt.show()
    return

def analyze2(_latency, _loss, _throughput):
    print "Not yet finished"

""" PROGRAM BEGINS HERE """
latency, loss, throughput, avglatency, avgloss, avgthroughput = parseFile("video_startupdelays.txt")

analyze1(avglatency, avgloss, avgthroughput)

analyze2(latency, loss, throughput)
