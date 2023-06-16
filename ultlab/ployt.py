# generate pdf document as display, multiple pages with multiple display.
# use sumatrapdf to display and reload the document.
# if the plot are big, use diferent documents and pdf file names.

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
####################''

_CurrentFigure = None
_CurrentFigureAxes = None

# "A5" is set as default to fit remarkable 2

def SelectFigure(name, 
        SizeName = "A4",            # A0 to A10
        Margins = 15.0,             # 0 to 100
        orientation = "portrait",   # "portrait", "landscape"
        ):

    # matplotlib should be installed
    from matplotlib.pyplot import fignum_exists
    from matplotlib.pyplot import figure

    if not fignum_exists(name):
        # create figure
        fg = figure(name)
        # get paper dimensions in mm
        W, H = AClass().PaperSize(SizeName)
        # set figure size  in inches
        fg.set_size_inches(W/25.4, H/25.4)
        # compute square axes length in page units
        l = 2*(1.0-Margins/100)
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

    def __init__(self, pathname):
        self.pathname   = pathname
        self.filehandle = None # file handle
        self.figures    = [] # figure list
        return

    def openfile(self):
        from matplotlib.backends.backend_pdf import PdfPages
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

##############
## LORENTZ ###
##############

from numpy import square

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

############
## SHEET ###
############

from numpy import array, linspace

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
        self.data["x"] = FX(x, 123, 0.2, 2.0, 0.0)
        self.data["y"] = FY(x, 123, 0.2, 2.0, 0.0)

        # done
        return

    def Col(self, *names):
        r = []
        for n in names:        
            if n in self.data.keys():
                r.append(self.data[n])
        # done
        return r

##################
## TEST MODULE ###
##################

if __name__ == "__main__":

    # fg1, ax1 = selectfigure("1")
    # fg2, ax2 = selectfigure("2")

    ds = DataSheet()
    ds.read()
    # sheet.read("path")

    f = ds.Col("f")
    x = ds.Col("x")
    y = ds.Col("y")

    # x, y = sheet.Col("name1", "name2")

    fg, ax = SelectFigure("fx")

    # Plot("figname", x, y, style = sheet.GetStyle("stylename"))

    ax.plot(f, x)
    ax.plot([0, 1], [0, 1])
    # sheet.GetStyle("stylename")("figname")

    # s = sheet.GetStyle("stylename")
    # Plot("figname", x, y, style = s)

    doc = Document("result.pdf")
    doc.exportfigure("fx")
    doc.updatefile()
