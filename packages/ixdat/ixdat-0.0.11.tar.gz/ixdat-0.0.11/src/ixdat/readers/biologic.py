"""This module implements the Reader for .mpt files made by BioLogic's EC-Lab software

Demonstrated/tested at the bottom under `if __name__ == "__main__":`
"""

from pathlib import Path
import re
import numpy as np

from . import TECHNIQUE_CLASSES
from ..data_series import TimeSeries, ValueSeries
from ..exceptions import ReadError
from .reading_tools import timestamp_string_to_tstamp

ECMeasurement = TECHNIQUE_CLASSES["EC"]
delim = "\t"
t_str = "time/s"
regular_expressions = {
    "N_header_lines": "Nb header lines : (.+)\n",
    "timestamp_string": "Acquisition started on : (.+)\n",
    "loop": "Loop ([0-9]+) from point number ([0-9]+) to ([0-9]+)",
}


class BiologicMPTReader:
    """A class to read .mpt files written by Biologic's EC-Lab.

    read() is the important method - it takes the path to the mpt file as argument
    and returns an ECMeasurement object (ec_measurement) representing that file.
    The ECMeasurement contains a reference to the BiologicMPTReader object, as
    ec_measurement.reader. This makes available all the following stuff, likely
    useful for debugging.

    Attributes:
        path_to_file (Path): the location and name of the file read by the reader
        n_line (int): the number of the last line read by the reader
        place_in_file (str): The last location in the file read by the reader. This
            is used internally to tell the reader how to parse each line. Options are:
            "header", "column names", and "data".
        header_lines (list of str): a list of the header lines of the files. This
            includes the column name line. The header can be nicely viewed with the
            print_header() function.
        timestamp_string (str): The string identified to represent the t=0 time of the
            measurement recorded in the file.
        tstamp (str): The unix time corresponding to t=0, parsed from timestamp_string
        ec_technique (str): The name of the electrochemical sub-technique, i.e.
            "Cyclic Voltammatry Advanced", etc.
        N_header_lines (int): The number of lines in the header of the file
        column_names (list of str): The names of the data columns in the file
        column_data (dict of str: np.array): The data in the file as a dict.
            Note that the np arrays are the same ones as in the measurement's DataSeries,
            so this does not waste memory.
        file_has_been_read (bool): This is used to make sure read() is only successfully
            called once by the Reader. False until read() is called, then True.
        measurement (Measurement): The measurement returned by read() when the file is
            read. self.measureemnt is None before read() is called.
    """

    def __init__(self):
        """Initialize a Reader for .mpt files. See class docstring."""
        self.name = None
        self.path_to_file = None
        self.n_line = 0
        self.place_in_file = "header"
        self.header_lines = []
        self.timestamp_string = None
        self.tstamp = None
        self.ec_technique = None
        self.N_header_lines = None
        self.column_names = []
        self.column_data = {}
        self.file_has_been_read = False
        self.measurement = None

    def read(self, path_to_file, name=None, cls=None, **kwargs):
        """Return an ECMeasurement with the data and metadata recorded in path_to_file

        This loops through the lines of the file, processing one at a time. For header
        lines, this involves searching for metadata. For the column name line, this
        involves creating empty arrays for each data series. For the data lines, this
        involves appending to these arrays. After going through all the lines, it
        converts the arrays to DataSeries.
        For .mpt files, there is one TimeSeries, with name "time/s", and all other data
        series are ValueSeries sharing this TimeSeries.
        Finally, the method returns an ECMeasurement with these DataSeries. The
        ECMeasurement contains a reference to the reader.

        Args:
            path_to_file (Path): The full abs or rel path including the ".mpt" extension
            name (str): The name to use if not the file name
            cls (Measurement subclass): The Measurement class to return an object of.
                Defaults to `ECMeasurement` and should probably be a subclass thereof in
                any case.
            **kwargs (dict): Key-word arguments are passed to cls.__init__
        """
        path_to_file = Path(path_to_file) if path_to_file else self.path_to_file
        if self.file_has_been_read:
            print(
                f"This {self.__class__.__name__} has already read {self.path_to_file}."
                " Returning the measurement resulting from the original read. "
                "Use a new Reader if you want to read another file."
            )
            return self.measurement
        self.name = name or path_to_file.name
        self.path_to_file = path_to_file
        self.measurement_class = cls or ECMeasurement
        with open(self.path_to_file, "r", encoding="ISO-8859-1") as f:
            for line in f:
                self.process_line(line)
        for name in self.column_names:
            self.column_data[name] = np.array(self.column_data[name])

        if t_str not in self.column_data:
            raise ReadError(
                f"{self} did not find any data for t_str='{t_str}'. "
                f"This reader only works for files with a '{t_str}' column"
            )
        tseries = TimeSeries(
            name=t_str,
            data=self.column_data[t_str],
            tstamp=self.tstamp,
            unit_name="s",
        )
        data_series_list = [tseries]
        for column_name, data in self.column_data.items():
            if column_name == t_str:
                continue
            vseries = ValueSeries(
                name=column_name,
                data=data,
                tseries=tseries,
                unit_name=get_column_unit(column_name),
            )
            data_series_list.append(vseries)

        obj_as_dict = dict(
            name=self.name,
            technique="EC",
            reader=self,
            series_list=data_series_list,
            tstamp=self.tstamp,
            ec_technique=self.ec_technique,
        )
        obj_as_dict.update(kwargs)

        self.measurement = self.measurement_class.from_dict(obj_as_dict)
        self.file_has_been_read = True

        return self.measurement

    def process_line(self, line):
        """Call the correct line processing method depending on self.place_in_file"""
        if self.place_in_file == "header":
            self.process_header_line(line)
        elif self.place_in_file == "column names":
            self.process_column_line(line)
        elif self.place_in_file == "data":
            self.process_data_line(line)
        else:  # just for debugging
            raise ReadError(f"place_in_file = {self.place_in_file}")
        self.n_line += 1

    def process_header_line(self, line):
        """Search line for important metadata and set the relevant attribute of self"""
        self.header_lines.append(line)
        if not self.N_header_lines:
            N_head_match = re.search(regular_expressions["N_header_lines"], line)
            if N_head_match:
                self.N_header_lines = int(N_head_match.group(1))
                return
        if self.n_line == 3:
            self.ec_technique = line.strip()
            return
        if not self.timestamp_string:
            timestamp_match = re.search(regular_expressions["timestamp_string"], line)
            if timestamp_match:
                self.timestamp_string = timestamp_match.group(1)
                self.tstamp = timestamp_string_to_tstamp(
                    self.timestamp_string, forms=BIOLOGIC_TIMESTAMP_FORMS
                )
            return
        loop_match = re.search(regular_expressions["loop"], line)
        if loop_match:
            # print(f"loop specified on line='{line}'")  # debugging
            n = int(loop_match.group(1))
            start = int(loop_match.group(2))
            finish = int(loop_match.group(3))
            if "loop_number" not in self.column_data:
                self.column_data["loop_number"] = np.array([])
            self.column_data["loop_number"] = np.append(
                self.column_data["loop_number"], np.array([n] * (finish - start + 1))
            )
            return

        if self.N_header_lines and self.n_line >= self.N_header_lines - 2:
            self.place_in_file = "column names"

    def process_column_line(self, line):
        """Split the line to get the names of the file's data columns"""
        self.header_lines.append(line)
        self.column_names = line.strip().split(delim)
        self.column_data.update({name: [] for name in self.column_names})
        self.place_in_file = "data"

    def process_data_line(self, line):
        """Split the line and append the numbers the corresponding data column arrays"""
        data_strings_from_line = line.strip().split()
        for name, value_string in zip(self.column_names, data_strings_from_line):
            try:
                value = float(value_string)
            except ValueError:
                if "," in value_string:  # oh my god, why?!
                    value_string = value_string.replace(",", ".")
                try:
                    value = float(value_string)
                except ValueError:
                    raise ReadError(f"can't parse value string '{value_string}'")
            self.column_data[name].append(value)

    def print_header(self):
        """Print the file header including column names. read() must be called first."""
        header = "".join(self.header_lines)
        print(header)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.path_to_file})"


