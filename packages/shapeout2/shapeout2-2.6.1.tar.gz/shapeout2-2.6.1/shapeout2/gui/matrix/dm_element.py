import pkg_resources

from PyQt5 import uic, QtWidgets, QtCore


class MatrixElement(QtWidgets.QWidget):
    _quick_view_instance = None
    quickview_selected = QtCore.pyqtSignal()
    element_changed = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        path_ui = pkg_resources.resource_filename(
            "shapeout2.gui.matrix", "dm_element.ui")
        uic.loadUi(path_ui, self)

        self.active = False
        self.enabled = True
        self.invalid = False

        self.update_content()

    def __getstate__(self):
        state = {"active": self.active and not self.invalid,
                 "enabled": self.enabled,
                 "invalid": self.invalid}
        return state

    def __setstate__(self, state):
        self.active = state["active"] and not state["invalid"]
        self.enabled = state["enabled"]
        self.invalid = state["invalid"]
        self.update_content()

    def has_quickview(self):
        curinst = MatrixElement._quick_view_instance
        if curinst is self:
            quickview = True
        else:
            quickview = False
        return quickview

    def mousePressEvent(self, event):
        # toggle selection
        if not self.invalid:
            if event.modifiers() == QtCore.Qt.ShiftModifier:
                quickview = not self.has_quickview()
            else:
                self.active = not self.active
                quickview = False
                self.element_changed.emit()
            self.update_content(quickview)
            event.accept()

    def set_active(self, b=True):
        state = self.__getstate__()
        state["active"] = b
        self.__setstate__(state)

    def update_content(self, quickview=False):
        if self.invalid:
            color = "#DCDCDC"  # gray
            label = "invalid"
            tooltip = "Incompatible filter settings"
        elif self.active and self.enabled:
            color = "#86E789"  # green
            label = "active"
            tooltip = "Click to deactivate"
        elif self.active and not self.enabled:
            color = "#C9DAC9"  # gray-green
            label = "active\n(unused)"
            tooltip = "Click to deactivate"
        elif not self.active and self.enabled:
            color = "#EFEFEF"  # light gray
            label = "inactive"
            tooltip = "Click to activate"
        else:
            color = "#DCDCDC"  # gray
            label = "inactive\n(unused)"
            tooltip = "Click to activate"

        if not self.invalid:
            if self.has_quickview():
                do_quickview = True
            elif quickview:
                curinst = MatrixElement._quick_view_instance
                # reset color of old quick view instance
                if curinst is not None and self is not curinst:
                    MatrixElement._quick_view_instance = None
                    try:
                        curinst.update_content()
                    except RuntimeError:
                        # element has been deleted
                        pass
                MatrixElement._quick_view_instance = self
                do_quickview = True
            else:
                do_quickview = False
            if do_quickview:
                color = "#F0A1D6"
                label += "\n(QV)"
                self.quickview_selected.emit()
            else:
                tooltip += "\nShift+Click for Quick View"

        self.setStyleSheet("background-color:{}".format(color))
        self.label.setStyleSheet("background-color:{}".format(color))
        self.label.setText(label)
        self.setToolTip(tooltip)
        self.label.setToolTip(tooltip)
