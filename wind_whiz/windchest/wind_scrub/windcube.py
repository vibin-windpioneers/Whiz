import pandas as pd

from ..adhoc_processes import AdHoc_Processes


class WindCube_Clean(AdHoc_Processes):

    def windcube_data_filter(self, measurement_data, flag_cols, threshold):
        # threshold : the data availabilty percentage to clean the data
        # measurement_data : measurement data in wp_format
        # flags : L -> Low Quality , currently only low quality filter is implimented

        heights = self.measurement_height(measurement_data=measurement_data)
        for h in heights:
            search_value_str = str(h)
            search_value_str
            associated_cols_for_the_height = [
                col for col in flag_cols if search_value_str in col
            ]
            measurement_data.loc[
                (measurement_data[f"{h}m Data Availability (%)"] < threshold),
                associated_cols_for_the_height,
            ] = "L"

        measurement_data.loc[
            (measurement_data["P_1_mean"] > 1800)
            | (measurement_data["P_1_mean"] < 600),
            "P_1_mean_flag",
        ] = "L"
        measurement_data.loc[
            (measurement_data["T_1_mean"] > 70) | (measurement_data["T_1_mean"] < -50),
            "P_1_mean_flag",
        ] = "L"
        measurement_data.loc[
            (measurement_data["RH_1_mean"] > 110) | (measurement_data["RH_1_mean"] < 0),
            "P_1_mean_flag",
        ] = "L"
        return measurement_data
