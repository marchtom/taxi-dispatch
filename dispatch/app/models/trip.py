from datetime import datetime, timezone

from sqlalchemy import DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Trip(Base):
    __tablename__ = "trip"

    id: Mapped[str] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    x_start: Mapped[int] = mapped_column()
    y_start: Mapped[int] = mapped_column()
    x_stop: Mapped[int] = mapped_column()
    y_stop: Mapped[int] = mapped_column()

    @classmethod
    def create(
        cls,
        id: str,
        x_start: int,
        y_start: int,
        x_stop: int,
        y_stop: int,
        start_time: datetime | None = None,
    ) -> "Trip":
        kwargs = {
            "id": id,
            "start_time": start_time,
            "x_start": x_start,
            "y_start": y_start,
            "x_stop": x_stop,
            "y_stop": y_stop,
        }
        return cls(**kwargs)