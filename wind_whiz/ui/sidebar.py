import reflex as rx

from .. import navigation
from ..auth.state import SessionState


def sidebar_user_item() -> rx.Component:
    user_info_obj = SessionState.authenticated_user_info
    username_via_user_obj = rx.cond(
        SessionState.authenticated_username,
        SessionState.authenticated_username,
        "Account",
    )

    return rx.cond(
        user_info_obj,
        rx.hstack(
            rx.icon_button(
                rx.icon("user"),
                size="3",
                radius="full",
            ),
            rx.vstack(
                rx.box(
                    rx.text(
                        username_via_user_obj,
                        size="3",
                        weight="bold",
                    ),
                    rx.text(
                        f"{user_info_obj.email}",
                        size="2",
                        weight="medium",
                    ),
                    width="100%",
                ),
                spacing="0",
                align="start",
                justify="start",
                width="100%",
            ),
            padding_x="0.5rem",
            align="center",
            justify="start",
            width="100%",
        ),
        rx.fragment(""),
    )


def sidebar_logout_item() -> rx.Component:
    return (
        rx.box(
            rx.hstack(
                rx.icon("log-out"),
                rx.text("Log Out", size="4"),
                width="100%",
                padding_x="0.5rem",
                padding_y="0.75rem",
                align="center",
                style={
                    "_hover": {
                        "cursor": "pointer",  # css
                        "bg": rx.color("accent", 4),
                        "color": rx.color("accent", 11),
                    },
                    "color": rx.color("accent", 11),
                    "border-radius": "0.5em",
                },
            ),
            on_click=navigation.NavState.to_logout,
            as_="button",
            underline="none",
            weight="medium",
            width="100%",
        ),
    )


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("My Dashboard", "layout-dashboard", navigation.routes.HOME_ROUTE),
        sidebar_item(
            "Organisations", "building-2", navigation.routes.ORGANISATION_ROUTE
        ),
        # sidebar_item("Vena shear Analysis", "bar-chart-4", navigation.routes.VENA_SHEAR_ANALYSIS),
        sidebar_item("Contact Us", "mail", navigation.routes.CONTACT_US_ROUTE),
        spacing="1",
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="/WP_logo.ico",
                        width="1.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Wind Whiz", size="4", weight="bold"),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    rx.vstack(
                        # sidebar_item(
                        #     "Settings", "settings", "/#"
                        # ),
                        sidebar_logout_item(),
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(),
                    sidebar_user_item(),
                    width="100%",
                    spacing="5",
                ),
                spacing="5",
                # position="fixed",
                # left="0px",
                # top="0px",
                # z_index="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",
                # height="650px",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(rx.icon("x", size=30)),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                rx.vstack(
                                    # sidebar_item(
                                    #     "Settings",
                                    #     "settings",
                                    #     "/#",
                                    # ),
                                    sidebar_logout_item(),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.divider(margin="0"),
                                sidebar_user_item(),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )
