from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Integer, Text, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间",
    )

class Favorite(Base):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, comment="用户id")
    note_id: Mapped[int] = mapped_column(Integer, comment="随笔id")
