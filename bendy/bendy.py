# Bendy Road File
# This takes in the .gpx data and converts it into a more usable format and runs analysis on the bendyness of the road.


from tracemalloc import start
import matplotlib.pyplot as plt
from xml.dom.minidom import parse


# Data Format
# data = [point]
# point = [x, y, elevation]


def tangent(startPoint, endPoint):
    pass


class Road:
    def __init__(self):
        self.data = []

    def inject_data(self):
        self.data = []

    def load(self, filename):
        data_file = open(filename, "r")
        data_xml = parse(data_file)
        data_file.close()

        element_list = data_xml.getElementsByTagName("trkpt")

        xStart = float(element_list[0].getAttribute("lat"))
        yStart = float(element_list[0].getAttribute("lon"))

        for e in element_list:
            xTemp = xStart - float(e.getAttribute("lat"))
            yTemp = yStart - float(e.getAttribute("lon"))
            self.data.append([xTemp, yTemp])

    def bend_point(self, startIndex, endIndex):
        startPoint = self.data[startIndex]
        endPoint = self.data[endIndex]

        midIndex = startIndex + int(0.5 * (endIndex - startIndex))
        lineMidPoint = self.data[midIndex]

        tanMidPoint = [
            startPoint[0] + (0.5 * (endPoint[0] - startPoint[0])),
            startPoint[1] + (0.5 * (endPoint[1] - startPoint[1]))
        ]

        return lineMidPoint, tanMidPoint

    def bend_index(self, startIndex, endIndex):

        lineMid, tanMid = self.bend_point(startIndex, endIndex)
        #dX = (tanMid[0] - lineMid[0])
        #dY = (tanMid[1] - lineMid[1])
        dX = (lineMid[0] - tanMid[0])
        dY = (lineMid[1] - tanMid[1])

        lineLen = ((dX**2) + (dY**2)) ** 0.5

        return lineLen

    def analyse(self):
        average_quality = 200
        bend_threshold = 0

        # point = [startPoint, endPoint, bendIndex]
        significant_points = []

        for d, i in zip(self.data, range(len(self.data) - average_quality)):

            if (i % average_quality) == 0:
                significant_points.append(self.bend_index(i, i+average_quality))

        return sum(significant_points) / len(significant_points)

    def show(self):
        road_fig = plt.subplot(1, 1, 1)

        xData = list(d[0] for d in self.data)
        yData = list(d[1] for d in self.data)
        bendData = self.analyse()
        print(bendData)

        road_fig.plot(xData, yData)
        road_fig.set(xlim=(min(xData), max(xData)), ylim=(min(yData), max(yData)))
        
        plt.show()