import reflex as rx


from .forms import measurementdevice_edit_form, measurementdevice_dataqualityedit_form
from ..ui.base import base_page
from . import state
from .state_data_alteration import (
    MeasurementDeviceDataAlterationState,
    MeasurementDevicePlottingState,
)
from ..navigation import routes
from ..windchest.plots import timeseries_plot


# About page (Index)
def measurementdevice_detail_page() -> rx.Component:
    # actual_value = state.MeasurementDeviceState.measurementdevice.get_cleaned_file
    # print(
    #      actual_value
    # )
    my_child = rx.fragment(
        rx.box(
            rx.hstack(
                rx.heading(
                    state.MeasurementDeviceState.measurementdevice.measurementdevice_name,
                    size="5",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(rx.icon(tag="bolt")),
                        ),
                        rx.popover.content(
                            measurementdevice_edit_form(),
                            side="bottom",
                            width="100%",
                        ),
                    ),
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button("Edit Data Quality Filter"),
                        ),
                        rx.popover.content(
                            measurementdevice_dataqualityedit_form(),
                            side="bottom",
                            width="100%",
                        ),
                        rx.button(
                            "Update with New data",
                            on_click=MeasurementDeviceDataAlterationState.handle_appenddata,
                        ),
                    ),
                    align_items="flex-end",
                ),
                width="100%",
                justify="space-between",
                align_items="center",
            ),
            padding="4",
            width="100%",
        ),
        rx.cond(
            MeasurementDevicePlottingState.timeseries_fig,
            rx.box(
                rx.plotly(
                    data=MeasurementDevicePlottingState.timeseries_fig,
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
            ),
            rx.text("timesereis_fig is none"),
        ),
        width="100%",
        align="stretch",
        spacing="2",
    )

    return base_page(my_child)
