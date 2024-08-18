import numpy as np
import os
import pandas as pd
from ..utils import logger


logger = logger.get_logger()


class InputOutput:

    def skip_to(self, path, search_word="Date/Time", nodata_value=9999, **kwargs):

        # skip the metadata and start loading data from the timestamp data column with the search word
        # path : the location of the timeseries file
        # nodata_value : default = 9999
        # *kwargs for pandas.read_csv function

        if os.stat(path).st_size == 0:
            raise ValueError("File is empty")
        with open(path) as f:

            pos = 0
            cur_line = f.readline()
            while not cur_line.startswith(search_word):
                pos = f.tell()
                cur_line = f.readline()
            f.seek(pos)
            timeseries_data = pd.read_csv(f, **kwargs)
            timeseries_data[timeseries_data == nodata_value] = np.nan
            logger.debug("Time series loaded with skip_to function")
            return timeseries_data

    def windcube_meta_data(self, path, search_word, **kwargs):

        # Get meta data for windcube_lidar and windographer exports as dictionaries
        # search_word : the firdst column name
        # path : location of the timeseries file

        if os.stat(path).st_size == 0:
            raise ValueError("File is empty")
        lines_to_read = ""
        metadata_dict = {}
        with open(path) as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.startswith(search_word):
                    break
                else:
                    if "=" in line:
                        key, value = line.split("=", 1)
                        # Remove leading and trailing whitespaces
                        key = key.strip()
                        value = value.strip()
                        metadata_dict[key] = value

        return metadata_dict
