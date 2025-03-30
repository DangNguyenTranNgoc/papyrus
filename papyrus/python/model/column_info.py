#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Information about columns in the table
"""
from uuid import UUID
from dataclasses import dataclass
from sqlalchemy.orm import (
    mapped_column, Mapped, relationship
)
from sqlalchemy import (
    Integer, String, ForeignKey
)

from . import BaseModel

@dataclass
class ColumnInfo(BaseModel):
    """
    Entity store info about a column
    """
    __tablename__ = "columns"

    position: Mapped[int] = mapped_column(Integer)
    dtype_text: Mapped[str] = mapped_column(String)
    dtype_json: Mapped[str] = mapped_column(String)
    dtype_name: Mapped[str] = mapped_column(String)
    dtype_precision: Mapped[int] = mapped_column(Integer)
    dtype_scale: Mapped[int] = mapped_column(Integer)
    dtype_interval: Mapped[str] = mapped_column(String)
    nullable: Mapped[bool] = mapped_column(Integer)

    table_id: Mapped[UUID] = mapped_column(ForeignKey("tables.id"))

    table: Mapped["TableInfo"] = relationship(back_populates="columns")
