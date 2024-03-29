from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm.mapper import validates
from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, Enum
import enum
import ipaddress
import macaddress
from typing import Optional, TYPE_CHECKING
from sqlalchemy_serializer import SerializerMixin


if TYPE_CHECKING:
    from .customer import Customer
else:
    Customer = "Customer"

class DeviceStatus(str ,enum.Enum):
    ACTIVE = "ACTIVE"
    NOT_ACTIVE = "NOT ACTIVE"
    DISABLED = "DISABLED"

class DeviceCategory(str, enum.Enum):
    ROUTER = "ROUTER"
    SWITCH = "SWITCH"
    BRIDGE = "BRIDGE"
    REPEATER = "REPEATER"
    WIRELESS_ACCESS_POINT = "WIRELESS ACCESS POINT"
    NETWORK_INTERFACE_CARD = "NETWORK INTERFACE CARD"
    FIREWALL = "FIREWALL"
    HUB = "HUB"
    MODEM = "MODEM"
    GATEWAY = "GATEWAY"

@dataclass
class Device(db.Model, SerializerMixin):
    __tablename__ = "devices"
    serialize_only = ("device_id", "device_mac_address", "device_ip_v4_address", "device_category", "device_status", "created_at", "updated_at",  "customer", "-customer.devices")

    device_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_mac_address: Mapped[str] = mapped_column(unique=True, nullable=False)
    device_ip_v4_address: Mapped[Optional[str]] = mapped_column(nullable=True)
    device_category: Mapped[DeviceCategory] = mapped_column(Enum(DeviceCategory, native_enum=False, validate_strings=True), nullable=False)
    device_status: Mapped[DeviceStatus] = mapped_column(Enum(DeviceStatus, native_enum=False, validate_strings=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.current_timestamp(), onupdate=func.current_timestamp())
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=True)
    customer: Mapped[Optional[Customer]] = relationship(foreign_keys=customer_id, back_populates="devices", lazy="joined")

    @validates("device_mac_address")
    def mac_address_validator(self, key, value):
        try:
            macaddress.MAC(value)
        except ValueError as error:
            raise ValueError(f"Invalid MAC address: {error}")
        return value

    @validates("device_ip_v4_address")
    def ip_v4_address_validator(self, key, value):
        try:
            ipaddress.ip_address(value)
        except ValueError as error:
            raise ValueError(f"Invalid IP address: {error}")
        return value