def get_column_unit(column_name):
    """Return the unit name of a .mpt column, i.e the part of the name after the '/'"""
    if "/" in column_name:
        unit_name = column_name.split("/")[-1]
    else:
        unit_name = None
    return unit_name


BIOLOGIC_TIMESTAMP_FORMS = (
    "%m/%d/%Y %H:%M:%S",  # like 07/29/2020 10:31:03
    "%m-%d-%Y %H:%M:%S",  # like 01-31-2020 10:32:02
)

# This tuple contains variable names encountered in .mpt files. The tuple can be used by
#   other modules to tell which data is from biologic.
BIOLOGIC_COLUMN_NAMES = (
    "mode",
    "ox/red",
    "error",
    "control changes",
    "time/s",
    "control/V",
    "Ewe/V",
    "<I>/mA",
    "(Q-Qo)/C",
    "P/W",
    "loop number",
    "I/mA",
    "control/mA",
    "Ns changes",
    "counter inc.",
    "cycle number",
    "Ns",
    "(Q-Qo)/mA.h",
    "dQ/C",
    "Q charge/discharge/mA.h",
    "half cycle",
    "Capacitance charge/µF",
    "Capacitance discharge/µF",
    "dq/mA.h",
    "Q discharge/mA.h",
    "Q charge/mA.h",
    "Capacity/mA.h",
    "file number",
    "file_number",
    "Ece/V",
    "Ewe-Ece/V",
    "<Ece>/V",
    "<Ewe>/V",
    "Energy charge/W.h",
    "Energy discharge/W.h",
    "Efficiency/%",
    "Rcmp/Ohm",
)


if __name__ == "__main__":
    """Module demo here.

    To run this module in PyCharm, open Run Configuration and set
        Module name = ixdat.readers.biologic,
    and *not*
        Script path = ...
    """

    from matplotlib import pyplot as plt
    from ixdat.measurements import Measurement

    test_data_dir = (
        Path(__file__).parent.parent.parent.parent
        / "test_data/biologic_mpt_and_zilien_tsv"
    )

    path_to_test_file = (
        test_data_dir / "2020-07-29 10_30_39 Pt_poly_cv_01_02_CVA_C01.mpt"
    )

    ec_measurement = Measurement.read(
        reader="biologic",
        path_to_file=path_to_test_file,
    )

    t, v = ec_measurement.grab_potential(tspan=[0, 100])

    ec_measurement.tstamp -= 20
    t_shift, v_shift = ec_measurement.grab_potential(tspan=[0, 100])

    fig, ax = plt.subplots()
    ax.plot(t, v, "k", label="original tstamp")
    ax.plot(t_shift, v_shift, "r", label="shifted tstamp")
    ax.legend()
