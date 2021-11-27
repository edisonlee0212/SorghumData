import copy

import numpy as np
import pandas as pd
import random


def calculate_distance(lon1, pat1, lon2, pat2):
    return 0.0


class Processor:
    def __init__(self):
        self.data = None
        self.center = None

    def import_data(self, path):
        self.data = pd.read_csv(path, index_col=0)


