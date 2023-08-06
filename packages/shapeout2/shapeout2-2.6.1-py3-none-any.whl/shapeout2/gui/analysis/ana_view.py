import pkg_resources

from PyQt5 import uic, QtCore, QtWidgets


class AnalysisView(QtWidgets.QWidget):
    filter_changed = QtCore.pyqtSignal(dict)
    plot_changed = QtCore.pyqtSignal(dict)
    slot_changed = QtCore.pyqtSignal(dict)
    pipeline_changed = QtCore.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self)
        path_ui = pkg_resources.resource_filename(
            "shapeout2.gui.analysis", "ana_view.ui")
        uic.loadUi(path_ui, self)
        self.setWindowTitle("Analysis View")
        self.setMinimumSize(self.sizeHint())
        # Signals
        self.widget_filter.filter_changed.connect(self.filter_changed)
        self.widget_filter.pipeline_changed.connect(self.pipeline_changed)
        self.widget_plot.plot_changed.connect(self.plot_changed)
        self.widget_plot.pipeline_changed.connect(self.pipeline_changed)
        self.widget_slot.slot_changed.connect(self.slot_changed)
        self.widget_slot.pipeline_changed.connect(self.pipeline_changed)

    def adopt_pipeline(self, pipeline_state):
        self.widget_meta.pipeline_state = pipeline_state
        # widget_plot, widget_slot, and widget_filter know the pipeline
        self.update_content()

    def set_pipeline(self, pipeline):
        self.widget_filter.set_pipeline(pipeline)
        self.widget_plot.set_pipeline(pipeline)
        self.widget_slot.set_pipeline(pipeline)
        self.adopt_pipeline(pipeline.__getstate__())

    def update_content(self):
        self.widget_filter.update_content()
        self.widget_meta.update_content()
        self.widget_plot.update_content()
        self.widget_slot.update_content()
