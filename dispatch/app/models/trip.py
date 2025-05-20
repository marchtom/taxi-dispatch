import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models import TaxiModel


class Trip(Base):
    __tablename__ = "trip"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
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
    taxi_id: Mapped[str] = mapped_column(
        ForeignKey("taxi.id"),
        nullable=True,
    )

    taxi: Mapped[TaxiModel] = relationship(
        "Taxi",
        foreign_keys=[taxi_id],
    )

    @classmethod
    def create(
        cls,
        id: str,
        x_start: int,
        y_start: int,
        x_stop: int,
        y_stop: int,
        start_time: datetime | None = None,
        taxi_id: str | None = None,
    ) -> "Trip":
        kwargs = {
            "id": id,
            "start_time": start_time,
            "x_start": x_start,
            "y_start": y_start,
            "x_stop": x_stop,
            "y_stop": y_stop,
            "taxi_id": taxi_id,
        }
        return cls(**kwargs)