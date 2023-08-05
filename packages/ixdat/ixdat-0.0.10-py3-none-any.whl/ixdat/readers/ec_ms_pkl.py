from pathlib import Path
from . import TECHNIQUE_CLASSES
import pickle
from ..data_series import TimeSeries, ValueSeries
from ..measurements import Measurement
from .biologic import BIOLOGIC_COLUMN_NAMES, get_column_unit


ECMSMeasruement = TECHNIQUE_CLASSES["EC-MS"]


class EC_MS_CONVERTER:
    """Imports old .pkl files obtained from the legacy EC-MS package"""

    def __init__(self):
        print("Reader of old ECMS .pkl files")

    def read(self, file_path, cls=None, **kwargs):
        """Return an ECMSMeasurement with the data recorded in path_to_file
        Most of the work is done by module-level function measurement_from_ec_ms_dataset

        Args:
            path_to_file (Path): The full abs or rel path including the
            ".pkl" extension.
        """
        with open(file_path, "rb") as f:
            ec_ms_dict = pickle.load(f)

        return measurement_from_ec_ms_dataset(
            ec_ms_dict,
            name=Path(file_path).name,
            cls=cls,
            reader=self,
            technique="EC-MS",
            **kwargs,
        )


def measurement_from_ec_ms_dataset(
    ec_ms_dict,
    name=None,
    cls=ECMSMeasruement,
    reader=None,
    **kwargs,
):
    """Return an ixdat Measurement with the data from an EC_MS data dictionary.

    This loops through the keys of the EC-MS dict and searches for MS and
    EC data. Names the dataseries according to their names in the original
    dict. Omitts any other data as well as metadata.

    Args:
        ec_ms_dict (dict): The EC_MS data dictionary
        name (str): Name of the measurement
        cls (Measurement class): The class to return a measurement of
        reader (Reader object): typically what calls this funciton with its read() method
    """

    cols_str = ec_ms_dict["data_cols"]
    cols_list = []

    name = name or ec_ms_dict.get("title", None)

    for col in cols_str:
        if col.endswith("-x"):
            cols_list.append(
                TimeSeries(col, "s", ec_ms_dict[col], ec_ms_dict["tstamp"])
            )

    if "time/s" in ec_ms_dict:
        cols_list.append(
            TimeSeries("time/s", "s", ec_ms_dict["time/s"], ec_ms_dict["tstamp"])
        )

    measurement = Measurement("tseries_ms", technique="EC_MS", series_list=cols_list)

    for col in cols_str:
        if col.endswith("-y"):
            unit_name = "A" if col.startswith("M") else ""
            cols_list.append(
                ValueSeries(
                    col[:-2],
                    unit_name=unit_name,
                    data=ec_ms_dict[col],
                    tseries=measurement[col[:-1] + "x"],
                )
            )
        if col in BIOLOGIC_COLUMN_NAMES and col not in measurement.series_names:
            cols_list.append(
                ValueSeries(
                    name=col,
                    data=ec_ms_dict[col],
                    unit_name=get_column_unit(col),
                    tseries=measurement["time/s"],
                )
            )

    obj_as_dict = dict(
        name=name,
        technique="EC_MS",
        series_list=cols_list,
        reader=reader,
        tstamp=ec_ms_dict["tstamp"],
    )
    obj_as_dict.update(kwargs)

    measurement = cls.from_dict(obj_as_dict)
    return measurement
