# file: ployt_bkup01.py
# created:
# modified: 2023 06 18
# author: Roch Schanen

# target: generate pdf document as display, multiple pages with multiple display.
# use sumatrapdf to display and reload the document.
# if the plot are big, use diferent documents and pdf file names.

# from 
from matplotlib.pyplot import figure
from matplotlib.pyplot import fignum_exists
from matplotlib.backends.backend_pdf import PdfPages

# from 
from numpy import ceil, floor
from numpy import log, log10, exp, square, absolute
from numpy import array, linspace, insert

### A-class paper sizes

class AClass():

    def __init__(self):
        # largest size
        d = {"A0" : (841, 1189)}
        # smaller sizes
        for i in range(10):
            W, H = d[f"A{i}"]
            d[f"A{i+1}"] = (round(H/2), W)
        # register dictionary
        self.sizes = d
        # done
        return

    def PaperSize(self, Format):
        return self.sizes[Format]

#####################
### select figure ###
#####################

_CurrentFigure = None
_CurrentFigureAxes = None

# "A5" is set as default to fit remarkable 2

def SelectFigure(name, 
        Size        =       "A5", # A0 to A10
        border      =       15.0, # percent
        orientation = "portrait", # "portrait"/"landscape"
        ):

    if not fignum_exists(name):
        # create figure
        fg = figure(name)
        # get paper dimensions in mm
        W, H = AClass().PaperSize(Size)
        # set figure size  in inches
        fg.set_size_inches(W/25.4, H/25.4)
        # compute square axes length in page units
        l = 1.0-2*border/100
        # setup orientation
        if orientation == "portrait":  w, h = (l, l*W/H)
        if orientation == "landscape": w, h = (l*W/H, l)
        # compute square axes positions in page units
        x, y = (1.0-w)/2, (1.0-h)/2
        # create axes
        ax = fg.add_axes([x, y, w, h])

    else:
        # select any existing figure
        fg = figure(name)
        # get the figure first axes
        ax = fg.get_axes()[0]

    # update current values
    global _CurrentFigure
    global _CurrentFigureAxes
    _CurrentFigure       = fg
    _CurrentFigureAxes   = ax

    # done
    return fg, ax

def cfg():
    return _CurrentFigure

def cfa():
    return _CurrentFigureAxes

######################
### document class ###
######################

class Document():

    def __init__(self, pathname, *figures):
        self.pathname   = pathname
        self.filehandle = None
        self.figures    = figures
        self.updatefile()
        return

    def openfile(self):
        self.filehandle = PdfPages(self.pathname)
        return self.filehandle

    def closefile(self):
        self.filehandle.close()
        return

    def updatefile(self):
        self.openfile()
        for n in self.figures:
            args = SelectFigure(n)
            self.filehandle.savefig(args[0])
        self.closefile()
        return

    def exportfigure(self, name):
        if not name in self.figures:
            self.figures.append(name)
        self.updatefile()
        return

############
## SHEET ###
############

class DataSheet():

    def __init__(self):
        self.data = {}
        return

    def read(self, path = None):
        # select path using wx dialog
        if path is None:
            # open dialog
            pass
        # open file

        # detect file type
        
        # import data 
        
        # simulate
        x = linspace(122.5, 123.5, 101)
        self.data["f"] = x
        self.data["x"] = FX(x, 123, 0.2, 2.0E-5, 0.0)
        self.data["y"] = FY(x, 123, 0.2, 2.0E-5, 0.0)

        # done
        return

    def Col(self, *names):
        r = []
        for n in names:        
            if n in self.data.keys():
                r.append(self.data[n])
        # return single column
        if len(r) == 1: return r[0]
        # return multiple columns
        return r

###########
## PLOT ###
###########

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

def GetUnitPrefix(table, *tables):

    # find minimum and maximum in table
    S, E = min(table), max(table)

    # find minimum and maximum in all tables
    for T in tables:
        s, e = min(T), max(T)
        S, E = min(S, s), max(E, e)

    # get the maximum absolute value
    ma = max(absolute(S), absolute(E))

    # compute prefactor and prefix
    prefactor, prefix = {   
         0: (1E+00, ""),
        -1: (1E+03, "m"),
        -2: (1E+06, "µ"),
        -3: (1E+09, "n"),
        -4: (1E+12, "p"),
        +1: (1E-03, "K"),
        +2: (1E-06, "M"),
        +3: (1E-09, "G"),
        +4: (1E-12, "T"),
    }[int(floor(log10(ma)/3))]
    
    # done
    return prefactor, prefix 

