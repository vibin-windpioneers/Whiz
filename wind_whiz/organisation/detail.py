import reflex as rx


from ..navigation import routes
from ..measurementdevice import MeasurementDeviceState, measurementdevice_list_page


def organisation_detail_page() -> rx.Component:
    return measurementdevice_list_page()
