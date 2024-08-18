import numpy as np
import pandas as pd

from ..categorisation import GeneralCatergorisation
from ..processes import Processes
from .vena_lt_prework import VenaLT_Prework


class Method2(GeneralCatergorisation, Processes, VenaLT_Prework):

    def vena_method2(
        self,
        mast_timeseries,
        lidar_with_offset_applied,
        heights_tobe_sheared,
        num_of_nearest_channels,
    ):

        mast_heights = self.measurement_height(mast_timeseries)

        mast_timeseries["month_hour"] = mast_timeseries.index.to_series().apply(
            lambda x: f'{x.strftime("%B")}_{x.hour+1}'
        )
        lidar_with_offset_applied[
            "month_hour"
        ] = lidar_with_offset_applied.index.to_series().apply(
            lambda x: f'{x.strftime("%B")}_{x.hour+1}'
        )
        for sheared_height in heights_tobe_sheared:
            if sheared_height not in mast_heights:
                req_cols = self.required_cols(
                    lidar_with_offset_applied, sheared_height, num_of_nearest_channels
                )
                lidar_timeseries_withrequired_heights = pd.concat(
                    [
                        lidar_with_offset_applied[req_cols],
                        lidar_with_offset_applied["month_hour"],
                    ],
                    axis=1,
                )
                lidar_month_hour_windspeed = (
                    lidar_timeseries_withrequired_heights.groupby(["month_hour"]).mean()
                )
                lidar_month_hour_windspeed_log = lidar_month_hour_windspeed.apply(
                    np.log
                )

                req_heights = self.measurement_height(
                    lidar_timeseries_withrequired_heights
                )
                req_heights_log = np.log(req_heights)

                slopes = []
                for index, row in lidar_month_hour_windspeed_log.iterrows():
                    slope, intercept, r_value, p_value, std_err = linregress(
                        req_heights_log, row
                    )
                    slopes.append(slope)
                lidar_month_hour_windspeed_log["power_law_exponent"] = slopes

                mast_timeseries_with_powerlawexponent = pd.merge(
                    mast_timeseries,
                    lidar_month_hour_windspeed_log["power_law_exponent"],
                    left_on="month_hour",
                    right_on="month_hour",
                )

                mast_timeseries_with_powerlawexponent.index = mast_timeseries.index

                nearest_height = self.find_nearest_height(mast_heights, sheared_height)
                mast_timeseries[
                    f"WS_{sheared_height}_mean"
                ] = mast_timeseries_with_powerlawexponent[
                    f"WS_{nearest_height}_mean"
                ] * (
                    (sheared_height / nearest_height)
                    ** mast_timeseries_with_powerlawexponent["power_law_exponent"]
                )
                mast_timeseries_with_powerlawexponent.drop(
                    columns=["power_law_exponent"], inplace=True
                )
                mast_heights.append(sheared_height)

        ws_cols = self.get_windspeed_cols(mast_timeseries)

        mast_timeseries = mast_timeseries[ws_cols].copy()
        momm = self.momm(mast_timeseries)
        return momm
