import reflex as rx


from ..auth.state import SessionState
from ..ui.base import base_page
from .. import navigation
from . import form, state
from ..models import ContactEntryModel


def contact_entry_list_item(contact: ContactEntryModel):
    return rx.box(
        rx.hstack(
            rx.heading(contact.name),
            rx.divider(orientation="vertical", size="4"),
            rx.text(contact.contact_type),
        ),
        rx.text(contact.message),
        padding="1em",
    )


def contact_entries_list_page() -> rx.Component:

    return base_page(
        rx.vstack(
            rx.heading("Contact Entries", size="5"),
            rx.foreach(state.ContactState.entries, contact_entry_list_item),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    )


def contact_page() -> rx.Component:

    my_child = rx.vstack(
        rx.heading("Contact Us", size="9"),
        rx.cond(state.ContactState.did_submit, state.ContactState.thank_you, ""),
        rx.desktop_only(rx.box(form.contact_page_form(), width="30vw")),
        rx.mobile_and_tablet(rx.box(form.contact_page_form(), width="50vw")),
        spacing="5",
        justify="center",
        align="center",
        text_align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(my_child)
