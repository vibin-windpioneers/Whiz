import os
import plotly.graph_objects as go
import plotly
import pandas as pd
import reflex as rx

from .state import MeasurementDeviceAddFormState, MeasurementDeviceEditFormState
from .state_data_alteration import MeasurementDeviceDataAlterationState
from ..windchest.io import InputOutput
from ..windchest.categorisation import GeneralCatergorisation
from ..utils import logger


logger = logger.get_logger()


inputoutput = InputOutput()
generalcategorisation = GeneralCatergorisation()


def measurementdevice_add_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                name="measurementdevice_name",
                placeholder="Measurement Device Name",
                required=True,
                type="text",
                width="100%",
            ),
            rx.input(
                name="rawdata_location",
                placeholder="Raw data location",
                required=True,
                type="text",
                width="100%",
            ),
            rx.input(
                name="measurementdevice_description",
                placeholder="Measurement Device Description",
                required=True,
                width="100%",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=MeasurementDeviceAddFormState.handle_submit,
        reset_on_submit=True,
    )


def measurementdevice_edit_form() -> rx.Component:
    measurementdevice = MeasurementDeviceEditFormState.measurementdevice
    measurementdevice_name = measurementdevice.measurementdevice_name
    rawdata_location = measurementdevice.rawdata_location
    measurementdevice_description = measurementdevice.measurementdevice_description
    return rx.form(
        rx.box(
            rx.input(
                type="hidden", name="measurementdevice_id", value=measurementdevice.id
            ),
            display="none",
        ),
        rx.vstack(
            rx.input(
                default_value=measurementdevice_name,
                name="measurementdevice_name",
                placeholder="measurementdevice Name",
                required=True,
                type="text",
                width="100%",
            ),
            rx.input(
                default_value=rawdata_location,
                on_change=MeasurementDeviceEditFormState.set_rawdata_location,
                name="rawdata_location",
                placeholder="Measurement Device Location",
                required=True,
                width="100%",
            ),
            rx.input(
                default_value=measurementdevice_description,
                on_change=MeasurementDeviceEditFormState.set_measurementdevice_description,
                name="measurementdevice_description",
                placeholder="Measurement Device Description",
                required=True,
                width="100%",
            ),
            rx.flex(
                rx.switch(
                    default_checked=MeasurementDeviceEditFormState.is_measurementdevice_active,
                    on_change=MeasurementDeviceEditFormState.set_is_measurementdevice_active,
                    name="measurementdevice_active",
                    color_scheme="green",
                    variant="soft",
                    high_contrast=False,
                ),
                rx.cond(
                    MeasurementDeviceEditFormState.is_measurementdevice_active,
                    rx.text("Active"),
                    rx.text("Archived"),
                ),
                spacing="2",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=MeasurementDeviceEditFormState.handle_submit,
    )


def measurementdevice_dataqualityedit_form() -> rx.Component:
    measurementdevice = MeasurementDeviceEditFormState.measurementdevice
    dataquality_filter = measurementdevice.dataquality_filter
    measurementdevice_name = measurementdevice.measurementdevice_name
    return rx.form(
        rx.box(
            rx.input(
                type="hidden", name="measurementdevice_id", value=measurementdevice.id
            ),
            display="none",
        ),
        rx.vstack(
            rx.input(
                default_value=dataquality_filter.to_string(),
                type="number",
                name="dataquality_filter",
                placeholder="New Data Quality Filter",
                required=True,
                width="100%",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=MeasurementDeviceDataAlterationState.handle_dataqualitysubmit,
    )
