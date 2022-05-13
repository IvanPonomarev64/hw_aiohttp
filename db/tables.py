from sqlalchemy import func
import uuid
from aiohttp import web
from gino import Gino
from sqlalchemy.dialects.postgresql import UUID

app = web.Application()
db = Gino()


class Owner(db.Model):
    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=False)

    def to_dict(self):
        return {
            "email": self.email,
            "id": self.id,
        }


class Advertisement(db.Model):
    __tablename__ = "advertisements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    creation_time = db.Column(db.DateTime, server_default=func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"))

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "creation_time": int(self.creation_time.timestamp()),
            "owner": self.owner_id
        }


class Token(db.Model):
    __tablename__ = "tokens"

    id = db.Column(UUID, default=uuid.uuid4, primary_key=True)
    creation_time = db.Column(db.DateTime, server_default=func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"))


async def orm_context(app):
    print("start")
    await db.set_bind("postgres://ivan:12345@127.0.0.1:5432/hw_aiohttp")
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print("close")
