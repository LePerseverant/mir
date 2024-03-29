from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy_serializer import SerializerMixin


if TYPE_CHECKING:
    from .device import Device
else:
    Device = "Device"

@dataclass
class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.current_timestamp(), onupdate=func.current_timestamp())
    devices: Mapped[Optional[List[Device]]] = relationship(back_populates="customer", lazy="joined")
