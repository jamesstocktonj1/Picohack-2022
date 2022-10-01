# Bendy Road File
# This takes in the .gpx data and converts it into a more usable format and runs analysis on the bendyness of the road.


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


    def analyse(self):
        pass

    def show(self):
        print(self.data)

        road_fig = plt.subplot(1, 1, 1)

        xData = list(d[0] for d in self.data)
        yData = list(d[1] for d in self.data)

        road_fig.plot(xData, yData)

        road_fig.set(xlim=(min(xData), max(xData)), ylim=(min(yData), max(yData)))
        
        plt.show()