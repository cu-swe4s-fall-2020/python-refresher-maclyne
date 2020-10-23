""" plot Covid19 rates

    Initial date: 22 Oct 2020
    Author: Margot Clyne


"""
from my_utils import get_column
import sys
import argparse
from operator import itemgetter
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt


def plot_lines(points, labels, file_name):
"""Take a list of list of points and plot each list as a line.
        Parameters
        ----------
        points    : list of list of points
                    Each sublist corresponds to the points for one element.
                    Each point has two values, the first will be the X value
                    and the second the Y value
        labels    : list of strings
                    Each element in lables corresponds to the sublist at the
                    same poisiting in data
        file_name : string
                    Name of the output file.
"""
    fig = plt.figure(figsize=(10,3), dpi=300)
    ax = fig.add_subplot(1,1,1)
    i=0
    for pairs in points:
        X = []
        Y = []
        for pair in pairs:
            X.append(pair[0])
            Y.append(pair[1])

        ax.plot(X, Y, lw=0.5)
        ax.text(X[-1], Y[-1], labels[i], size=5)

        i += 1

    plt.savefig(file_name, bbox_inches='tight')


