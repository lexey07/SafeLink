from datetime import datetime

from pydantic import BaseModel


class HistoryResponse(BaseModel):
    id: int
    url: str
    status: str
    risk_score: int
    reasons: list[str]
    ai_explanation: str
    created_at: datetime

    class Config:
        from_attributes = True