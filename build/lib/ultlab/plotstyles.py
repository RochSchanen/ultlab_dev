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
 
    # fg.text(0.5, 0.5,
    #     'boxed italics text in data coords',
    #     style='italic',
    #     bbox={
    #         'facecolor': 'red',
    #         'alpha': 0.3,
    #         'pad': 10}
    #     )
