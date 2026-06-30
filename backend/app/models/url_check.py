from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSON

from app.database.database import Base


class UrlCheck(Base):
    __tablename__ = "url_checks"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String, nullable=False)

    status = Column(String, nullable=False)

    risk_score = Column(Integer, nullable=False)

    reasons = Column(JSON, nullable=False)

    ai_explanation = Column(String, nullable=False)

    username = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )