import reflex as rx
from typing import Optional, List
import sqlalchemy.orm
from sqlmodel import select
import sqlalchemy

from .. import navigation
from ..auth.state import SessionState
from ..models import OrganisationModel, UserInfo
from ..utils import logger


logger = logger.get_logger()
logger.debug("logger is running")

ORGANISATION_ROUTE = navigation.routes.ORGANISATION_ROUTE
if ORGANISATION_ROUTE.endswith("/"):
    ORGANISATION_ROUTE = ORGANISATION_ROUTE[:-1]


class OrganisationState(SessionState):
    organisations: List["OrganisationModel"] = []
    organisation: Optional["OrganisationModel"] = None
    organisation_description: str = ""
    is_organisation_active: bool = True

    @rx.var
    def organisation_id(self):
        return self.router.page.params.get("organisation_id", "")

    @rx.var
    def organisation_url(self):
        if not self.organisation:
            return f"{ORGANISATION_ROUTE}"
        return f"{ORGANISATION_ROUTE}/{self.organisation.id}"

    @rx.var
    def organisation_edit_url(self):
        if not self.organisation:
            return f"{ORGANISATION_ROUTE}"
        return f"{ORGANISATION_ROUTE}/{self.organisation.id}/edit"

    def load_organisations(self):

        with rx.session() as session:
            result = session.exec(
                select(OrganisationModel)
                .options(sqlalchemy.orm.joinedload(OrganisationModel.userinfo))
                .where(OrganisationModel.userinfo_id == self.my_userinfo_id)
            ).all()
            self.organisations = result

    # def load_my_organisations(self):
    #     with rx.session() as session:
    #         result = session.exec(
    #             select(OrganisationModel)
    #         ).all()
    #         self.organisations = result

    def get_organisation_detail(self):
        with rx.session() as session:
            if self.organisation_id == "":
                self.organisation = None
                return
            sql_statement = (
                select(OrganisationModel)
                .options(
                    sqlalchemy.orm.joinedload(OrganisationModel.userinfo).joinedload(
                        UserInfo.user
                    )
                )
                .where(OrganisationModel.id == self.organisation_id)
            )
            result = session.exec(sql_statement).one_or_none()
            result.userinfo
            self.organisation = result
            if result is None:
                self.organisation_description = ""
                return
            self.organisation_description = self.organisation.organisation_description
            self.is_organisation_active = self.organisation.organisation_active

    def add_organisation(self, form_data: dict):
        with rx.session() as session:
            organisation = OrganisationModel(**form_data)
            session.add(organisation)
            session.commit()
            session.refresh(organisation)  # post.id
            self.organisation = organisation

    def save_organisation_edits(self, organisation_id: int, updated_data: dict):
        with rx.session() as session:
            organisation = session.exec(
                select(OrganisationModel).where(
                    OrganisationModel.id == self.organisation_id
                )
            ).one_or_none()
            if organisation is None:
                return
            for key, value in updated_data.items():
                setattr(organisation, key, value)
            session.add(organisation)
            session.commit()
            session.refresh(organisation)
            self.organisation = organisation

    def to_organisation(self, edit_page=False):
        if not self.organisation:
            return rx.redirect(ORGANISATION_ROUTE)
        if edit_page:
            return rx.redirect(f"{self.organisation_edit_url}")
        return rx.redirect(f"{self.organisation_url}")


class OrganisationAddFormState(OrganisationState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        data = form_data.copy()
        if self.my_userinfo_id is not None:
            data["userinfo_id"] = self.my_userinfo_id
        self.form_data = data
        self.add_organisation(data)
        return self.to_organisation()


class OrganisationEditFormState(OrganisationState):
    form_data: dict = {}

    def handle_submit(self, form_data):

        self.form_data = form_data
        organisation_id = form_data.pop("organisation_id")
        organisation_active = True
        if (
            "organisation_active" in form_data
            and form_data["organisation_active"] == "on"
        ):
            organisation_active = True
        else:
            organisation_active = False
        updated_data = {**form_data}
        updated_data["organisation_active"] = organisation_active
        print(updated_data)
        self.save_organisation_edits(organisation_id, updated_data)
        return self.to_organisation()
