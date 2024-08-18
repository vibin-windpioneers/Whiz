import datashader as ds
import os
import pandas as pd
import plotly.graph_objects as go
import plotly
import reflex as rx

from ..categorisation import GeneralCatergorisation
from ..io import InputOutput

from ...utils import logger


logger = logger.get_logger()

inputoutput = InputOutput()
generalcategorisation = GeneralCatergorisation()


def timeseries_plot(rawdata_folder):
    logger.info("Running timeseries plot function")
    cleaneddata_path = os.path.join(rawdata_folder, "cleaned_timeseries.csv")
    if os.path.exists(cleaneddata_path):
        logger.debug("Timeseries for plotting exist")
        timeseries = inputoutput.skip_to(cleaneddata_path, "Date/Time")
        logger.debug("Data Read for plotting")
        timeseries.set_index("Date/Time", inplace=True)
        timeseries.index = pd.to_datetime(timeseries.index)
        req_cols = generalcategorisation.get_windspeed_cols(timeseries)
        logger.debug("Retrieved WS cols, Plotting them")
        color_palette = plotly.colors.qualitative.Set1
        fig = go.Figure()
        # cvs = ds.Canvas(plot_width=100, plot_height=100)
        for i, col in enumerate(req_cols):
            # Determine the color for the trace from the palette
            line_color = color_palette[i % len(color_palette)]
            # agg  = cvs.line(timeseries, timeseries.index, timeseries[col])
            # line_img =
            fig.add_trace(
                go.Scattergl(
                    x=timeseries.index,
                    y=timeseries[col],
                    mode="lines",
                    name=col,
                    line=dict(
                        color=line_color,
                    ),
                )
            )

            # Filter the data to include only rows where col_flag is "L"
            flag_values = timeseries[timeseries[col + "_flag"] == "L"]
            # Add a trace for the flagged values with markers matching the line color
            fig.add_trace(
                go.Scattergl(
                    x=flag_values.index,
                    y=flag_values[col],
                    mode="markers",
                    marker=dict(color=line_color),  # Use the same color as the line
                    showlegend=False,
                )
            )
        fig.update_layout(
            xaxis_title="Date/Time",
            yaxis_title="Wind Speed (m/s)",
        )
        fig.update_layout(dragmode="pan", autosize=True)
        fig.update_yaxes(fixedrange=True, automargin=True)
        fig.update_xaxes(
            range=[timeseries.index[0], timeseries.index[-1]], automargin=True
        )
        logger.debug("Returning rx.plolty component")
        # fig.show(config={'scrollZoom': True,'modeBarButtonsToRemove': ['toImage','zoom2d','zoomIn2d','select2d', 'lasso2d','zoomOut2d','pan2d','autoScale2d'],'showLink': False,'displaylogo': False})
        return rx.plotly(
            data=fig,
            config={
                "autosizable": True,
                "responsive": True,
                "scrollZoom": True,
                "modeBarButtonsToRemove": [
                    "toImage",
                    "zoomIn2d",
                    "select2d",
                    "lasso2d",
                    "zoomOut2d",
                    "autoScale2d",
                ],
                "showLink": False,
                "displaylogo": False,
            },
            use_resize_handler=True,
            style={"width": "100%", "height": "100%"},
        )

    else:
        logger.debug("Timeseries for plotting does not exist")
        return rx.fragment("")
