import numpy as np
import pandas as pd
import re


class WindCube_Catergorisation:

    def windcube_channels_to_wp_format(self, measurement_data):

        # vitals
        wiper_count = []
        battery = []
        int_temp = []

        # Windspeed associated cols
        ws = []
        ws_dispersion = []
        ws_min = []
        ws_max = []

        # z-wind associated cols
        vws = []
        vws_dispersion = []

        # Wind direction associated cols
        wd = []

        # cnr associated cols
        cnr = []
        cnr_min = []
        dopp_spect = []
        data_availability = []

        # ambient measurements
        temp = []
        rh = []
        pressure = []

        for col in measurement_data.columns:
            if ("wind speed (m/s)" in col.lower()) and (
                "dispersion" not in col.lower()
                or "min" not in col.lower()
                or "max" not in col.lower()
            ):
                col_renamed = "WS_" + re.findall("\d+", col)[0] + "_mean"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                ws.append(col_renamed)
            if ("wind speed dispersion (m/s)" in col.lower()) and (
                "min" not in col.lower() or "max" not in col.lower()
            ):
                col_renamed = "WS_" + re.findall("\d+", col)[0] + "_dispersion"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                ws_dispersion.append(col_renamed)
            if ("wind speed min (m/s)" in col.lower()) and (
                "dispersion" not in col.lower() or "max" not in col.lower()
            ):
                col_renamed = "WS_" + re.findall("\d+", col)[0] + "_min"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                ws_min.append(col_renamed)
            if ("wind speed max (m/s)" in col.lower()) and (
                "dispersion" not in col.lower() or "min" not in col.lower()
            ):
                col_renamed = "WS_" + re.findall("\d+", col)[0] + "_max"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                ws_max.append(col_renamed)

            if ("z-wind (m/s)" in col.lower()) and ("dispersion" not in col.lower()):
                col_renamed = "VWS_" + re.findall("\d+", col)[0] + "_mean"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                vws.append(col_renamed)
            if "z-wind dispersion (m/s)" in col.lower():
                col_renamed = "VWS_" + re.findall("\d+", col)[0] + "_dispersion"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                vws_dispersion.append(col_renamed)

            if "wind direction (°)" in col.lower():
                col_renamed = "WD_" + re.findall("\d+", col)[0] + "_mean"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                wd.append(col_renamed)

            if ("cnr (db)" in col.lower()) and ("min" not in col.lower()):
                cnr.append(col)
            if "cnr min (db)" in col.lower():
                cnr_min.append(col)
            if "cnr min (db)" in col.lower():
                cnr_min.append(col)
            if "dopp spect broad" in col.lower():
                dopp_spect.append(col)
            if "data availability (%)" in col.lower():
                data_availability.append(col)

            if "ext temp (°c)" in col.lower():
                col_renamed = "T_1_mean"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                temp.append(col_renamed)
            if "rel humidity (%)" in col.lower():
                col_renamed = "RH_1_mean"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                rh.append(col_renamed)
            if "pressure" in col.lower():
                col_renamed = "P_1_mean"
                measurement_data = measurement_data.rename(columns={col: col_renamed})
                pressure.append(col_renamed)

            if "wiper count" in col.lower():
                wiper_count.append(col)
            if "vbatt (v)" in col.lower():
                battery.append(col)
            if "int temp (°c)" in col.lower():
                int_temp.append(col)

        associated_cols = (
            ws + ws_dispersion + ws_min + ws_max + vws + vws_dispersion + wd
        )
        ambient_cols = temp + rh + pressure
        flag_cols = {f"{col}_flag": "" for col in associated_cols + ambient_cols}
        flag_cols_df = pd.DataFrame(flag_cols, index=measurement_data.index)

        # Concatenate the original DataFrame with the new columns DataFrame
        measurement_data = pd.concat([measurement_data, flag_cols_df], axis=1)

        # To get a de-fragmented frame, use copy
        measurement_data = measurement_data.copy()
        measurement_data.sort_index(axis=1, inplace=True)
        measurement_data.rename_axis("Date/Time", inplace=True)

        return measurement_data, flag_cols
