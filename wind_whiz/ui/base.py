import reflex as rx

from ..auth.state import SessionState
from .nav import navbar
from .dashboard import base_dasboard_page


def base_layout_component(child, *args, **kwargs) -> rx.fragment:
    return rx.fragment(
        navbar(),
        rx.box(child, padding="1em", width="100%", id="base-child-element"),
        rx.color_mode.button(position="bottom-right"),
    )


def base_page(child: rx.Component, hide_navbar=False, *args, **kwargs) -> rx.Component:

    is_logged_in = True

    return rx.cond(
        SessionState.is_authenticated,
        base_dasboard_page(child, *args, **kwargs),
        base_layout_component(child, *args, **kwargs),
    )
