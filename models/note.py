from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Integer, Text, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 基类
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    )

# 随笔分类表模型类
class note_category(Base):
    __tablename__ = "note_category"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="分类id")
    name: Mapped[str] = mapped_column(String(50),unique=True,nullable=False,comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer,default=0,nullable=False,comment="排序顺序")

    def __repr__(self):
        return f"<note_category {self.id} {self.name} {self.sort_order}>"

# 随笔列表模型类
class Note(Base):
    __tablename__ = "note"

    # 创建索引提升查询速度
    __table_args__ = (
        Index("fk_note_category_idx", 'category_id'),
        Index("idx_publish_time", 'publish_time'),
    )

    id: Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    title:Mapped[str]=mapped_column(String(255),nullable=False)
    description:Mapped[Optional[str]]=mapped_column(String(500))
    content:Mapped[str]=mapped_column(Text,nullable=False)
    image:Mapped[Optional[str]]=mapped_column(String(255))
    author:Mapped[Optional[str]]=mapped_column(String(50))
    category_id:Mapped[int]=mapped_column(Integer)
    views: Mapped[int] = mapped_column(Integer, default=0,nullable=False)
    publish_time:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)




