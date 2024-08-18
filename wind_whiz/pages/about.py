import reflex as rx
from ..ui.base import base_page


# About page (Index)


# @rx.page(route='/about-us')
def about_page() -> rx.Component:

    my_child = rx.vstack(
        rx.heading("About Us", size="9"),
        rx.text(
            "Our Story from the founder",
            size="5",
        ),
        rx.link(
            rx.button("Read it"),
            href="https://www.wind-pioneers.com/our-story/",
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
