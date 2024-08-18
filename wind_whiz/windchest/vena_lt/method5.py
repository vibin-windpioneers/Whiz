from ..processes import Processes
from ..categorisation import GeneralCatergorisation


class Method5(Processes, GeneralCatergorisation):

    def vena_method5(
        self, lidar_with_offset_applied, heights_tobe_sheared, num_of_nearest_channels
    ):
        month_hour_sheared_timeseries = self.month_hour_shear(
            lidar_with_offset_applied, heights_tobe_sheared, num_of_nearest_channels
        )

        ws_cols = self.get_windspeed_cols(month_hour_sheared_timeseries)
        month_hour_sheared_timeseries = month_hour_sheared_timeseries[ws_cols].copy()

        momm = self.momm(month_hour_sheared_timeseries)
        return momm
