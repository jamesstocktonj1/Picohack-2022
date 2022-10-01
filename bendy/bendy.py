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


class Bendy:
    def __init__(self):
        self.data = []

    def inject_data(self):
        self.data = []

    def load(self, filename):
        data_file = open(filename, "r")
        data_xml = parse(data_file)
        data_file.close()

        element_list = data_xml.getElementsByTagName("trkpt")

        for e in element_list:
            xTemp = float(e.getAttribute("lon"))
            yTemp = float(e.getAttribute("lat"))
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
        average_quality = int(len(self.data) / 25)
        bend_threshold = 0

        # point = [startPoint, endPoint, bendIndex]
        significant_points = []

        for d, i in zip(self.data, range(len(self.data) - average_quality)):

            if (i % average_quality) == 0:
                significant_points.append([d[0], d[1], self.bend_index(i, i+average_quality)])

        return significant_points

    def filter_significant(self, significant_points):
        filter_significant_points = []

        sorted_points = list(p[2] for p in significant_points)
        sorted_points.sort()
        filter_threshold = sorted_points[int(len(sorted_points) * 0.9)]

        for p in significant_points:
            if p[2] > filter_threshold:
                filter_significant_points.append(p)

        return filter_significant_points


    def show_significant(self):
        road_fig = plt.subplot(1, 1, 1)

        xData = list(d[0] for d in self.data)
        yData = list(d[1] for d in self.data)
        bendData = self.analyse()
        filterData = self.filter_significant(bendData)

        for p in filterData:
            road_fig.annotate("Index: {}".format(p[2]), [p[0], p[1]])


        road_fig.plot(xData, yData)
        road_fig.set(xlim=(min(xData), max(xData)), ylim=(min(yData), max(yData)))
        
        plt.show()

    def show_bend(self):
        average_quality = int(len(self.data) / 25)

        # point = [startPoint, endPoint, bendIndex]
        significant_points = []

        for d, i in zip(self.data, range(len(self.data) - average_quality)):

            if (i % average_quality) == 0:
                significant_points.append([d[0], d[1], self.bend_index(i, i+average_quality)])

        return significant_points


        road_fig = plt.subplot(1, 1, 1)

        xData = list(d[0] for d in self.data)
        yData = list(d[1] for d in self.data)
        bendData = self.bend_point()
        #filterData = self.filter_significant(bendData)

        for p in bendData:
            road_fig.annotate("Index: {}".format(p[2]), [p[0], p[1]])
        
        road_fig.plot(xData, yData)
        road_fig.set(xlim=(min(xData), max(xData)), ylim=(min(yData), max(yData)))
        
        plt.show()

    def show(self):
        road_fig = plt.subplot(1, 1, 1)

        xData = list(d[0] for d in self.data)
        yData = list(d[1] for d in self.data)
        bendData = self.analyse()
        print(len(xData))

        road_fig.plot(xData, yData)
        road_fig.set(xlim=(min(xData), max(xData)), ylim=(min(yData), max(yData)))
        
        plt.show()