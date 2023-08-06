import sys, os, numpy, platform
import orangecanvas.resources as resources
from PyQt5 import QtGui, QtCore

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from matplotlib import figure as matfig
    import pylab
except ImportError:
    print(sys.exc_info()[1])
    pass


import xraylib

from oasys.widgets import gui
from orangecontrib.xoppy.util.text_window import TextWindow

from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class locations:
    @classmethod
    def home_bin(cls):
        if platform.system() == "Windows":
            return resources.package_dirname("orangecontrib.xoppy.util") + "\\bin\windows\\"
        else:
            return resources.package_dirname("orangecontrib.xoppy.util") + "/bin/" + str(sys.platform) + "/"

    @classmethod
    def home_doc(cls):
        if platform.system() == "Windows":
            return resources.package_dirname("orangecontrib.xoppy.util") + "\doc_txt/"
        else:
            return resources.package_dirname("orangecontrib.xoppy.util") + "/doc_txt/"

    @classmethod
    def home_data(cls):
        if platform.system() == "Windows":
            return resources.package_dirname("orangecontrib.xoppy.util") + "\data/"
        else:
            return resources.package_dirname("orangecontrib.xoppy.util") + "/data/"

    @classmethod
    def home_bin_run(cls):
        #return resources.package_dirname("orangecontrib.xoppy.util") + "/bin_run/"
        return os.getcwd()

def xoppy_doc(app):
    home_doc = locations.home_doc()

    filename1 = os.path.join(home_doc,app+'.txt')

    o = TextWindow()
    o.set_file(filename1)


class XoppyPhysics:

    ######################################
    # FROM NIST
    codata_h = numpy.array(6.62606957e-34)
    codata_ec = numpy.array(1.602176565e-19)
    codata_c = numpy.array(299792458.0)
    ######################################

    A2EV = (codata_h*codata_c/codata_ec)*1e+10
    K2EV = 2*numpy.pi/(codata_h*codata_c/codata_ec*1e+2)

    @classmethod
    def getWavelengthFromEnergy(cls, energy): #in eV
        return cls.A2EV/energy # in Angstrom

    @classmethod
    def getEnergyFromWavelength(cls, wavelength): # in Angstrom
        return cls.A2EV/wavelength # in eV

    @classmethod
    def getMaterialDensity(cls, material_formula):
        if material_formula is None: return 0.0
        if str(material_formula.strip()) == "": return 0.0

        try:
            compoundData = xraylib.CompoundParser(material_formula)

            if compoundData["nElements"] == 1:
                return xraylib.ElementDensity(compoundData["Elements"][0])
            else:
                return 0.0
        except:
            return 0.0

class XoppyGui:

    @classmethod
    def combobox_text(cls, widget, master, value, box=None, label=None, labelWidth=None,
             orientation='vertical', items=(), callback=None,
             sendSelectedValue=False, valueType=str,
             control2attributeDict=None, emptyString=None, editable=False, selectedValue = None,
             **misc):

        combo = gui.comboBox(widget, master, value, box=box, label=label, labelWidth=labelWidth, orientation=orientation,
                                  items=items, callback=callback, sendSelectedValue=sendSelectedValue, valueType=valueType,
                                  control2attributeDict=control2attributeDict, emptyString=emptyString, editable=editable, **misc)
        try:
            combo.setCurrentIndex(items.index(selectedValue))
        except:
            pass

        return combo
