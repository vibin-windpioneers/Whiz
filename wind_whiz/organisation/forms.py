import reflex as rx

from .state import (
    OrganisationAddFormState,
    OrganisationEditFormState,
    OrganisationState,
)
from ..models import OrganisationModel
from ..utils import logger

logger = logger.get_logger()


def organisation_add_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="organisation_name",
                    placeholder="Organisation Name",
                    required=True,
                    type="text",
                    width="100%",
                ),
                width="100%",
            ),
            rx.input(
                name="organisation_description",
                placeholder="Organisation Description",
                required=True,
                width="100%",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=OrganisationAddFormState.handle_submit,
        reset_on_submit=True,
    )


def organisation_edit_form() -> rx.Component:
    organisation = OrganisationEditFormState.organisation
    organisation_name = organisation.organisation_name
    organisation_description = organisation.organisation_description
    # logger.debug(f"Organisation name :{organisation_name}")
    return rx.form(
        rx.box(
            rx.input(type="hidden", name="organisation_id", value=organisation.id),
            display="none",
        ),
        rx.vstack(
            rx.hstack(
                rx.input(
                    default_value=organisation_name,
                    name="organisation_name",
                    placeholder="Organisation Name",
                    required=True,
                    type="text",
                    width="100%",
                ),
                width="100%",
            ),
            rx.input(
                default_value=organisation_description,
                on_change=OrganisationEditFormState.set_organisation_description,
                name="organisation_description",
                placeholder="Organisation Description",
                required=True,
                width="100%",
            ),
            rx.flex(
                rx.switch(
                    default_checked=OrganisationEditFormState.is_organisation_active,
                    on_change=OrganisationEditFormState.set_is_organisation_active,
                    name="organisation_active",
                    color_scheme="green",
                    variant="soft",
                    high_contrast=False,
                ),
                rx.cond(
                    OrganisationEditFormState.is_organisation_active,
                    rx.text("Active"),
                    rx.text("Archived"),
                ),
                spacing="2",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=OrganisationEditFormState.handle_submit,
    )


def add_organisation_to_mydashboard_form() -> rx.Component:
    print()


def organisation_list_for_dropdown(organisation: OrganisationModel):
    return (rx.text(organisation.organisation_name),)


def organisation_dropdown():
    return rx.select.root(
        rx.select.trigger(placeholder="Select an organistion"),
        rx.select.content(
            # rx.select.group(
            #     rx.foreach(OrganisationState.organisations,
            #                lambda organisation : rx.select.item(f"{organisation}", value=organisation)),
            # ),
            rx.select.separator(),
            rx.select.group(
                rx.select.item("Help", value="Help"),
            ),
        ),
        name="contact_type",
    )
