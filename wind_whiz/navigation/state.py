import reflex as rx
import reflex_local_auth


from . import routes


class NavState(rx.State):

    def to_home(self):
        return rx.redirect(routes.HOME_ROUTE)

    def to_login(self):
        return rx.redirect(reflex_local_auth.routes.LOGIN_ROUTE)

    def to_logout(self):
        return rx.redirect(routes.LOGOUT_ROUTE)

    def to_signup(self):
        return rx.redirect(reflex_local_auth.routes.REGISTER_ROUTE)

    def to_about_us(self):
        return rx.redirect(routes.ABOUT_US_ROUTE)

    def to_contact_us(self):
        return rx.redirect(routes.CONTACT_US_ROUTE)

    def to_organisation(self):
        return rx.redirect(routes.ORGANISATION_ROUTE)

    def to_organisation_add(self):
        return rx.redirect(routes.ORGANISATION_ADD_ROUTE)

    def to_organisation_create(self):
        return self.to_organisation_add

    def to_pricing(self):
        return rx.redirect(routes.PRICING_ROUTE)
