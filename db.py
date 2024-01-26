from json import dumps

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from config import app


class Base(DeclarativeBase):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return dumps(self.as_dict(), default=str)


class BaseMixin(object):
    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
        return obj


db = SQLAlchemy(model_class=Base)
db.init_app(app)

with app.app_context():
    db.reflect()


class Player(BaseMixin, db.Model):
    __table__ = db.metadata.tables["Player"]

    @classmethod
    def exists(self, username: str):
        player = db.session.scalars(
            db.select(self).filter_by(username=username)
        ).first()
        return player.id if player else None


class SessionStats(BaseMixin, db.Model):
    __table__ = db.metadata.tables["SessionStats"]


class Session(BaseMixin, db.Model):
    __table__ = db.metadata.tables["Session"]

    @classmethod
    def get_player_stats(self, player_id: int):
        player_sessions = db.select(Session).filter_by(player_id=player_id).subquery()
        session_stats = db.session.execute(
            db.select(player_sessions, SessionStats)
            .join(SessionStats)
            .order_by(-SessionStats.session_end)
        ).all()
        return list(map(lambda stats: f"{stats[2]}", session_stats))
