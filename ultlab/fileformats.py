# file: fileformats.py
# created: 2023 05 18
# author: Roch Schanen
# comments:

from numpy import loadtxt

""" file formats for acquired data storage are classed using the acquisition
sotware, the device model, the measurement type, and a date used as a version
number. Each file format has an unique id number.
"""

FILE_FORMATS = [
    ("Labview Generated Data File", "Torsion Oscillator",  "two lockins", ""),              # 0
    ("Python Generated Data File", "Quartz Tuning Fork", "frequency sweep", "20230517"),    # 1
    ]

def DetectFileFormat(filepath):
    return 0

def ImportFileData(filepath, fileformat = None):

    def seconds(s):
        t =  float(s[0:2])*3600
        t += float(s[3:5])*60
        t += float(s[6: ])*1
        return t

    # automatic detection
    if fileformat is None:
        fileformat = detectFileFormat(filepath)

    # ---------------------------------------------------------------
    # Labview Generated Data Files - Torsion Oscillator - two lockins
    # ---------------------------------------------------------------

    if fileformat == 0:

        # import file header    
        with open(filepath, "r") as fh: header_string = fh.readline()

        header_list = header_string.split(f"\t")

        if header_list:
            filedate = header_list[1]
            filetime = header_list[2]

        header_info = {
            "file"      :   filepath.split("/")[-1],
            "date"      :   filedate,
            "time"      :   filetime,
            "time[s]"   :   seconds(filetime),
            "drive"     :   float(header_list[3].split(" ")[-1])*1E-3,
            }

        header = ""
        for k in header_info.keys():
            header += f"{k:<7}:  {header_info[k]}\n"

        # import file data
        #  Vx Vy time Vx2 Vy2
        data = loadtxt(filepath,
            comments    = ["%","freq"],
            converters  = {
                0: float,       # freq
                1: float,       # Vx
                2: float,       # Vy
                3: float,       # time
                4: float,       # Vx2
                5: float,       # Vy2
                },
            )

        # fix the orign of time at the begin of data acquisition
        T  = data[:, 3] - data[0, 3]   
        F  = data[:, 0]
        X  = data[:, 1]
        Y  = data[:, 2]
        X2 = data[:, 4]
        Y2 = data[:, 5]

        data = (T, F, X, Y, X2, Y2)

        # done
        return data, header
 
    return None


# --------------------------------------------------------------------- #
# Python Generated Data Files - Quartz Tuning Fork - FROM DATE 20230517 #
# --------------------------------------------------------------------- #

def QTF_TO_DataSheetImport(Datasheet, Filepath)

    # import file header, return as multi-lines string
    header = ""
    with open(fp, 'r') as fh: L = fh.readlines()
    for l in L[:10]: header += l[2:]

    # import data
    data = loadtxt(fp,
        converters = {
            0: seconds,
            1: float,
            2: float,
            3: float,
        })

    # append columns to datasheet
    T = data[:, 0]
    F = data[:, 1]
    X = data[:, 2]
    Y = data[:, 3]

    return data, header
