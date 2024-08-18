import reflex as rx
from typing import Optional, List
from datetime import datetime, timezone
import sqlalchemy
from sqlmodel import Field, Relationship
from reflex_local_auth.user import LocalUser

from . import utils


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UserInfo(rx.Model, table=True):
    email: str
    user_id: int = Field(foreign_key="localuser.id")
    user: LocalUser | None = Relationship()  # Local user instance
    organisations: List["OrganisationModel"] = Relationship(back_populates="userinfo")
    contact_entries: List["ContactEntryModel"] = Relationship(back_populates="userinfo")
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )


class OrganisationModel(rx.Model, table=True):
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional["UserInfo"] = Relationship(back_populates="organisations")
    measurementdevices: List["MeasurementDeviceModel"] = Relationship(
        back_populates="organisation_info"
    )
    organisation_name: str | None = None
    organisation_description: str | None = None
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )

    organisation_active: bool = True


class ContactEntryModel(rx.Model, table=True):
    user_id: int | None = None
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional["UserInfo"] = Relationship(back_populates="contact_entries")
    name: str | None = None
    email: str | None = None
    message: str | None = None
    contact_type: str | None = None
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )


class MeasurementDeviceModel(rx.Model, table=True):
    organisationinfo_id: int = Field(foreign_key="organisationmodel.id")
    organisation_info: Optional["OrganisationModel"] = Relationship(
        back_populates="measurementdevices"
    )
    measurementdevice_name: str | None = None
    measurementdevice_type: str | None = None
    rawdata_location: str | None = None
    measurementdevice_description: str | None = None
    dataquality_filter: int = 80
    cleaned_filepath: str = "cleaned_timeseries.csv"
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )

    measurementdevice_active: bool = True
