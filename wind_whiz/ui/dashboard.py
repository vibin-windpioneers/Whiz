import reflex as rx

from .sidebar import sidebar


def base_dasboard_page(
    child: rx.Component, hide_navbar=False, *args, **kwargs
) -> rx.Component:
    print([type(x for x in args)])

    return rx.fragment(
        rx.hstack(
            sidebar(),
            rx.box(
                child,
                padding="1em",
                width="100%",
                max_width="100%",
                id="base-child-element",
            ),
        ),
        rx.color_mode.button(position="bottom-right"),
    )
