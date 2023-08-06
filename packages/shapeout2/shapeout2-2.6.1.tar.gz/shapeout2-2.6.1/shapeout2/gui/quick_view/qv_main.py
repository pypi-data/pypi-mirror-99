import pathlib
import pkg_resources

import dclab
import numpy as np
from PyQt5 import uic, QtCore, QtWidgets
import pyqtgraph as pg
from scipy.ndimage import binary_erosion

from ..compute.comp_stats import STAT_METHODS
from .. import idiom
from ..widgets import show_wait_cursor


class QuickView(QtWidgets.QWidget):
    polygon_filter_created = QtCore.pyqtSignal()
    polygon_filter_modified = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self)
        path_ui = pkg_resources.resource_filename(
            "shapeout2.gui.quick_view", "qv_main.ui")
        uic.loadUi(path_ui, self)
        path_css = pkg_resources.resource_filename(
            "shapeout2.gui.quick_view", "qv_style.css")
        stylesheet = pathlib.Path(path_css).read_text()
        self.groupBox_image.setStyleSheet(stylesheet)
        self.groupBox_trace.setStyleSheet(stylesheet)

        self.setWindowTitle("Quick View")

        self._set_initial_ui()

        # Set scale options (with data)
        for cb in [self.comboBox_xscale, self.comboBox_yscale]:
            cb.clear()
            cb.addItem("linear", "linear")
            cb.addItem("logarithmic", "log")

        # settings button
        self.toolButton_event.toggled.connect(self.on_tool)
        self.toolButton_poly.toggled.connect(self.on_tool)
        self.toolButton_settings.toggled.connect(self.on_tool)

        # polygon filter signals
        self.label_poly_create.hide()
        self.label_poly_modify.hide()
        self.pushButton_poly_save.hide()
        self.pushButton_poly_cancel.hide()
        self.pushButton_poly_create.clicked.connect(self.on_poly_create)
        self.pushButton_poly_save.clicked.connect(self.on_poly_done)
        self.pushButton_poly_cancel.clicked.connect(self.on_poly_done)
        self.comboBox_poly.currentIndexChanged.connect(self.on_poly_modify)
        self.update_polygon_panel()

        # event changed signal
        self.widget_scatter.scatter.sigClicked.connect(
            self.on_event_scatter_clicked)
        self.widget_scatter.update_hover_pos.connect(
            self.on_event_scatter_hover)
        self.spinBox_event.valueChanged.connect(self.on_event_scatter_spin)
        self.checkBox_image_contour.stateChanged.connect(
            self.on_event_scatter_update)
        self.checkBox_image_contrast.stateChanged.connect(
            self.on_event_scatter_update)
        self.checkBox_image_zoom.stateChanged.connect(
            self.on_event_scatter_update)
        self.checkBox_image_background.stateChanged.connect(
            self.on_event_scatter_update)
        self.checkBox_trace_raw.stateChanged.connect(
            self.on_event_scatter_update)
        self.checkBox_trace_legend.stateChanged.connect(
            self.on_event_scatter_update)
        self.checkBox_trace_zoom.stateChanged.connect(
            self.on_event_scatter_update)
        self.tabWidget_event.currentChanged.connect(
            self.on_event_scatter_update)

        # value changed signals for plot
        self.signal_widgets = [self.checkBox_downsample,
                               self.spinBox_downsample,
                               self.comboBox_x,
                               self.comboBox_y,
                               self.comboBox_xscale,
                               self.comboBox_yscale,
                               self.checkBox_isoelastics,
                               ]
        for w in self.signal_widgets:
            if hasattr(w, "currentIndexChanged"):
                w.currentIndexChanged.connect(self.plot)
            elif hasattr(w, "stateChanged"):
                w.stateChanged.connect(self.plot)
            elif hasattr(w, "valueChanged"):
                w.valueChanged.connect(self.plot)
        # copy statistics to clipboard
        self.toolButton_stats2clipboard.clicked.connect(
            self.on_stats2clipboard)

        # Set individual plots
        kw0 = dict(x=np.arange(10), y=np.arange(10))
        self.trace_plots = {
            "fl1_raw": pg.PlotDataItem(pen="#6EA068", **kw0),  # green
            "fl2_raw": pg.PlotDataItem(pen="#8E7A45", **kw0),  # orange
            "fl3_raw": pg.PlotDataItem(pen="#8F4D48", **kw0),  # red
            "fl1_median": pg.PlotDataItem(pen="#15BF00", **kw0),  # green
            "fl2_median": pg.PlotDataItem(pen="#BF8A00", **kw0),  # orange
            "fl3_median": pg.PlotDataItem(pen="#BF0C00", **kw0),  # red
        }
        for key in self.trace_plots:
            self.graphicsView_trace.addItem(self.trace_plots[key])
            self.trace_plots[key].hide()

        self.graphicsView_trace.plotItem.setLabels(
            left="Fluorescence [a.u.]", bottom="Event time [µs]")
        self.legend_trace = self.graphicsView_trace.addLegend(
            offset=(-.01, +.01))

        #: default parameters for the event image
        self.imkw = dict(autoLevels=False,
                         levels=(0, 255),
                         )

        # set initial empty dataset
        self._rtdc_ds = None
        self.slot = None

    def __getstate__(self):
        plot = {
            "downsampling": self.checkBox_downsample.isChecked(),
            "downsampling value": self.spinBox_downsample.value(),
            "axis x": self.comboBox_x.currentData(),
            "axis y": self.comboBox_y.currentData(),
            "scale x": self.comboBox_xscale.currentData(),
            "scale y": self.comboBox_yscale.currentData(),
            "isoelastics": self.checkBox_isoelastics.isChecked(),
        }
        event = {
            "index": self.spinBox_event.value(),
            "image auto contrast": self.checkBox_image_contrast.isChecked(),
            "image contour": self.checkBox_image_contour.isChecked(),
            "image zoom": self.checkBox_image_zoom.isChecked(),
            "image background": self.checkBox_image_background.isChecked(),
            "trace legend": self.checkBox_trace_legend.isChecked(),
            "trace raw": self.checkBox_trace_raw.isChecked(),
            "trace zoom": self.checkBox_trace_zoom.isChecked(),
        }
        state = {
            "plot": plot,
            "event": event,
        }
        return state

    def __setstate__(self, state):
        plot = state["plot"]
        for tb in self.signal_widgets:
            tb.blockSignals(True)
        # downsampling
        self.checkBox_downsample.setChecked(plot["downsampling"])
        self.spinBox_downsample.setValue(plot["downsampling value"])
        # axes labels
        self.update_feature_choices()
        idx = self.comboBox_x.findData(plot["axis x"])
        self.comboBox_x.setCurrentIndex(idx)
        idy = self.comboBox_y.findData(plot["axis y"])
        self.comboBox_y.setCurrentIndex(idy)
        # scaling
        idxs = self.comboBox_xscale.findData(plot["scale x"])
        self.comboBox_xscale.setCurrentIndex(idxs)
        idys = self.comboBox_yscale.findData(plot["scale y"])
        self.comboBox_yscale.setCurrentIndex(idys)
        # isoelastics
        self.checkBox_isoelastics.setChecked(plot["isoelastics"])
        for tb in self.signal_widgets:
            tb.blockSignals(False)
        if "event" in state:
            event = state["event"]
            self.checkBox_image_contrast.setChecked(
                event["image auto contrast"])
            self.checkBox_image_contour.setChecked(event["image contour"])
            self.checkBox_image_zoom.setChecked(event["image zoom"])
            self.checkBox_image_background.setChecked(
                    event["image background"])
            self.spinBox_event.setValue(event["index"])
            self.checkBox_trace_raw.setChecked(event["trace raw"])
            self.checkBox_trace_legend.setChecked(event["trace legend"])

    def _check_file_open(self, rtdc_ds):
        """Check whether a dataset is still open"""
        if isinstance(rtdc_ds, dclab.rtdc_dataset.RTDC_HDF5):
            if rtdc_ds._h5:
                # the file is open
                isopen = True
            else:
                isopen = False
        elif isinstance(rtdc_ds, dclab.rtdc_dataset.RTDC_Hierarchy):
            isopen = self._check_file_open(rtdc_ds.hparent)
        else:
            # DCOR
            isopen = True
        return isopen

    def _set_initial_ui(self):
        # Initially, only show the info about how QuickView works
        self.widget_tool.setEnabled(False)
        self.widget_scatter.hide()
        # Hide settings/events by default
        self.widget_event.hide()
        self.widget_settings.hide()
        self.widget_poly.hide()
        # show the how-to label
        self.label_howto.show()
        # hide the no events label
        self.label_noevents.hide()

    @property
    def rtdc_ds(self):
        """Dataset to plot; set to None initially and if the file is closed"""
        if self._rtdc_ds is not None:
            if not self._check_file_open(self._rtdc_ds):
                self._rtdc_ds = None
        # now check again
        if self._rtdc_ds is None:
            self._set_initial_ui()
        return self._rtdc_ds

    @rtdc_ds.setter
    def rtdc_ds(self, rtdc_ds):
        self._rtdc_ds = rtdc_ds

        # Hide "Subtract Background"-Checkbox if feature
        # "image_bg" not in dataset
        contains_bg_feat = "image_bg" in rtdc_ds
        self.checkBox_image_background.setVisible(contains_bg_feat)

    def get_event_image(self, ds, event):
        state = self.__getstate__()
        imkw = self.imkw.copy()
        cellimg = ds["image"][event]
        # apply background correction
        if "image_bg" in ds:
            if state["event"]["image background"]:
                bgimg = ds["image_bg"][event].astype(np.int16)
                cellimg = cellimg.astype(np.int16)
                cellimg = cellimg - bgimg + int(np.mean(bgimg))
        # automatic contrast
        if state["event"]["image auto contrast"]:
            vmin, vmax = cellimg.min(), cellimg.max()
            cellimg = (cellimg - vmin) / (vmax - vmin) * 255
        # convert to RGB
        cellimg = cellimg.reshape(
            cellimg.shape[0], cellimg.shape[1], 1)
        cellimg = np.repeat(cellimg, 3, axis=2)
        # clip and convert to int
        cellimg = np.clip(cellimg, 0, 255)
        cellimg = np.require(cellimg, np.uint8, 'C')

        # Only load contour data if there is an image column.
        # We don't know how big the images should be so we
        # might run into trouble displaying random contours.
        if "mask" in ds and len(ds["mask"]) > event:
            mask = ds["mask"][event]
            if state["event"]["image contour"]:
                # Compute contour image from mask. If you are wondering
                # whether this is kosher, please take a look at issue #76:
                # https://github.com/ZELLMECHANIK-DRESDEN/dclab/issues/76
                cont = mask ^ binary_erosion(mask)
                # set red contour pixel values in original image
                cellimg[cont, 0] = int(255*.7)
                cellimg[cont, 1] = 0
                cellimg[cont, 2] = 0
            if state["event"]["image zoom"]:
                xv, yv = np.where(mask)
                idminx = xv.min() - 5
                idminy = yv.min() - 5
                idmaxx = xv.max() + 5
                idmaxy = yv.max() + 5
                idminx = idminx if idminx >= 0 else 0
                idminy = idminy if idminy >= 0 else 0
                shx, shy = mask.shape
                idmaxx = idmaxx if idmaxx < shx else shx
                idmaxy = idmaxy if idmaxy < shy else shy
                cellimg = cellimg[idminx:idmaxx, idminy:idmaxy]
        return cellimg, imkw

    def get_statistics(self):
        if self.rtdc_ds is not None:
            features = [self.comboBox_x.currentData(),
                        self.comboBox_y.currentData()]
            h, v = dclab.statistics.get_statistics(ds=self.rtdc_ds,
                                                   features=features,
                                                   methods=STAT_METHODS)
            return h, v
        else:
            return None, None

    def on_event_scatter_clicked(self, plot, point):
        """User clicked on scatter plot

        Parameters
        ----------
        plot: pg.PlotItem
            Active plot
        point: QPoint
            Selected point (determined by scatter plot widget)
        """
        # `self.on_tool` (`self.toolButton_event`) takes care of this:
        # self.widget_scatter.select.show()
        if not self.toolButton_event.isChecked():
            # emulate mouse toggle
            self.toolButton_event.setChecked(True)
            self.toolButton_event.toggled.emit(True)
        if self.widget_scatter.events_plotted is not None:
            # plotted events
            plotted = self.widget_scatter.events_plotted
            # get corrected index
            ds_idx = np.where(plotted)[0][point.index()]
            self.show_event(ds_idx)

    def on_event_scatter_hover(self, pos):
        """Update the image view in the polygon widget """
        if self.rtdc_ds is not None and self.toolButton_poly.isChecked():
            # plotted events
            plotted = self.widget_scatter.events_plotted
            spos = self.widget_scatter.scatter.mapFromView(pos)
            point = self.widget_scatter.scatter.pointAt(spos)
            # get corrected index
            event = np.where(plotted)[0][point.index()]
            if "image" in self.rtdc_ds:
                cellimg, imkw = self.get_event_image(self.rtdc_ds, event)
                self.imageView_image_poly.setImage(cellimg, **imkw)
                self.imageView_image_poly.show()
            else:
                self.imageView_image_poly.hide()

    def on_event_scatter_spin(self, event):
        """Sping control for event selection changed"""
        self.show_event(event - 1)

    def on_event_scatter_update(self):
        """Just update the event shown"""
        event = self.spinBox_event.value()
        self.show_event(event - 1)

    def on_poly_create(self):
        """User wants to create a polygon filter"""
        self.pushButton_poly_create.setEnabled(False)
        if not self.toolButton_poly.isChecked():
            # emulate mouse toggle
            self.toolButton_poly.setChecked(True)
            self.toolButton_poly.toggled.emit(True)
        self.comboBox_poly.setEnabled(False)
        self.groupBox_poly.setEnabled(True)
        self.label_poly_create.setVisible(True)
        self.pushButton_poly_save.setVisible(True)
        self.pushButton_poly_cancel.setVisible(True)
        # defaults
        self.lineEdit_poly.setText("Polygon Filter {}".format(
            dclab.PolygonFilter._instance_counter + 1))
        self.checkBox_poly.setChecked(False)
        self.widget_scatter.activate_poly_mode()
        # trigger resize and redraw
        mdiwin = self.parent()
        mdiwin.adjustSize()
        mdiwin.update()
        self.update()

    def on_poly_done(self):
        """User is done creating or modifying a polygon filter"""
        self.pushButton_poly_create.setEnabled(True)
        self.label_poly_create.setVisible(False)
        self.label_poly_modify.setVisible(False)
        self.pushButton_poly_save.setVisible(False)
        self.pushButton_poly_cancel.setVisible(False)
        if self.sender() == self.pushButton_poly_save:
            # save the polygon filter
            points = self.widget_scatter.get_poly_points()
            name = self.lineEdit_poly.text()
            inverted = self.checkBox_poly.isChecked()
            axes = self.widget_scatter.xax, self.widget_scatter.yax
            # determine whether to create a new polygon filter or whether
            # to update an existing one.
            idp = self.comboBox_poly.currentData()
            if idp is None:
                dclab.PolygonFilter(axes=axes, points=points, name=name,
                                    inverted=inverted)
                mode = "create"
            else:
                pf = dclab.PolygonFilter.get_instance_from_id(idp)
                pf.name = name
                pf.inverted = inverted
                pf.points = points
                mode = "modify"
        else:
            mode = "none"
        # remove the PolyLineRoi
        self.widget_scatter.activate_scatter_mode()
        self.update_polygon_panel()
        if mode == "create":
            self.polygon_filter_created.emit()
        elif mode == "modify":
            self.polygon_filter_modified.emit()

    def on_poly_modify(self):
        """User wants to modify a polygon filter"""
        self.pushButton_poly_create.setEnabled(False)
        self.comboBox_poly.setEnabled(False)
        self.groupBox_poly.setEnabled(True)
        self.label_poly_modify.setVisible(True)
        self.pushButton_poly_save.setVisible(True)
        self.pushButton_poly_cancel.setVisible(True)
        # get the polygon filter id
        idp = self.comboBox_poly.currentData()
        pf = dclab.PolygonFilter.get_instance_from_id(idp)
        # set UI information
        self.lineEdit_poly.setText(pf.name)
        self.checkBox_poly.setChecked(pf.inverted)
        # set axes
        state = self.__getstate__()
        state["plot"]["axis x"] = pf.axes[0]
        state["plot"]["axis y"] = pf.axes[1]
        self.__setstate__(state)
        self.plot()
        # add ROI
        self.widget_scatter.activate_poly_mode(pf.points)

    def on_stats2clipboard(self):
        """Copy the statistics as tsv data to the clipboard"""
        h, v = self.get_statistics()
        if h is not None:
            # assemble tsv data
            tsv = ""
            for hi, vi in zip(h, v):
                tsv += "{}\t{:.7g}\n".format(hi, vi)
            QtWidgets.qApp.clipboard().setText(tsv)

    @show_wait_cursor
    @QtCore.pyqtSlot()
    def on_tool(self, collapse=False):
        """Show and hide tools when the user selected a tool button"""
        toblock = [self.toolButton_event,
                   self.toolButton_poly,
                   self.toolButton_settings,
                   ]
        for b in toblock:
            b.blockSignals(True)
        # show extra data
        show_event = False
        show_poly = False
        show_settings = False
        sender = self.sender()
        if sender == self.toolButton_event:
            show_event = self.toolButton_event.isChecked()
        elif sender == self.toolButton_poly:
            show_poly = self.toolButton_poly.isChecked()
        elif sender == self.toolButton_settings:
            show_settings = self.toolButton_settings.isChecked()
        elif collapse:
            # show nothing
            pass
        else:
            # keep everything as-is but update the sizes
            show_event = self.widget_event.isVisible()
            show_settings = self.widget_settings.isVisible()
            show_poly = self.widget_poly.isVisible()

        # toolbutton checked
        self.toolButton_event.setChecked(show_event)
        self.toolButton_poly.setChecked(show_poly)
        self.toolButton_settings.setChecked(show_settings)

        # widget visibility
        self.widget_event.setVisible(show_event)
        self.widget_scatter.select.setVisible(show_event)  # point in scatter
        self.widget_poly.setVisible(show_poly)
        self.widget_settings.setVisible(show_settings)

        if show_event:
            # update event plot (maybe axes changed)
            self.on_event_scatter_update()

        for b in toblock:
            b.blockSignals(False)

        if not show_poly:
            self.on_poly_done()
        # set size
        self.update()
        ws = self.sizeHint()
        mdiwin = self.parent()
        geom = mdiwin.geometry()
        geom.setWidth(ws.width())
        geom.setHeight(ws.height())
        mdiwin.setGeometry(geom)
        mdiwin.adjustSize()
        mdiwin.update()

    @show_wait_cursor
    @QtCore.pyqtSlot()
    def plot(self):
        """Update the plot using the current state of the UI"""
        if self.rtdc_ds is not None:
            plot = self.__getstate__()["plot"]
            downsample = plot["downsampling"] * plot["downsampling value"]

            self.widget_scatter.plot_data(rtdc_ds=self.rtdc_ds,
                                          slot=self.slot,
                                          downsample=downsample,
                                          xax=plot["axis x"],
                                          yax=plot["axis y"],
                                          xscale=plot["scale x"],
                                          yscale=plot["scale y"],
                                          isoelastics=plot["isoelastics"])
            # make sure the correct plot items are visible
            # (e.g. scatter select)
            self.on_tool()
            # update polygon filter axis names
            self.label_poly_x.setText(
                dclab.dfn.get_feature_label(plot["axis x"]))
            self.label_poly_y.setText(
                dclab.dfn.get_feature_label(plot["axis y"]))
            self.show_statistics()

    @show_wait_cursor
    @QtCore.pyqtSlot(int)
    def show_event(self, event):
        """Display the event data (image, contour, trace)

        Parameters
        ----------
        event: int
            Event index of the dataset; indices start at 0
            If set to None, the index from `self.spinBox_event`
            will be used.
        """
        # dataset
        ds = self.rtdc_ds
        event_count = ds.config["experiment"]["event count"]
        if event_count == 0:
            # nothing to do
            return
        # Update spin box data
        self.spinBox_event.blockSignals(True)
        self.spinBox_event.setValue(event + 1)
        self.spinBox_event.blockSignals(False)

        # Update selection point in scatter plot
        self.widget_scatter.setSelection(event)
        if self.tabWidget_event.currentIndex() == 0:
            # update image
            state = self.__getstate__()
            if "image" in ds:
                cellimg, imkw = self.get_event_image(ds, event)
                self.imageView_image.setImage(cellimg, **imkw)
                self.groupBox_image.show()
            else:
                self.groupBox_image.hide()
            if "trace" in ds:
                # remove legend items
                for item in reversed(self.legend_trace.items):
                    self.legend_trace.removeItem(item[1].text)
                self.legend_trace.setVisible(state["event"]["trace legend"])
                # get slot from identifier
                # time axis
                flsamples = ds.config["fluorescence"]["samples per event"]
                flrate = ds.config["fluorescence"]["sample rate"]
                fltime = np.arange(flsamples) / flrate * 1e6
                # temporal range (min, max, fl-peak-maximum)
                range_t = [fltime[0], fltime[-1], 0]
                # fluorescence intensity
                range_fl = [0, 0]
                for key in dclab.dfn.FLUOR_TRACES:
                    if key.count("raw") and not state["event"]["trace raw"]:
                        # hide raw trace data if user decided so
                        show = False
                    else:
                        show = True
                    flid = key.split("_")[0]
                    if (key in ds["trace"] and show):
                        # show the trace information
                        tracey = ds["trace"][key][event]  # trace data
                        range_fl[0] = min(range_fl[0], tracey.min())
                        range_fl[1] = max(range_fl[1], tracey.max())
                        self.trace_plots[key].setData(fltime, tracey)
                        self.trace_plots[key].show()
                        if state["event"]["trace zoom"]:
                            flpos = ds["{}_pos".format(flid)][event]
                            flwidth = ds["{}_width".format(flid)][event]
                            flmax = ds["{}_max".format(flid)][event]
                            # use the peak maximum to decide which range to use
                            if flmax > range_t[2]:
                                range_t[0] = flpos - 1.5 * flwidth
                                range_t[1] = flpos + 1.5 * flwidth
                                range_t[2] = flmax
                        # set legend name
                        ln = "{} {}".format(self.slot.fl_name_dict[
                            "FL-{}".format(key[2])], key[4:])
                        self.legend_trace.addItem(self.trace_plots[key], ln)
                        self.legend_trace.update()
                    else:
                        self.trace_plots[key].hide()
                self.graphicsView_trace.setXRange(*range_t[:2], padding=0)
                if range_fl[0] != range_fl[1]:
                    self.graphicsView_trace.setYRange(*range_fl, padding=.01)
                self.graphicsView_trace.setLimits(xMin=0, xMax=fltime[-1])
                self.groupBox_trace.show()
            else:
                self.groupBox_trace.hide()
        else:
            # only use computed features (speed)
            fcands = ds.features_loaded
            feats = [f for f in fcands if f in ds.features_scalar]
            lf = sorted([(dclab.dfn.get_feature_label(f), f) for f in feats])
            keys = []
            vals = []
            for lii, fii in lf:
                keys.append(lii)
                val = ds[fii][event]
                if fii in idiom.INTEGER_FEATURES:
                    val = int(np.round(val))
                vals.append(val)
            self.tableWidget_feats.set_key_vals(keys, vals)

    @show_wait_cursor
    def show_rtdc(self, rtdc_ds, slot):
        """Display an RT-DC measurement given by `path` and `filters`"""
        # Create a hierarchy child so that the user can browse
        # comfortably through the data without seeing hidden events.
        self.rtdc_ds = dclab.new_dataset(rtdc_ds)
        event_count = self.rtdc_ds.config["experiment"]["event count"]
        if event_count == 0:
            self.widget_scatter.hide()
            self.widget_tool.setEnabled(False)
            self.label_noevents.show()
            self.on_tool(collapse=True)
            return
        else:
            # make things visible
            self.label_noevents.hide()
            self.label_howto.hide()
            self.widget_scatter.show()
            self.widget_tool.setEnabled(True)
        # get the state
        state = self.__getstate__()
        plot = state["plot"]
        # remove event state (ill-defined for different datasets)
        state.pop("event")

        self.slot = slot
        # default features (plot axes)
        if plot["axis x"] is None:
            plot["axis x"] = "area_um"
        if plot["axis y"] is None:
            plot["axis y"] = "deform"
        # check whether axes exist in ds and change them to defaults
        # if necessary
        ds_features = self.rtdc_ds.features_scalar
        if plot["axis x"] not in ds_features:
            for feat in dclab.dfn.scalar_feature_names:
                if feat in ds_features:
                    plot["axis x"] = feat
                    break
        if plot["axis y"] not in ds_features:
            for feat in dclab.dfn.scalar_feature_names:
                if feat in ds_features:
                    plot["axis y"] = feat
                    if feat != plot["axis y"]:
                        # If there is only one feature, at least we
                        # have set the state to a reasonable value.
                        break
        # set control ranges
        self.spinBox_event.blockSignals(True)
        self.spinBox_event.setMaximum(event_count)
        self.spinBox_event.setToolTip("total: {}".format(event_count))
        self.spinBox_event.setValue(1)
        self.spinBox_event.blockSignals(False)

        # set quick view state
        self.__setstate__(state)
        # scatter plot
        self.plot()
        # select first event in event viewer (also updates selection point)
        self.show_event(0)
        # this only updates the size of the tools (because there is no
        # sender)
        self.on_tool()

    def show_statistics(self):
        h, v = self.get_statistics()
        if h is not None:
            self.tableWidget_stat.set_key_vals(keys=h, vals=v)

    def update_feature_choices(self):
        """Updates the axes comboboxes choices

        This is used e.g. when emodulus becomes available
        """
        if self.rtdc_ds is not None:
            # axes combobox choices
            ds_feats = self.rtdc_ds.features_scalar
            ds_labels = [dclab.dfn.get_feature_label(f) for f in ds_feats]
            ds_fl = sorted(zip(ds_labels, ds_feats))
            for cb in [self.comboBox_x, self.comboBox_y]:
                fcur = cb.currentData()
                blocked = cb.signalsBlocked()  # remember block state
                cb.blockSignals(True)
                # set features
                cb.clear()
                for label, feat in ds_fl:
                    if feat in ds_feats:
                        cb.addItem(label, feat)
                idcur = cb.findData(fcur)
                if idcur >= 0:
                    cb.setCurrentIndex(idcur)
                cb.blockSignals(blocked)

    def update_polygon_panel(self):
        """Update polygon filter combobox etc."""
        pfts = dclab.PolygonFilter.instances
        if pfts:
            self.comboBox_poly.blockSignals(True)
            self.comboBox_poly.clear()
            self.comboBox_poly.addItem("Choose...", None)
            for pf in pfts:
                self.comboBox_poly.addItem(pf.name, pf.unique_id)
            self.comboBox_poly.blockSignals(False)
            self.comboBox_poly.setEnabled(True)
        else:
            self.comboBox_poly.setEnabled(False)
        self.groupBox_poly.setEnabled(False)
