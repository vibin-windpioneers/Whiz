import numpy as np
import pandas as pd
import re


class ZX_Lidar_Catergorisation:

    def zx_lidar_channels_to_wp_format(self, timeseries):
        # Applies offset for data channel in Zx lidar , Currently only takes in data channel named according to WP naming convention.
        ws = []
        for col in timeseries:
            if ("ws" in col.lower()) and ("vws" not in col.lower()):
                height = int(re.findall("\d+", col)[0])
                col_renamed = f"WS_{height}_mean"
                timeseries = timeseries.rename(columns={col: col_renamed})
                ws.append(col_renamed)
            if "wd" in col.lower():
                height = int(re.findall("\d+", col)[0])
                col_renamed = f"WD_{height}_mean"
                timeseries = timeseries.rename(columns={col: col_renamed})
                ws.append(col_renamed)
        return timeseries
