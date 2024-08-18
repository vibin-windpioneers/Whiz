import numpy as np
import pandas as pd
import re


class GeneralCatergorisation:

    def get_windspeed_cols(self, timeseries):
        # Input timeseries should be in WP format or in Windcube format

        ws = []
        for col in timeseries:
            if (
                "ws" in col.lower()
                and "mean" in col.lower()
                and "vws" not in col.lower()
                and "_flag" not in col.lower()
            ) and (
                "vws" not in col.lower()
                or "dispersion" not in col.lower()
                or "min" not in col.lower()
                or "max" not in col.lower()
            ):
                ws.append(col)
        return ws

    def get_flagcols(self, timeseries):
        flag_cols = []
        for col in timeseries:
            if "_flag" in col.lower():
                flag_cols.append(col)
        return flag_cols
