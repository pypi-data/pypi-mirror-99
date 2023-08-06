import copy

import dclab
from dclab.features.emodulus.viscosity import KNOWN_MEDIA
import numpy as np

from .. import meta_tool
from ..util import hashobj


class Dataslot(object):
    """Handles datasets in a pipeline"""
    _instance_counter = 0
    _instances = {}

    def __init__(self, path, identifier=None, name=None):
        Dataslot._instance_counter += 1
        self.path = path
        self._dataset = None
        if identifier is None:
            identifier = "Dataslot_{}".format(Dataslot._instance_counter)
            while identifier in Dataslot._instances:
                Dataslot._instance_counter += 1
                identifier = "Dataslot_{}".format(Dataslot._instance_counter)
        cfg = meta_tool.get_rtdc_config(path)
        if name is None:
            name = cfg["experiment"]["sample"]
        #: unique identifier of the filter
        self.identifier = identifier
        #: user-defined name of the filter
        self.name = name
        #: whether or not to use this slot
        self.slot_used = True
        if identifier in Dataslot._instances:
            raise ValueError("Dataslot with identifier "
                             + "'{}' already exists!".format(identifier))
        Dataslot._instances[identifier] = self
        self.color = random_color()
        self.fl_name_dict = {"FL-1": "FL-1",
                             "FL-2": "FL-2",
                             "FL-3": "FL-3"}
        is_channel = cfg["setup"]["chip region"] == "channel"
        self.config = {
            "crosstalk": {
                # crosstalk
                "crosstalk fl12": 0,
                "crosstalk fl13": 0,
                "crosstalk fl21": 0,
                "crosstalk fl23": 0,
                "crosstalk fl31": 0,
                "crosstalk fl32": 0,
            },
            "emodulus": {
                # emodulus
                "emodulus enabled": is_channel,  # False for reservoir
                "emodulus lut": "LE-2D-FEM-19",
                "emodulus medium": "undefined",
                # https://dclab.readthedocs.io/en/latest/sec_av_emodulus.html
                # possible values are:
                # - "feature": scenario A
                # - None: secnario B ("emodulus medium" is "other" or user-def)
                # - "config": scenario C (temperature taken from config)
                # - "manual": scenario C (temperature entered manually)
                "emodulus scenario": "manual",
                "emodulus temperature": np.nan,
                "emodulus viscosity": np.nan,
            }
        }

        # use the emodulus medium and temperature values as defaults
        ds = self.get_dataset()
        calc = self.config["emodulus"]
        if "medium" in ds.config["setup"]:
            calc["emodulus medium"] = ds.config["setup"]["medium"]
        if "temp" in ds:
            # use the "temp" feature
            calc["emodulus scenario"] = "feature"
        elif "temperature" in ds.config["setup"]:
            # use the average temperature
            calc["emodulus temperature"] = ds.config["setup"]["temperature"]
            calc["emodulus scenario"] = "config"

        #: data file format
        self.format = self.get_dataset().format

    def __getstate__(self):
        state = {"color": self.color,
                 "crosstalk": self.config["crosstalk"],
                 "emodulus": self.config["emodulus"],
                 "fl names": self.fl_name_dict,
                 "identifier": self.identifier,
                 "name": self.name,
                 "path": self.path,
                 "slot used": self.slot_used,
                 }
        return copy.deepcopy(state)

    def __repr__(self):
        repre = "<Pipeline Slot '{}' at {}>".format(self.identifier,
                                                    hex(id(self)))
        return repre

    def __setstate__(self, state):
        if self.identifier != state["identifier"]:
            raise ValueError("Identifier mismatch: '{}' vs. '{}'".format(
                self.identifier, state["identifier"]))
        self.color = state["color"]
        self.config["crosstalk"].update(state["crosstalk"])
        self.config["emodulus"].update(state["emodulus"])
        self.fl_name_dict = state["fl names"]
        self.name = state["name"]
        self.path = state["path"]
        self.slot_used = state["slot used"]

    @staticmethod
    def get_slot(slot_id):
        """Get the slot with the given identifier"""
        return Dataslot._instances[slot_id]

    @staticmethod
    def get_instances():
        return Dataslot._instances

    @staticmethod
    def remove_slot(slot_id):
        """Remove a slot taking care of closing any opened files"""
        slot = Dataslot.get_slot(slot_id)
        ds = slot._dataset
        if ds is not None:
            if isinstance(ds, dclab.rtdc_dataset.RTDC_HDF5):
                ds._h5.close()
        Dataslot._instances.pop(slot_id)

    @property
    def hash(self):
        """Return the hash of the slot"""
        return hashobj(self.__getstate__())

    def _set_emodulus_config(self, dataset):
        """Set the Young's modulus data options

        The three cases in the dclab docs apply:
        https://dclab.readthedocs.io/en/latest/sec_av_emodulus.html
        """
        # remove any information
        for key in self.config["emodulus"]:
            if key in dataset.config["calculation"]:
                dataset.config["calculation"].pop(key)

        lut = self.config["emodulus"]["emodulus lut"]
        medium = self.config["emodulus"]["emodulus medium"]
        visc = self.config["emodulus"]["emodulus viscosity"]
        scenario = self.config["emodulus"]["emodulus scenario"]
        if scenario == "config":
            # Force the temperature from the dataset metadata
            # (this is a failsafe, the user/developer might not have set it)
            temp = dataset.config["setup"]["temperature"]
        elif scenario == "manual":
            # Only here do we actually need the temperature stored
            temp = self.config["emodulus"]["emodulus temperature"]
        else:
            # Temperature is not used in these scenarios.
            temp = np.nan

        dataset.config["calculation"]["emodulus lut"] = lut
        # known media
        if medium in dclab.features.emodulus.viscosity.KNOWN_MEDIA:
            dataset.config["calculation"]["emodulus medium"] = medium
        # temperature
        if not np.isnan(temp):
            dataset.config["calculation"]["emodulus temperature"] = temp
        # viscosity
        if medium not in KNOWN_MEDIA and not np.isnan(visc):
            dataset.config["calculation"]["emodulus viscosity"] = visc

    def get_dataset(self):
        """Return the corresponding dataset

        Returns
        -------
        ds: dclab.RTDCBase
            Loaded dataset
        """
        if self._dataset is None:
            ds = dclab.new_dataset(self.path, identifier=self.identifier)
            self._dataset = ds
        else:
            ds = self._dataset
        self.update_dataset(ds)
        return ds

    def update_dataset(self, dataset):
        """Update the configuration of an instance of RTDCBase

        This is used to update the configuration for computing
        the Young's modulus and fluorescence crosstalk.
        """
        # emodulus
        self._set_emodulus_config(dataset)

        # crosstalk
        if np.sum(list(self.config["crosstalk"].values())):
            dataset.config["calculation"].update(self.config["crosstalk"])
        else:
            # remove any information
            for key in self.config["crosstalk"]:
                if key in dataset.config["calculation"]:
                    dataset.config["calculation"].pop(key)


def random_color():
    color = "#"
    for _ in range(3):
        # dark colors (until 200)
        part = hex(np.random.randint(0, 200))[2:]
        if len(part) == 1:
            part += "0"
        color += part
    return color.upper()
