from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Taxi(Base):
    __tablename__ = "taxi"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    callback_url: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    x: Mapped[int] = mapped_column()
    y: Mapped[int] = mapped_column()

    @classmethod
    def create(
        cls,
        id: str,
        callback_url: str,
        active: bool,
        x: int,
        y: int,
    ) -> "Taxi":
        kwargs = {
            "id": id,
            "callback_url": callback_url,
            "active": active,
            "x": x,
            "y": y,
        }
        return cls(**kwargs)