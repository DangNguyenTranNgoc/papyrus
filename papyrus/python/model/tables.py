#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List
import uuid

from sqlalchemy.orm import (
    mapped_column, Mapped, relationship
)
from sqlalchemy import (
    Integer, String, UUID
)

from . import BaseModel, Columns

class Tables(BaseModel):
    """
    Entity store info about a table
    ---
    """
    __tablename__ = "tables"

    schema_id: Mapped[uuid.UUID] = mapped_column("schema_id", UUID)
    column_count: Mapped[int] = mapped_column("column_count", Integer)
    data_source_format: Mapped[str] = mapped_column("data_source_format", String)
    url: Mapped[str] = mapped_column("url", String)
    created_by: Mapped[str] = mapped_column("created_by", String)
    owner: Mapped[str] = mapped_column("owner", String)
    updated_by: Mapped[str] = mapped_column("updated_by", String)

    columns: Mapped[List["Columns"]] = relationship(
        back_populates="table", cascade="all, delete-orphan"
    )
