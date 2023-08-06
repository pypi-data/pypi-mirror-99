"""Module for representation and analysis of EC-MS measurements"""
from .ec import ECMeasurement
from .ms import MSMeasurement
from .cv import CyclicVoltammagram
from ..exporters.ecms_exporter import ECMSExporter


class ECMSMeasurement(ECMeasurement, MSMeasurement):
    """Class for raw EC-MS functionality. Parents: ECMeasurement and MSMeasurement"""

    extra_column_attrs = {
        # FIXME: It would be more elegant if this carried over from both parents
        #   That might require some custom inheritance definition...
        "ecms_meaurements": {
            "mass_aliases",
            "signal_bgs",
            "ec_technique",
            "RE_vs_RHE",
            "R_Ohm",
            "raw_potential_names",
            "A_el",
            "raw_current_names",
        },
    }

    def __init__(self, **kwargs):
        """FIXME: Passing the right key-word arguments on is a mess"""
        ec_kwargs = {
            k: v for k, v in kwargs.items() if k in ECMeasurement.get_all_column_attrs()
        }
        ms_kwargs = {
            k: v for k, v in kwargs.items() if k in MSMeasurement.get_all_column_attrs()
        }
        # FIXME: I think the lines below could be avoided with a PlaceHolderObject that
        #  works together with MemoryBackend
        if "series_list" in kwargs:
            ec_kwargs.update(series_list=kwargs["series_list"])
            ms_kwargs.update(series_list=kwargs["series_list"])
        if "component_measurements" in kwargs:
            ec_kwargs.update(component_measurements=kwargs["component_measurements"])
            ms_kwargs.update(component_measurements=kwargs["component_measurements"])
        ECMeasurement.__init__(self, **ec_kwargs)
        MSMeasurement.__init__(self, **ms_kwargs)

    @property
    def plotter(self):
        """The default plotter for ECMSMeasurement is ECMSPlotter"""
        if not self._plotter:
            from ..plotters.ecms_plotter import ECMSPlotter

            self._plotter = ECMSPlotter(measurement=self)

        return self._plotter

    @property
    def exporter(self):
        """The default plotter for ECMSMeasurement is ECMSExporter"""
        if not self._exporter:
            self._exporter = ECMSExporter(measurement=self)
        return self._exporter

    def as_cv(self):
        self_as_dict = self.as_dict()

        # FIXME: The following lines are only necessary because
        #  PlaceHolderObject.get_object isn't able to find things in the MemoryBackend
        del self_as_dict["s_ids"]
        self_as_dict["series_list"] = self.series_list

        return ECMSCyclicVoltammogram.from_dict(self_as_dict)


class ECMSCyclicVoltammogram(CyclicVoltammagram, MSMeasurement):
    """Class for raw EC-MS functionality. Parents: CyclicVoltammogram, MSMeasurement

    FIXME: Maybe this class should instead inherit from ECMSMeasurement and
        just add the CyclicVoltammogram functionality?
    """

    extra_column_attrs = {
        # FIXME: It would be more elegant if this carried over from both parents
        #   That might require some custom inheritance definition...
        "ecms_meaurements": {
            "mass_aliases",
            "signal_bgs",
            "ec_technique",
            "RE_vs_RHE",
            "R_Ohm",
            "raw_potential_names",
            "A_el",
            "raw_current_names",
        },
    }

    def __init__(self, **kwargs):
        """FIXME: Passing the right key-word arguments on is a mess"""
        ec_kwargs = {
            k: v for k, v in kwargs.items() if k in ECMeasurement.get_all_column_attrs()
        }
        ec_kwargs.update(series_list=kwargs["series_list"])
        ECMeasurement.__init__(self, **ec_kwargs)
        ms_kwargs = {
            k: v for k, v in kwargs.items() if k in MSMeasurement.get_all_column_attrs()
        }
        ms_kwargs.update(series_list=kwargs["series_list"])
        MSMeasurement.__init__(self, **ms_kwargs)
        self.plot = self.plotter.plot_vs_potential

    @property
    def plotter(self):
        """The default plotter for ECMSCyclicVoltammogram is ECMSPlotter"""
        if not self._plotter:
            from ..plotters.ecms_plotter import ECMSPlotter

            self._plotter = ECMSPlotter(measurement=self)

        return self._plotter

    @property
    def exporter(self):
        """The default plotter for ECMSCyclicVoltammogram is ECMSExporter"""
        if not self._exporter:
            self._exporter = ECMSExporter(measurement=self)
        return self._exporter
