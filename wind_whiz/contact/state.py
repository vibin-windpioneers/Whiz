import reflex as rx
import asyncio
from sqlmodel import select
from typing import List

from ..auth.state import SessionState
from ..models import ContactEntryModel


class ContactState(SessionState):
    form_data: dict = {}
    entries: List["ContactEntryModel"] = []
    did_submit: bool = False
    timeleft: int = 5

    @rx.var
    def timeleft_label(self):
        return

    @rx.var
    def thank_you(self):
        name = self.form_data.get("name") or ""
        return f"Thank you {name}".strip() + " !"

    async def handle_submit(self, form_data: dict):
        """Handle the form submit."""

        self.form_data = form_data
        data = {}
        for k, v in form_data.items():
            if v == "" or v is None:
                continue
            data[k] = v
        if self.my_user_id is not None:
            data["user_id"] = self.my_user_id
        print("contact_data", data)
        with rx.session() as session:
            db_entry = ContactEntryModel(**data)
            session.add(db_entry)
            session.commit()
            self.did_submit = True
            yield

        await asyncio.sleep(2)
        self.did_submit = False
        yield

    def list_entries(self):
        with rx.session() as session:
            entries = session.exec(select(ContactEntryModel)).all()
            print(entries)
            self.entries = entries
