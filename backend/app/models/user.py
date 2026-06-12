from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    nickname = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    avatar = Column(String, nullable=True)

    verification_code = Column(String, nullable=True)

    email_verified = Column(Boolean, default=False)

    checks_left = Column(Integer, default=5)

    is_premium = Column(Boolean, default=False)