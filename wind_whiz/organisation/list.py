import reflex as rx


from .. import navigation

from . import state
from .forms import organisation_add_form
from ..models import OrganisationModel
from ..ui.base import base_page


def organisation_detail_link(child: rx.Component, organisation: OrganisationModel):
    if organisation is None:
        return rx.fragment(child)
    organisation_id = organisation.id
    if organisation_id is None:
        return rx.fragment(child)
    root_path = navigation.routes.ORGANISATION_ROUTE
    organisation_detail_url = f"{root_path}/{organisation_id}"
    return rx.link(child, href=organisation_detail_url)


def organisation_list_item(organisation: OrganisationModel):
    return rx.box(
        organisation_detail_link(
            rx.heading(organisation.organisation_name), organisation
        ),
        padding="1em",
    )


def organisation_list_page() -> rx.Component:

    return base_page(
        rx.fragment(
            rx.box(
                rx.flex(
                    rx.spacer(),
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button("Add Organisation"),
                        ),
                        rx.popover.content(
                            organisation_add_form(),
                            side="bottom",
                            width="100%",
                        ),
                    ),
                    width="100%",
                    justify="end",
                ),
                width="100%",
                padding="4",
            ),
            rx.vstack(
                rx.container(
                    rx.foreach(
                        state.OrganisationState.organisations, organisation_list_item
                    ),
                ),
                spacing="5",
                min_height="85vh",
            ),
        )
    )
