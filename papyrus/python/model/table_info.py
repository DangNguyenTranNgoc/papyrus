#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.orm import (
    mapped_column, Mapped, relationship
)
from sqlalchemy import (
    Integer, String, ForeignKey
)

from .base_model import BaseModel

@dataclass
class TableInfo(BaseModel):
    """
    Entity store info about a table
    ---
    """
    __tablename__ = "tables"

    column_count: Mapped[int] = mapped_column("column_count", Integer)
    data_source_format: Mapped[str] = mapped_column("data_source_format", String)
    url: Mapped[str] = mapped_column("url", String)
    created_by: Mapped[str] = mapped_column("created_by", String)
    owner: Mapped[str] = mapped_column("owner", String)
    updated_by: Mapped[str] = mapped_column("updated_by", String)

    namespace_id: Mapped[UUID] = mapped_column(ForeignKey("namespaces.id"))
    namespace: Mapped["NamespaceInfo"] = relationship(back_populates="tables")

    columns: Mapped[List["ColumnInfo"]] = relationship(
        back_populates="table", cascade="all, delete-orphan"
    )
