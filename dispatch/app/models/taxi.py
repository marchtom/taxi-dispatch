from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

from .mixins import CreatedAtMixin


class Taxi(Base, CreatedAtMixin):
    __tablename__ = "taxi"

    id: Mapped[str] = mapped_column(primary_key=True)
    callback_url: Mapped[str] = mapped_column()
    available: Mapped[bool] = mapped_column(default=True)
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()

    @classmethod
    def create(
        cls,
        id: str,
        callback_url: str,
        available: bool,
        x: int,
        y: int,
    ) -> "Taxi":
        kwargs = {
            "id": id,
            "callback_url": callback_url,
            "available": available,
            "x": x,
            "y": y,
        }
        return cls(**kwargs)
