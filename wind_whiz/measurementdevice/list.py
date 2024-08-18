from datetime import datetime
import reflex as rx


from .. import navigation

from . import state
from .forms import measurementdevice_add_form
from ..models import MeasurementDeviceModel
from ..organisation.forms import organisation_edit_form
from ..ui.base import base_page
from .state import MeasurementDeviceState
from ..utils import logger

logger = logger.get_logger()


def measurementdevice_detail_link(
    child: rx.Component, measurementdevice: MeasurementDeviceModel
):
    if measurementdevice is None:
        return rx.fragment(child)
    measurementdevice_id = measurementdevice.id
    if measurementdevice_id is None:
        return rx.fragment(child)
    # root_path = navigation.routes.MEASUREMENTDEVICE_ROUTE
    root_path = navigation.routes.MEASUREMENTDEVICE_ROUTE
    measurementdevice_detail_url = f"{root_path}/{measurementdevice_id}"
    return rx.link(child, href=measurementdevice_detail_url)


# def measurementdevice_list_item(measurementdevice : MeasurementDeviceModel):
#     return rx.box(
#         measurementdevice_detail_link(
#             rx.heading(measurementdevice.measurementdevice_name),
#             measurementdevice
#             ),


#         padding = '1em'
#     )


def measurementdevice_list_item(measurementdevice: MeasurementDeviceModel):
    return rx.card(
        rx.hstack(
            rx.vstack(
                measurementdevice_detail_link(
                    rx.heading(measurementdevice.measurementdevice_name),
                    measurementdevice,
                ),
                align="center",
                justify="center",
                height="100%",
            ),
            # rx.hstack(
            #     rx.text("Analysis"),
            #     rx.text("In Progress"),
            #     rx.text("Published"),
            #     rx.text("Masts"),
            #     rx.text("LiDARs"),
            #     rx.text("SoDARs"),
            #     rx.text("Virtual"),
            #     width="75%",
            #     justify="space-between",
            # ),
            width="100%",
            align_items="flex-start",
        ),
        rx.vstack(
            rx.text(
                "Created on : ",
                rx.moment(measurementdevice.created_at, format="MMMM YYYY DD HH:mm"),
                # font_size="sm",
                # mt="2",
                text_align="right",
            ),
            rx.text(
                "Updated on : ",
                rx.moment(measurementdevice.updated_at, format="MMMM YYYY DD HH:mm"),
                font_size="sm",
                text_align="right",
            ),
            align="right",
        ),
        border="0.01px solid",
        border_color="gray.100",
        border_radius="large",
        p="4",
        mb="4",
        width="100%",
        style={
            "_hover": {
                "transform": "scale(1.02)",
                "box_shadow": "lg",
                "transition": "all 0.2s ease-in-out",
            }
        },
        padding="4",
    )


def measurementdevice_list_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.box(
                rx.vstack(
                    rx.flex(
                        rx.spacer(),
                        rx.popover.root(
                            rx.popover.trigger(
                                rx.button("Add Measurement Device"),
                            ),
                            rx.popover.content(
                                measurementdevice_add_form(),
                                side="left",
                                width="130%",
                            ),
                        ),
                        width="100%",
                        justify="end",
                    ),
                    rx.flex(
                        rx.spacer(),
                        rx.popover.root(
                            rx.popover.trigger(
                                rx.button(rx.icon(tag="bolt")),
                            ),
                            rx.popover.content(
                                organisation_edit_form(),
                                side="bottom",
                                width="100%",
                            ),
                        ),
                        width="100%",
                        justify="end",
                    ),
                    width="100%",
                    padding="4",
                )
            ),
            rx.vstack(
                rx.foreach(
                    MeasurementDeviceState.measurementdevices,
                    measurementdevice_list_item,
                ),
                width="90%",
                padding="10",
                spacing="4",
                align="center",
            ),
            width="100%",
            spacing="4",
            align_items="stretch",
        )
    )