def AutoRange(axis, data):
    # default margin
    m = 0.1
    # set limits
    s, e = min(data), max(data)
    # extend to margins
    s, e = s-(e-s)*m, e+(e-s)*m
    # apply to selected axis
    {"x": cfa().set_xlim,
     "y": cfa().set_ylim,
        }[axis](s, e)
    return 

def AutoTick(axis, ticks = 5):
    # get current limits
    s, e = {
        "x": cfa().get_xlim,
        "y": cfa().get_ylim
        }[axis]()
    # get tick positions
    M, S = _getTickPositions(s, e, ticks)
    # get method on selected axis
    set_ticks = {
        "x": cfa().set_xticks,
        "y": cfa().set_yticks
        }[axis]
    # apply minor and major ticks
    set_ticks(M)
    set_ticks(S, minor = True)
    # apply tick styles
    cfa().tick_params(axis = axis, which = "both", direction = "in")
    return

def AutoGrid(axis = "both"):
    cfa().grid("on", axis = axis, which = "minor", linewidth = 0.3)
    cfa().grid("on", axis = axis, which = "major", linewidth = 0.6)
    return    

def AutoStyle(x, y, xticks = 7, yticks = 7, origin_x = False, origin_y = False):
    if origin_x: x = insert(x, 0, 0.0)
    if origin_y: y = insert(y, 0, 0.0)
    AutoRange("x", x); AutoTick("x", xticks)
    AutoRange("y", y); AutoTick("y", yticks)
    AutoGrid()
    # done
    return

def Plot(*args, **kwargs):
    if isinstance(args[0], str):
        SelectFigure(args[0])
        args = args[1:]
    return _CurrentFigureAxes.plot(*args, **kwargs)

##################
## TEST MODULE ###
##################

if __name__ == "__main__":

    # in-phase fitting function
    def FX(t, p, w, h, o):
        x = (t-p)/w
        y = h/(1+square(x))+o
        return y

    # quadrature fitting function
    def FY(t, p, w, h, o):
        x = (t-p)/w
        # y = -x*h/(1+square(x))+o
        y = +x*h/(1+square(x))+o
        return y

    ####################################

    # ds = DataSheet()

    # ds.read() # unfinished
    # sheet.read("path")

    # f = ds.Col("f")
    # x = ds.Col("x")
    # y = ds.Col("y")

    # f, x, y = ds.Col("f", "x", "y")

    # fg, ax = SelectFigure("fx")
    # ax.Plot(f, x)

    # SelectFigure("fx")
    # Plot(f, x)

    # Plot("fx", f, x)

    # Plot("fx", ds.Col("f"), ds.Col("x"))

    # Plot("fx", *ds.Col("f", "x"))
    # Plot("fy", *ds.Col("f", "y"))
    # Plot("xy", *ds.Col("x", "y"))

    # f, x, y = ds.Col("f", "x", "y")

    # fg, ax = SelectFigure("fx", Size = "A5")
    # ax.plot(f, x)

    # doc = Document("result.pdf")
    # doc.exportfigure("fx")
    # doc.exportfigure("fy")
    # doc.updatefile()

    # doc = Document("result.pdf", "fx", "fy", "xy")


    ds = DataSheet()

    ds.read()

    f, x, y = ds.Col("f", "x", "y")

    uf, up = GetUnitPrefix(x, y)

    Plot("fx", f, x*uf)
    AutoStyle(f, x*uf)

    cfa().set_xlabel(f"frequency / Hz")
    cfa().set_ylabel(f"X signal / {up}V")

    doc = Document("result.pdf", "fx")

    ####################################

    # sheet.GetStyle("stylename")("figname")
    # Plot("figname", x, y, style = sheet.GetStyle("stylename"))
    # s = sheet.GetStyle("stylename")
    # Plot("figname", x, y, style = s)
