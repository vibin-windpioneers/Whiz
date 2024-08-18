import reflex as rx
import sqlalchemy.orm
import sqlmodel
from sqlmodel import select
import sqlalchemy
from typing import Optional, List

from .. import navigation
from ..auth.state import SessionState
from ..organisation.state import OrganisationState
from ..models import MeasurementDeviceModel, OrganisationModel

from ..utils import logger

logger = logger.get_logger()

MEASUREMENTDEVICE_ROUTE = navigation.routes.MEASUREMENTDEVICE_ROUTE
if MEASUREMENTDEVICE_ROUTE.endswith("/"):
    MEASUREMENTDEVICE_ROUTE = MEASUREMENTDEVICE_ROUTE[:-1]


class MeasurementDeviceState(OrganisationState):
    measurementdevices: List["MeasurementDeviceModel"] = []
    measurementdevice: Optional["MeasurementDeviceModel"] = None
    rawdata_location: str = ""
    measurementdevice_description: str = ""
    is_measurementdevice_active: bool = True
    dataquality_filter: int = 80
    cleaned_filepath: str = "cleaned_timeseries.csv"

    @rx.var
    def rawdata_folder(self):
        if self.measurementdevice:
            return self.measurementdevice.rawdata_location.replace('"', "")
        else:
            return None

    @rx.var(cache=True)
    def current_organisation_id(self) -> str | None:
        if self.organisation is None:
            logger.info(f"Organisaiton id : None")
            return None

        logger.info(f"Organisaiton id : {self.organisation.id}")
        return self.organisation.id

    @rx.var
    def measurementdevice_id(self):
        return self.router.page.params.get("measurementdevice_id", "")

    @rx.var
    def measurementdevice_url(self):
        if not self.measurementdevice:
            return f"{MEASUREMENTDEVICE_ROUTE}"
        return f"{MEASUREMENTDEVICE_ROUTE}/{self.measurementdevice.id}"

    @rx.var
    def measurementdevice_edit_url(self):
        if not self.measurementdevice:
            return f"{MEASUREMENTDEVICE_ROUTE}"
        return f"{MEASUREMENTDEVICE_ROUTE}/{self.measurementdevice.id}/edit"

    def load_measurementdevices(self):
        self.get_organisation_detail()
        with rx.session() as session:
            result = session.exec(
                select(MeasurementDeviceModel)
                .options(
                    sqlalchemy.orm.joinedload(MeasurementDeviceModel.organisation_info)
                )
                .where(
                    MeasurementDeviceModel.organisationinfo_id
                    == self.current_organisation_id
                )
            ).all()
            # logger.info(f"Measurement devices lookup : {result}")
            self.measurementdevices = result

    def get_measurementdevice_detail(self):
        with rx.session() as session:
            if self.measurementdevice_id == "":
                self.measurementdevice = None
                return
            sql_statement = (
                select(MeasurementDeviceModel)
                .options(
                    sqlalchemy.orm.joinedload(MeasurementDeviceModel.organisation_info)
                )
                .where(MeasurementDeviceModel.id == self.measurementdevice_id)
            )
            result = session.exec(sql_statement).one_or_none()
            result.organisation_info

            self.measurementdevice = result
            if result is None:
                self.measurementdevice_description = ""
                return

    def add_measurementdevice(self, form_data: dict):
        with rx.session() as session:
            measurementdevice = MeasurementDeviceModel(**form_data)
            session.add(measurementdevice)
            session.commit()
            session.refresh(measurementdevice)  # post.id
            self.measurementdevice = measurementdevice

    def save_measurementdevice_edits(
        self, measurementdevice_id: int, updated_data: dict
    ):
        with rx.session() as session:
            measurementdevice = session.exec(
                select(MeasurementDeviceModel).where(
                    MeasurementDeviceModel.id == self.measurementdevice_id
                )
            ).one_or_none()
            if measurementdevice is None:
                return
            for key, value in updated_data.items():
                print(key, value)
                setattr(measurementdevice, key, value)
            session.add(measurementdevice)
            session.commit()
            session.refresh(measurementdevice)
            self.measurementdevice = measurementdevice

    def to_measurementdevice(self, edit_page=False):
        if not self.measurementdevice:
            return rx.redirect(MEASUREMENTDEVICE_ROUTE)
        if edit_page:
            return rx.redirect(f"{self.measurementdevice_edit_url}")
        return rx.redirect(f"{self.measurementdevice_url}")


class MeasurementDeviceAddFormState(MeasurementDeviceState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        data = form_data.copy()
        if self.current_organisation_id is not None:
            data["organisationinfo_id"] = self.current_organisation_id
        self.form_data = data
        self.add_measurementdevice(data)
        return self.to_organisation()


class MeasurementDeviceEditFormState(MeasurementDeviceState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        # logger.debug(f"Measurement Device Edit formdata : {form_data}")
        self.form_data = form_data
        measurementdevice_id = form_data.pop("measurementdevice_id")
        measurementdevice_active = True
        if (
            "measurementdevice_active" in form_data
            and form_data["measurementdevice_active"] == "on"
        ):
            measurementdevice_active = True
        else:
            measurementdevice_active = False
        updated_data = {**form_data}
        updated_data["measurementdevice_active"] = measurementdevice_active
        self.save_measurementdevice_edits(measurementdevice_id, updated_data)
        return self.to_measurementdevice()
