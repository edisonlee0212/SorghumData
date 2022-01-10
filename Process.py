import copy
import math
import utm
import numpy as np
import pandas as pd
import random
from geopy.distance import distance
import csv
from pyproj import Proj, transform

proj_4326 = Proj(init='epsg:4326')
proj_2151 = Proj(init='epsg:2152')


def utm_to_latlon(easting, northing):
    lon, lat = transform(proj_2151, proj_4326, easting, northing)
    return lon, lat


def latlon_to_utm(lon, lat):
    easting, northing = transform(proj_4326, proj_2151, lon, lat)
    return easting, northing

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

class Processor:
    def __init__(self):
        self.data = None
        self.center = None
        self.distance_pair = []
        self.xMin = 99999
        self.xMax = -99999
        self.yMin = 99999
        self.yMax = -99999

    @staticmethod
    def sortFunc(e):
        return e[1]

    def import_data(self, path):
        self.data = pd.read_csv(path, index_col=False)
        avgx = 0.0
        avgy = 0.0
        data_count = self.data.count(axis=0)
        for index, row in self.data.iterrows():
            [utm_east, utm_north, utm_zone, utm_letter] = utm.from_latlon(row["lat"], row["lon"])
            avgx += utm_east / data_count[1]
            avgy += utm_north / data_count[1]
        self.center = [avgx, avgy]
        self.xMin = 9999999
        self.xMax = -9999999
        self.yMin = 9999999
        self.yMax = -9999999
        for index, row in self.data.iterrows():
            [x, y, utm_zone, utm_letter] = utm.from_latlon(row["lat"], row["lon"])
            self.distance_pair.append(
                [index, calculate_distance(self.center[0], self.center[1], x, y), x, y])
            self.xMin = min(self.xMin, x)
            self.xMax = max(self.xMax, x)
            self.yMin = min(self.yMin, y)
            self.yMax = max(self.yMax, y)
        self.distance_pair.sort(key=self.sortFunc)
        print("x:[" + str(self.xMin) + ", " + str(self.xMax) + "]")
        print("y:[" + str(self.yMin) + ", " + str(self.yMax) + "]")

    def retrieve_data(self):
        retVal = []
        for index in range(0, len(self.distance_pair)):
            retVal.append(self.distance_pair[index])
        return len(self.distance_pair), retVal

    def retrieve_simple_data(self):
        retVal = []
        for index in range(0, len(self.distance_pair)):
            retVal.append([self.distance_pair[index][2], self.distance_pair[index][3]])
        return len(self.distance_pair), retVal


if __name__ == '__main__':
    pros = Processor()
    pros.import_data("plant_coords.csv")

    count, rows = pros.retrieve_simple_data()
    f = open('season12original.txt', 'w')
    f.write(str(count))
    f.write("\n")
    np.savetxt(f,
               rows,
               delimiter=" ",
               fmt='% s')
    f.close()
    exit(0)
