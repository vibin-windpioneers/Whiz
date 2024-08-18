import numpy as np
import pandas as pd

from .adhoc_processes import AdHoc_Processes


class Processes(AdHoc_Processes):

    def momm(self, timeseries, averaging_period="ME", nodata_value=9999):
        # Timeseries has to have a DateTimeIndex
        # Calculates the MOMM for the timeseries and exports as a dictionary

        timeseries[timeseries == nodata_value] = np.nan
        if averaging_period != "ME":
            print(
                "Only mean of monthly means available , please use means_of_averagingpeiod of any other averaging period"
            )
        time_interval_minutes = self.get_time_interval(timeseries)
        timeseries_columns = timeseries.columns
        mean_of_means_dict = {}
        timeseries["daysinmonth"] = timeseries.index.days_in_month
        timeseries["period"] = timeseries.index.month
        monthsize_without_completeness_factor = timeseries.groupby("period").agg(
            **{"monthsize": ("daysinmonth", "mean")}
        )
        for col in timeseries_columns:
            mean_of_means_individual_cols = timeseries.groupby("period").agg(
                **{f"{col}_VDP": (col, "count"), f"{col}": (col, "mean")}
            )
            mean_of_means_individual_cols[f"{col}_completeness_factor"] = (
                (
                    mean_of_means_individual_cols[f"{col}_VDP"]
                    * (time_interval_minutes / (60 * 24))
                )
                / monthsize_without_completeness_factor["monthsize"]
            ).clip(upper=1)
            mean_of_means_individual_cols[
                f"{col}_monthsize_with_completeness_factor"
            ] = (
                mean_of_means_individual_cols[f"{col}_completeness_factor"]
                * monthsize_without_completeness_factor["monthsize"]
            )

            mean_of_means_individual_cols[f"{col}*monthsize_with_cf"] = (
                mean_of_means_individual_cols[
                    f"{col}_monthsize_with_completeness_factor"
                ]
                * mean_of_means_individual_cols[col]
            )

            mean_of_means_individual_cols = mean_of_means_individual_cols[
                [
                    f"{col}*monthsize_with_cf",
                    f"{col}_monthsize_with_completeness_factor",
                ]
            ].sum()
            momm = (
                mean_of_means_individual_cols[f"{col}*monthsize_with_cf"]
                / mean_of_means_individual_cols[
                    f"{col}_monthsize_with_completeness_factor"
                ]
            )
            mean_of_means_dict[col] = momm
        return mean_of_means_dict

    def month_hour_shear(
        self, timeseries, heights_tobe_sheared, num_of_nearest_channels
    ):
        timeseries_cols = list(timeseries.columns)
        lidar_heights = self.measurement_height(timeseries)
        sheared_heights_timeseries = pd.DataFrame()
        timeseries["month_hour"] = timeseries.index.to_series().apply(
            lambda x: f'{x.strftime("%B")}_{x.hour+1}'
        )
        for sheared_height in heights_tobe_sheared:
            if sheared_height not in lidar_heights:
                req_cols = self.required_cols(
                    timeseries, sheared_height, num_of_nearest_channels
                )

                timeseries_withrequired_heights = pd.concat(
                    [timeseries[req_cols], timeseries["month_hour"]], axis=1
                )

                month_hour_windspeed = timeseries_withrequired_heights.groupby(
                    ["month_hour"]
                ).mean()
                month_hour_windspeed_log = month_hour_windspeed.apply(np.log)

                req_heights = self.measurement_height(timeseries_withrequired_heights)
                req_heights_log = np.log(req_heights)

                slopes = []

                for index, row in month_hour_windspeed_log.iterrows():
                    slope, intercept, r_value, p_value, std_err = linregress(
                        req_heights_log, row
                    )
                    slopes.append(slope)
                month_hour_windspeed_log["power_law_exponent"] = slopes

                timeseries_with_powerlawexponent = pd.merge(
                    timeseries_withrequired_heights,
                    month_hour_windspeed_log["power_law_exponent"],
                    left_on="month_hour",
                    right_on="month_hour",
                )
                timeseries_with_powerlawexponent.index = (
                    timeseries_withrequired_heights.index
                )
                nearest_height = self.find_nearest_height(req_heights, sheared_height)
                sheared_heights_timeseries[
                    f"WS_{sheared_height}_mean"
                ] = timeseries_with_powerlawexponent[f"WS_{nearest_height}_mean"] * (
                    (sheared_height / nearest_height)
                    ** timeseries_with_powerlawexponent["power_law_exponent"]
                )
                timeseries_with_powerlawexponent.drop(
                    columns=["power_law_exponent"], inplace=True
                )

        timeseries = pd.concat(
            [timeseries[timeseries_cols], sheared_heights_timeseries], axis=1
        )

        return timeseries

    def means_of_averagingperiod(self, timeseries, averaging_period):
        # Timeseries has to have a DateTimeIndex
        timeseries_columns = timeseries.columns
        if averaging_period == "ME":
            timeseries_resampled_mean = timeseries.resample(averaging_period).mean()
            timeseries_resampled_mean["period"] = timeseries_resampled_mean.index.month
            timeseries_resampled_mean_of_means = timeseries_resampled_mean.groupby(
                "period"
            ).mean()

        else:
            averaging_period_integer = int(re.findall("\d+", averaging_period)[0])
            timeseries_resampled_mean = timeseries.resample(averaging_period).mean()
            timeseries_resampled_mean["day_of_year"] = (
                timeseries_resampled_mean.index.dayofyear
            )
            timeseries_resampled_mean["period"] = (
                timeseries_resampled_mean["day_of_year"] - 1
            ) // averaging_period_integer
            timeseries_resampled_mean_of_means = timeseries_resampled_mean.groupby(
                "period"
            ).mean()

        return timeseries_resampled_mean_of_means[timeseries_columns]

    def month_hour(self, timeseries):

        timeseries["month"] = timeseries.index.month
        timeseries["hour"] = timeseries.index.hour + 1
        month_hour_matrix = timeseries.groupby(["hour", "month"]).mean()
        return month_hour_matrix
