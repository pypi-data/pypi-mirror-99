import shutil
import tempfile
import time

from PyQt5 import QtCore


TMPDIR = tempfile.mkdtemp(prefix=time.strftime(
    "shapeout2_test_%H.%M_"))

pytest_plugins = ["pytest-qt"]


def pytest_configure(config):
    """This is ran before all tests"""
    # disable update checking
    QtCore.QCoreApplication.setOrganizationName("Zellmechanik-Dresden")
    QtCore.QCoreApplication.setOrganizationDomain("zellmechanik.com")
    QtCore.QCoreApplication.setApplicationName("shapeout2")
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)
    settings = QtCore.QSettings()
    settings.setIniCodec("utf-8")
    settings.setValue("check for updates", 0)
    settings.setValue("advanced/check pyqtgraph version", 0)
    settings.sync()
    # set global temp directory
    tempfile.tempdir = TMPDIR


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    # clear global temp directory
    shutil.rmtree(TMPDIR, ignore_errors=True)
