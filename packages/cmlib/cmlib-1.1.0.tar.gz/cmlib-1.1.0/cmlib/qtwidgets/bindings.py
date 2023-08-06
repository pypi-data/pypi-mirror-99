""" Harmonize PyQt and PySide bindings

    If the QT_API environment variable is set to pyside2 or pyqt5 that library is imported.
    Else it looks if one of those two is already imported.

    Then it will try first PyQt5 and then PySide2.

"""
import os
import sys


API_PYSIDE2 = 'pyside2'
API_PYQT5 = 'pyqt5'
ALL_API = [API_PYQT5, API_PYSIDE2]

# Determine from environment variable
QT_API_NAME = os.environ.get('QT_API')

# Discard unsupported bindings (e.g. pyqt4)
if QT_API_NAME not in ALL_API:
    QT_API_NAME = None

# Else see if module is already imported.
if QT_API_NAME is None:
    if 'PyQt5' in sys.modules:
        QT_API_NAME = API_PYQT5

if QT_API_NAME is None:
    if 'PySide2' in sys.modules:
        QT_API_NAME = API_PYSIDE2


# Finally, try the modules.
if QT_API_NAME is None:
    try:
        import PyQt5
    except ModuleNotFoundError:
        pass
    else:
        QT_API_NAME = API_PYQT5

if QT_API_NAME is None:
    try:
        import PySide2
    except ModuleNotFoundError:
        pass
    else:
        QT_API_NAME = API_PYSIDE2


# Do imports.

if QT_API_NAME == API_PYQT5:
    from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import pyqtSignal as QtSignal
    from PyQt5.QtCore import pyqtSlot as QtSlot
    from PyQt5.Qt import PYQT_VERSION_STR as PYQT_VERSION
    from PyQt5.Qt import QT_VERSION_STR as QT_VERSION

elif QT_API_NAME == API_PYSIDE2:

    from PySide2 import QtCore, QtGui, QtWidgets, QtSvg
    from PySide2.QtCore import Qt
    from PySide2.QtCore import Signal as QtSignal
    from PySide2.QtCore import Slot as QtSlot
    from PySide2 import __version__ as PYQT_VERSION
    from PySide2.QtCore import __version__ as QT_VERSION

else:

    raise ValueError("Unknown Qt API {!r}. Should be one of: {}".format(QT_API_NAME, ALL_API))


