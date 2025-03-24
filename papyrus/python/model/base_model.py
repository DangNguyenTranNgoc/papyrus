#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base data model class
"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column
)
from sqlalchemy import (
    String, DateTime, Boolean
)

class BaseModel(DeclarativeBase):
    """
    Based Entity class
    """
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    date_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    comment: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
