import pandas as pd
import re

from .categorisation import GeneralCatergorisation


class AdHoc_Processes(GeneralCatergorisation):

    def get_time_interval(self, timeseries):
        # get timeinterval for a timeseries that occurs the maximum time

        intervals = timeseries.index[1:] - timeseries.index[:-1]
        interval_counts = intervals.value_counts()
        most_common_interval = interval_counts.idxmax()
        interval_in_minutes = most_common_interval.total_seconds() / 60
        return interval_in_minutes

    def lidar_offset(self, lidar_data, offset):
        # Applies offset for data channel in Zx lidar , Currently only takes in data channel named according to WP naming convention.

        ws = []
        for col in lidar_data:
            if "ws" in col.lower():
                height = int(re.findall("\d+", col)[0])
                col_renamed = f"WS_{height+offset}_mean"
                lidar_data = lidar_data.rename(columns={col: col_renamed})
                ws.append(col_renamed)
            if "wd" in col.lower():
                height = int(re.findall("\d+", col)[0])
                col_renamed = f"WD_{height+offset}_mean"
                lidar_data = lidar_data.rename(columns={col: col_renamed})
                ws.append(col_renamed)
        return lidar_data

    def measurement_height(self, measurement_data):
        # Outputs measurement heights for all windspeed columns

        heights = []
        ws_cols = self.get_windspeed_cols(measurement_data)
        measurement_data = measurement_data[ws_cols]

        for col in measurement_data:
            matches = re.findall("\d+", col)
            if matches:
                h = int(matches[0])
                if h not in heights:
                    heights.append(h)
        return heights
