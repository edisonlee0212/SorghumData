import copy

import numpy as np
import pandas as pd
import random
from geopy.distance import distance
import csv

def calculate_distance(lat1, lon1, lat2, lon2):
    return distance((lat1, lon1), (lat2, lon2)).m

def calculate_xy(lat1, lon1, lat2, lon2):
    return distance((lat1, lon2), (lat2, lon2)).m, distance((lat2, lon1), (lat2, lon2)).m

class Processor:
    def __init__(self):
        self.data = None
        self.center = None
        self.distance_pair = []

    @staticmethod
    def sortFunc(e):
        return e[1]

    def import_data(self, path):
        self.data = pd.read_csv(path, index_col=0)
        avglon = 0.0
        avglat = 0.0
        for index, row in self.data.iterrows():
            avglon += row["lon"]
            avglat += row["lat"]
        avglon /= self.data.count(axis=0)
        avglat /= self.data.count(axis=0)
        self.center = (avglat["lat"], avglon["lon"])
        for index, row in self.data.iterrows():
            x, y = calculate_xy(self.center[0], self.center[1], row["lat"], row["lon"])
            self.distance_pair.append(
                [index, calculate_distance(self.center[0], self.center[1], row["lat"], row["lon"]), x, y])

        self.distance_pair.sort(key=self.sortFunc)

    def retrieve_data(self, count):
        retVal = []
        for index in range(0, count):
            retVal.append(self.distance_pair[index])
        return retVal

    def retrieve_simple_data(self, count):
        retVal = []
        for index in range(0, count):
            retVal.append([self.distance_pair[index][2], self.distance_pair[index][3]])
        return retVal

if __name__ == '__main__':
    pros = Processor()
    pros.import_data("2021-08-02__13-11-38-442_sorghum_detection.csv")
    rows = pros.retrieve_data(20000)
    np.savetxt("full.csv",
               rows,
               delimiter=", ",
               fmt='% s')
    rows = pros.retrieve_simple_data(20000)
    np.savetxt("simple.txt",
               rows,
               delimiter=" ",
               fmt='% s')