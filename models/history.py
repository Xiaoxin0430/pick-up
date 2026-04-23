from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    view_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="浏览时间",
    )

class History(Base):
    __tablename__ = "history"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer,comment="用户id")
    note_id:Mapped[int] = mapped_column(Integer,comment="随笔id")