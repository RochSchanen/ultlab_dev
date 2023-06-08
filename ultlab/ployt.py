# generate pdf document as display, multiple pages with multiple display.
# use sumatrapdf to display and reload the document.
# if the plot are big, use diferent documents and pdf file names.

###########################
### A-class paper sizes ###
###########################

# init with largest size
_AClassSizes = {"A0" : (841, 1189)}

# compute smaller sizes downto A10
for i in range(10):
    W, H = _AClassSizes[f"A{i}"]
    _AClassSizes[f"A{i+1}"] = (H/2, W)

#####################
### select figure ###
####################''

# "A5" is set as default to fit remarkable 2

def selectfigure(name, AClassName = "A5", Margins = 15):

    from matplotlib.pyplot import fignum_exists
    from matplotlib.pyplot import figure

    if not fignum_exists(name):
        # create figure
        fg = figure(name)
        # get paper dimensions in mm
        W, H = _AClassSizes[AClassName]
        # set figure size  in inches
        fg.set_size_inches(W/25.4, H/25.4)
        # compute square axes dimensions in page units
        w, h = 2*(1.0-Margins/100), 2*(1.0-Margins/100) * W/H
        # compute square axes positions in page units
        x, y = (1.0-w)/2, (1.0-h)/2
        # create axes
        ax = fg.add_axes([x, y, w, h])

    else:
        # select any existing figure
        fg = figure(name)
        # get the main figure axes
        ax = fg.get_axes()[0]

    # done
    return fg, ax

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
    doc.exportfigure("1")
