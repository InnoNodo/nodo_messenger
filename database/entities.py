from typing import List

from sqlalchemy import JSON, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column

from config import Settings

JSONType = JSON()
if Settings().database.connection_string.startswith("postgresql"):
    JSONType = postgresql.JSONB()


class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {List[int]: JSONType, dict: JSONType}

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()


__all__ = [
    "Base",
    "User",
]
