import reflex as rx
import reflex_local_auth
from rxconfig import config

from .ui.base import base_page
from . import pages
from .auth.pages import my_login_page, my_signup_page, my_logout_page
from .auth.state import SessionState
from . import auth, contact, organisation, navigation, pages, measurementdevice


class State(rx.State):
    """The app state."""

    def did_click(self):
        print("Hello world did click")
        return rx.redirect("/about-us")

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    my_user_obj = SessionState.authenticated_user_info
    my_child = rx.vstack(
        # rx.theme_panel(),
        rx.heading("Welcome to SaaS", size="9"),
        # rx.button("About Us",on_click=State.did_click),
        rx.link(
            rx.button("About Us"),
            href=navigation.routes.ABOUT_US_ROUTE,
        ),
        spacing="5",
        justify="center",
        align="center",
        text_align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(my_child)


app = rx.App(
    theme=rx.theme(
        accent_color="purple", grayColor="mauve", radius="large", scaling="90%"
    )
)
app.add_page(index)

app.add_page(
    my_login_page,
    route=reflex_local_auth.routes.LOGIN_ROUTE,
    title="Login",
)
app.add_page(
    my_logout_page,
    route=navigation.routes.LOGOUT_ROUTE,
    title="Logout",
)
app.add_page(
    my_signup_page,
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)

# my pages
app.add_page(pages.about_page, route=navigation.routes.ABOUT_US_ROUTE)
app.add_page(pages.protected_page, route="/protected", on_load=SessionState.on_load)
app.add_page(contact.contact_page, route=navigation.routes.CONTACT_US_ROUTE)
app.add_page(
    contact.contact_entries_list_page,
    route=navigation.routes.CONTACT_ENTRIES_ROUTE,
    on_load=contact.ContactState.list_entries,
)

app.add_page(
    measurementdevice.measurementdevice_detail_page,
    route=f"{navigation.routes.MEASUREMENTDEVICE_ROUTE}/[measurementdevice_id]",
    on_load=measurementdevice.MeasurementDeviceState.get_measurementdevice_detail,
)


app.add_page(
    organisation.organisation_list_page,
    route=navigation.routes.ORGANISATION_ROUTE,
    on_load=organisation.OrganisationState.load_organisations,
)

app.add_page(
    organisation.organisation_detail_page,
    route=f"{navigation.routes.ORGANISATION_ROUTE}/[organisation_id]",
    on_load=measurementdevice.MeasurementDeviceState.load_measurementdevices,
)

app.add_page(pages.pricing_page, route=navigation.routes.PRICING_ROUTE)
