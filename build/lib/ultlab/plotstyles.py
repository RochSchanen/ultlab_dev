# file: plotstyles.py
# created: 2023 05 19
# author: Roch Schanen
# comments:

# standard libraries
from sys import exit

# from package: "https://matplotlib.org/"
from matplotlib.pyplot import figure
from matplotlib.pyplot import fignum_exists
from matplotlib.backends.backend_pdf import PdfPages

from numpy import array
from numpy import absolute

# from package: "https://numpy.org/"
from numpy import pi, cos, sin
from numpy import ceil, floor
from numpy import log, log10, exp, square
from numpy import linspace, logspace

# from package: "https://scipy.org/"
from scipy.optimize import curve_fit as fit

def selectfigure(name):
    if not fignum_exists(name):
        # create figure
        fg = figure(name)
        # set A4 paper dimensions
        fg.set_size_inches(8.2677, 11.6929)
        # create square axis
        w, h = array([1, 1 / 1.4143])*0.7
        x, y = (1-w)/2, (1-h)/2
        ax = fg.add_axes([x, y, w, h])
    else:
        # select figure
        # (here the figure can be of any type)
        fg = figure(name)
        # get axes
        ax = fg.get_axes()[0]
    # done
    return fg, ax

def headerText(text, fg):
    w, h = array([1, 1 / 1.4143])*0.7
    x, y = (1-w)/2, (1-h)/2
    # tx = fg.text(x+w/2, 3*y/2+h, text)
    tx = fg.text(x, 3*y/2+h, text)
    tx.set_fontfamily('monospace')
    tx.set_horizontalalignment('left')
    tx.set_verticalalignment('center')
    tx.set_fontsize("small")
    return tx

def footerText(text, fg):
    w, h = array([1, 1 / 1.4143])*0.7
    x, y = (1-w)/2, (1-h)/2
    # tx = fg.text(x+w/2, y/2, text)
    tx = fg.text(x, y/2, text)
    tx.set_fontfamily('monospace')
    tx.set_horizontalalignment('left')
    tx.set_verticalalignment('center')
    tx.set_fontsize("small")
    return tx
 
def _getTickIntervals(start, stop, ticks):

    ln10 = 2.3025850929940459

    # trial table
    T = [0.010, 0.020, 0.025, 0.050,
         0.100, 0.200, 0.250, 0.500,
         1.000, 2.000, 2.500, 5.000]

    # corresponding tick sub division intervals
    S = [5.0,   4.0,   5.0,   5.0,
         5.0,   4.0,   5.0,   5.0,
         5.0,   4.0,   5.0,   5.0]

    span = stop - start                         # get span
    d = exp(ln10 * floor(log10(span)))          # find decade
    span /= d                                   # re-scale

    # find number of ticks below and closest to n
    i, m = 0, floor(span / T[0])                # start up
    while m > ticks:                            # next try?
        i, m = i + 1, floor(span / T[i + 1])    # try again 

    # re-scale
    mi =  d * T[i]   # main tick intervals
    si = mi / S[i]   # sub tick intervals

    # done
    return mi, si

def _getTickPositions(start, stop, ticks):

    # get intervals
    mi, si = _getTickIntervals(start, stop, ticks)

    # main ticks (round is the built-in python version)
    ns = ceil(start / mi - 0.001) * mi  # start
    ne = floor(stop / mi + 0.001) * mi  # end
    p  = round((ne - ns) / mi) + 1      # fail safe
    M  = linspace(ns, ne, p)            # main positions

    # sub ticks (round is the built-in python version)
    ns = ceil(start / si + 0.001) * si  # start
    ne = floor(stop / si - 0.001) * si  # end
    p  = round((ne - ns) / si) + 1      # fail safe
    S  = linspace(ns, ne, p)            # sub positions

    # done
    return M, S

def setup_units(value, *values):

    # find minimum and maximum in value
    S, E = min(value), max(value)

    # find minimum and maximum in *values
    for V in values:
        s, e = min(V), max(V)
        S, E = min(S, s), max(E, e)

    # get the maximum absolute value
    ma = max(absolute(S), absolute(E))

    # compute engineering units
    return {
         0: (1E+00,  ""),
        -1: (1E+03, "m"),
        -2: (1E+06, "µ"),
        -3: (1E+09, "n"),
        -4: (1E+12, "p"),
        +1: (1E-03, "K"),
        +2: (1E-06, "M"),
        +3: (1E-09, "G"),
        +4: (1E-12, "T"),
    }[int(floor(log10(ma)/3))]

def setup_axes(ax, x, y, lx = None, ly = None, ux = None, uy = None):

    # SETTINGS
    
    # margins as a fraction of the range
    l, r, t, b = 0.1, 0.1, 0.1, 0.1

    # target ticks number
    tx, ty = 7, 9

    # compute axis range
    xs, xe = min(x), max(x)
    ys, ye = min(y), max(y)
    dx, dy = xe-xs, ye-ys
    xs, xe = xs-dx*l, xe+dx*r
    ys, ye = ys-dy*b, ye+dy*t

    ax.set_xlim(xs, xe)
    MX, SX = _getTickPositions(xs, xe, tx)
    ax.set_xticks(MX)
    ax.set_xticks(SX, minor = True)

    ax.set_ylim(ys, ye)
    MY, SY = _getTickPositions(ys, ye, ty)
    ax.set_yticks(MY)
    ax.set_yticks(SY, minor = True)

    # fix grid style
    ax.tick_params(axis = "both", which = "both", direction = "in")
    ax.grid("on", which = "minor", linewidth = 0.3)
    ax.grid("on", which = "major", linewidth = 0.6)

    # set axes labels
    if ux: ax.set_xlabel(f"{lx} / {ux}")
    if uy: ax.set_ylabel(f"{ly} / {uy}")

    return

class Document():

    def __init__(self, pathname = None):
        if pathname is not None:
            self._DOC = self.opendocument(pathname)
        return

    def opendocument(self, pathname):
        self._DOC = PdfPages(pathname)
        return self._DOC

    def exportfigure(self, name):
        args = selectfigure(name)
        self._DOC.savefig(args[0])
        return

    def closedocument(self):
        self._DOC.close()
        return
