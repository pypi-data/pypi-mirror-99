"""Import readers and build the READER_CLASSES dictionary for direct import

Constants:
    READER_CLASSES (dict): Dictionary of {reader_name: ReaderClass} where
        reader_name is the name of the backend (like "directory") and ReaderClass
        is the reader class for parsing files.
"""
from ..techniques import TECHNIQUE_CLASSES

# ixdat
from .ixdat_csv import IxdatCSVReader

# potentiostats
from .biologic import BiologicMPTReader
from .autolab import NovaASCIIReader
from .ivium import IviumDatasetReader

# mass spectrometers
from .pfeiffer import PVMassSpecReader
from .cinfdata import CinfdataTXTReader

# ec-ms
from .zilien import ZilienTSVReader, ZilienTMPReader
from .ec_ms_pkl import EC_MS_CONVERTER

READER_CLASSES = {
    "ixdat": IxdatCSVReader,
    "biologic": BiologicMPTReader,
    "autolab": NovaASCIIReader,
    "ivium": IviumDatasetReader,
    "pfeiffer": PVMassSpecReader,
    "cinfdata": CinfdataTXTReader,
    "zilien": ZilienTSVReader,
    "zilien_tmp": ZilienTMPReader,
    "EC_MS": EC_MS_CONVERTER,
}
