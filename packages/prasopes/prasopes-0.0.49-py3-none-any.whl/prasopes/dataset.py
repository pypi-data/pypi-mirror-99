#!/usr/bin/env python3
from rawprasslib import load_raw
from opentimspy.opentims import OpenTIMS
import pathlib
import opentims_bruker_bridge
import numpy as np
import prasopes.config as cf


class Dataset():
    def __init__(self, rawfile):
        self.filename = rawfile
        self.chromatograms = []
        self.selectedtimes = []
        self.matrixes = []

    def refresh(self):
        """implement per-case"""
        return None

    def get_chromatogram(self):
        """implement per-case"""
        return

    def get_matrixes(self):
        """implement per-case"""
        return


class ThermoRawDataset(Dataset):
    def __init__(self, rawfile):
        super().__init__(self, rawfile)
        self.refresh()

    def refresh(self):
        self.dataset = load_raw(selt.filename, 
                                cf.settings().value("tmp_location"))
        self.chromatograms = self.get_chromatogram()
        self.selectedtimerange = (self.chromatogram[0][0],
                                  self.chromatogram[-1][-1])

    def get_chtomatograms(self):
        return [i[0] for i in self.dataset]

    def get_masses(self):
        return [i[1] for i in self.dataset]

    def get_matrixes(self):
        return [i[2] for i in self.dataset]
            

class BrukerTimsDataset(Dataset):
    def __init__(self, rawfile):
        super().__init__(rawfile)
        self.refresh()

    def refresh(self):
        self.dataset = OpenTIMS(pathlib.Path(self.filename))
        self.chromatograms = self.get_chromatogram()
        self.selectedtimerange = (self.chromatogram[0][0],
                                  self.chromatogram[-1][-1])

    def get_chromatogram(self):
        keywords = ('retention time', 'intensity')
        myset = self.dataset.query(frames=self.dataset.ms1_frames, 
                                   columns=('retention_time',))
        print(type(myset))
        print(1/0)
        """nparr = [myset[i] for i in keywords
        print(myset['retention_time'])
        print(1/0)"""

