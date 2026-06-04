from sqlalchemy import Column, Integer, String
from app.database.database import Base

class UrlCheck(Base):
    __tablename__ = "url_checks"

    id = Column(Integer, primary_key=True, index=True)

    url = Column(String, nullable=False)

    status = Column(String, nullable=False)

    username = Column(String, nullable=False)