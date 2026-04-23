from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NoteItemBase


class HistoryAddRequest(BaseModel):
    note_id: int = Field(...,alias="noteId")

class HistoryNoteItemResponse(NoteItemBase):
    history_id: int = Field(alias="historyId")
    history_time: datetime = Field(alias="historyTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryListResponse(BaseModel):
    list: list[HistoryNoteItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
