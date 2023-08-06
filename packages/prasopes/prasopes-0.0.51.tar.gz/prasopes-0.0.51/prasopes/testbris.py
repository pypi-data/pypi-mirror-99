#!/usr/bin/env python3
import datasets
import numpy as np
from matplotlib import pyplot as plt

print("hello")
#mySett = datasets.BrukerTimsDataset('/home/yan/roithPhD/sw_modd/msresearch/opentims_spektra/210211_PEG600_TIMS_Detect_Calibrated.d')
mySett = datasets.BrukerTimsDataset('/home/yan/sw_modd/msresearch/opentims/20210212/210212_Formose 13C_Reaction2.d')

print(type(mySett))

print("getting")
#[[masses, ints]] = mySett.get_spectra()
[tofs, ints] = mySett.get_mobilogram(221.8,222.2, 5, 7)

"""plotofs = np.bincount(tofs, ints) / np.bincount(tofs)
pos = np.arange(len(plotofs))"""

"""print(mySett.dataset)
masses = np.concatenate([i[0] for i in massints])
intensities =np.concatenate([i[1] for i in massints])
sortmasses = np.sort(np.concatenate([i[0] for i in massints]))
masssteps = sortmasses[1:] - sortmasses[:-1]
binspos = np.where(masssteps > 0.001)[0]
bins = sortmasses[:-1][binspos] + (masssteps[binspos]/2)
binposs = np.digitize(masses, bins)
bindmasses = np.bincount(binposs, masses) / np.bincount(binposs)
bindints = np.bincount(binposs, intensities) / np.bincount(binposs)
#print(bindmasses)"""

"""for i,j in enumerate(massints):
        plt.plot(j[0], j[1], marker='o', markersize=0.5, linestyle='None')"""
#plt.plot(bins, np.zeros(bins.shape), marker='o', markersize=2, linestyle='None')
print("plotting")
#plt.plot(tofs, ints)
plt.plot(tofs, ints)#, marker='o', markersize=2, linestyle='None')
#plt.plot(pos, plotofs)#, marker='o', markersize=2, linestyle='None')
plt.show()

