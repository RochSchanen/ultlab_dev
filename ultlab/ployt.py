# generate pdf document as display, multiple pages with multiple display.
# use sumatrapdf to display and reload the document.
# if the plot are big, use diferent documents and pdf file names.

#####################
### A-class sizes ###
#####################

_PageSizes = {"A0" : (841, 1189)}

# compute smaller sizes
for i in range(10):
    W, H = _PageSizes[f"A{i}"]
    _PageSizes[f"A{i+1}"] = (H/2, W)
del i, W, H

def PageSize(name):
    return _PageSizes[name]

#####################
### select figure ###
####################''

_CurrentFigure = None
_CurrentFigureAxes = None

# "A5" is set as default to fit remarkable 2

def selectfigure(name, 
        SizeName = "A5",            # A0 to A10
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
        W, H = PageSize(SizeName)
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
            args = selectfigure(n)
            self.filehandle.savefig(args[0])
        self.closefile()
        return

    def exportfigure(self, name):
        if not name in self.figures:
            self.figures.append(name)
        self.updatefile()
        return

##################
## TEST MODULE ###
##################

if __name__ == "__main__":

    fg1, ax1 = selectfigure("1")
    fg2, ax2 = selectfigure("2")

    doc = Document("../../results.pdf")
    doc.exportfigure("1")
    doc.exportfigure("2")
