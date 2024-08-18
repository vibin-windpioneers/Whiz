import os
import pandas as pd
import plotly.graph_objects as go
import plotly
import reflex as rx
from typing import Optional

from ..state import MeasurementDeviceState
from ...utils import logger
from ...windchest import InputOutput, GeneralCatergorisation


logger = logger.get_logger()
wc_io = InputOutput()
generalcategorisation = GeneralCatergorisation()


class MeasurementDevicePlottingState(MeasurementDeviceState):
    timeseries: Optional[pd.DataFrame] = None
    metadata_log: Optional[dict] = None
    timeseries_fig: Optional[go.Figure] = None

    @rx.var(cache=True)
    def checkif_cleanedfile_exist(self):
        if self.measurementdevice:
            self.cleaneddata_path = os.path.join(
                str(self.rawdata_folder), "cleaned_timeseries.csv"
            )

            if os.path.exists(self.cleaneddata_path):
                logger.debug("Cleaned file exist")
                self.load_cleaneddata()
                self.timeseriesplot_fig()
            else:
                logger.debug("Cleaned data not available for plotting")
        else:
            logger.debug("Measurement device state not loaded")

    def load_cleaneddata(self):

        timeseries = wc_io.skip_to(self.cleaneddata_path)
        print(timeseries)
        timeseries.set_index("Date/Time", inplace=True)
        timeseries.index = pd.to_datetime(timeseries.index)
        self.timeseries = timeseries

        logger.debug("Cleaned data fetched with skip_to() for plotting")

    def timeseriesplot_fig(self):
        if self.timeseries is not None:
            req_cols = generalcategorisation.get_windspeed_cols(self.timeseries)
            color_palette = plotly.colors.qualitative.Set1
            timeseries_fig = go.Figure()
            # cvs = ds.Canvas(plot_width=100, plot_height=100)
            for i, col in enumerate(req_cols):
                # Determine the color for the trace from the palette
                line_color = color_palette[i % len(color_palette)]
                # agg  = cvs.line(timeseries, timeseries.index, timeseries[col])
                # line_img =
                timeseries_fig.add_trace(
                    go.Scattergl(
                        x=self.timeseries.index,
                        y=self.timeseries[col],
                        mode="lines",
                        name=col,
                        line=dict(
                            color=line_color,
                        ),
                    )
                )

                # Filter the data to include only rows where col_flag is "L"
                flag_values = self.timeseries[self.timeseries[col + "_flag"] == "L"]
                # Add a trace for the flagged values with markers matching the line color
                timeseries_fig.add_trace(
                    go.Scattergl(
                        x=flag_values.index,
                        y=flag_values[col],
                        mode="markers",
                        marker=dict(color=line_color),  # Use the same color as the line
                        showlegend=False,
                    )
                )
            timeseries_fig.update_layout(
                xaxis_title="Date/Time",
                yaxis_title="Wind Speed (m/s)",
            )
            timeseries_fig.update_layout(dragmode="pan", autosize=True)
            timeseries_fig.update_yaxes(fixedrange=True, automargin=True)
            timeseries_fig.update_xaxes(
                range=[self.timeseries.index[0], self.timeseries.index[-1]],
                automargin=True,
            )
            self.timeseries_fig = timeseries_fig
            timeseries_fig.show()
            logger.debug("Fig created for plotting")

    def update_timeseries_plot(self):
        if os.path.exists(self.cleaneddata_path):
            self.load_cleaneddata()
            self.timeseriesplot_fig()
        else:
            logger.debug("Cleaned data not available for plotting")
