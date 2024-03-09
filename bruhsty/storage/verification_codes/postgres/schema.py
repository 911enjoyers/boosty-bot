from datetime import datetime

from sqlalchemy import String, Time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import functions
from bruhsty.storage.sql.base import Base

__all__ = ["VerificationCode"]


class VerificationCode(Base):
    __tablename__ = "verification_codes"
    code_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(Time(timezone=True), default=functions.now())
    valid_until: Mapped[datetime] = mapped_column(Time(timezone=True))
    used_at: Mapped[bool | None] = mapped_column(default=False, nullable=True)
