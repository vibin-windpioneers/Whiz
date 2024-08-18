import reflex as rx
from ..ui.base import base_page


# About page (Index)
def pricing_page() -> rx.Component:

    my_child = rx.vstack(
        # rx.heading("About Us", size="9"),
        rx.text(
            "Its absolutely free!",
            size="5",
        ),
        rx.link(
            rx.button("Check out our webpage"),
            href="https://www.wind-pioneers.com/",
            is_external=True,
        ),
        spacing="5",
        justify="center",
        align="center",
        text_align="center",
        min_height="85vh",
        id="my-child",
    )
    return base_page(my_child)
