import pandas as pd
from ..categorisation import GeneralCatergorisation


class VenaLT_Prework(GeneralCatergorisation):

    def required_cols(self, timeseries, search_value, num_of_nearest_channels):
        heights = self.measurement_height(timeseries)

        lower_values = []
        higher_values = []

        # Iterate through the list to find nearest values
        lower_values = sorted(
            [num for num in heights if num < search_value], reverse=True
        )[:num_of_nearest_channels]

        # Find nearest greater numbers
        higher_values = sorted([num for num in heights if num > search_value])[
            :num_of_nearest_channels
        ]

        req_heights = lower_values + higher_values
        req_cols = []
        for height in req_heights:
            col_name = f"WS_{height}_mean"
            req_cols.append(col_name)
        return req_cols

    def find_nearest_height(self, all_heights, target_height_to_be_sheared):
        # Find the nearest heigths for calculating shear values

        closest_heights = min(
            all_heights, key=lambda x: abs(x - target_height_to_be_sheared)
        )
        return closest_heights
