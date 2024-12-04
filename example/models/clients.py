import typing as t
from datetime import datetime

from sqlalchemy import select

from example.extensions import db


class Clients(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    @classmethod
    def create(cls, name: str, **_) -> t.Tuple[bool, str, t.Any]:
        client = cls(name=name)

        db.session.add(client)
        db.session.commit()

        return True, "OK", client

    @classmethod
    def read(cls, client_id: int, **_) -> t.Tuple[bool, str, t.Any]:
        q = select(cls).where(cls.client_id == client_id)
        r = db.session.execute(q).scalar_one_or_none()

        if not r:
            return False, "Client not found.", None

        return True, "OK", r

    @classmethod
    def update(cls, client_id: int, name: str, **_) -> t.Tuple[bool, str, t.Any]:
        q = select(cls).where(cls.client_id == client_id)
        r = db.session.execute(q).scalar_one_or_none()

        if not r:
            return False, "Client not found.", None

        r.name = name
        db.session.commit()

        return True, "OK", r

    @classmethod
    def delete(cls, client_id: int, **_) -> t.Tuple[bool, str, t.Any]:
        q = select(cls).where(cls.client_id == client_id)
        r = db.session.execute(q).scalar_one_or_none()

        if not r:
            return False, "Client not found.", None

        db.session.delete(r)
        db.session.commit()

        return True, "OK", r
