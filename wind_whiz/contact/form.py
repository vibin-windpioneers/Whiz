import reflex as rx

from ..auth.state import SessionState
from .state import ContactState
from ..organisation.forms import organisation_dropdown


def contact_page_form() -> rx.Component:
    user_info_obj = SessionState.authenticated_user_info
    authenticated_username = SessionState.authenticated_username
    return rx.cond(
        SessionState.my_user_id,
        rx.form(
            rx.vstack(
                rx.input(
                    default_value=f"{authenticated_username}",
                    name="name",
                    type="text",
                    required=True,
                    width="100%",
                    read_only=True,
                ),
                rx.input(
                    default_value=f"{user_info_obj.email}",
                    name="email",
                    type="email",
                    required=True,
                    width="100%",
                    read_only=True,
                ),
                contact_dropdown(),
                rx.text_area(
                    name="message",
                    placeholder="Your Message",
                    required=True,
                    width="100%",
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ContactState.handle_submit,
            reset_on_submit=True,
        ),
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder=f"Name",
                    name="name",
                    type="text",
                    required=True,
                    width="100%",
                ),
                rx.input(
                    placeholder=f"Email",
                    name="email",
                    type="email",
                    required=True,
                    width="100%",
                ),
                contact_dropdown(),
                rx.text_area(
                    name="message",
                    placeholder="Your Message",
                    required=True,
                    width="100%",
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ContactState.handle_submit,
            reset_on_submit=True,
        ),
    )


def contact_dropdown():
    return rx.select.root(
        rx.select.trigger(placeholder="Select a case type"),
        rx.select.content(
            rx.select.group(
                rx.select.label("Case Type"),
                rx.select.item("Feature Request", value="Feature Request"),
                rx.select.item("Report a bug", value="Report a bug"),
            ),
            rx.select.separator(),
            rx.select.group(
                rx.select.item("Help", value="Help"),
            ),
        ),
        name="contact_type",
    )
