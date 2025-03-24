#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Information about columns in the table
"""
from uuid import UUID
from sqlalchemy.orm import (
    mapped_column, Mapped, relationship
)
from sqlalchemy import (
    Integer, String, ForeignKey
)

from . import BaseModel

class Columns(BaseModel):
    """
    Entity store info about a column
    """
    __tablename__ = "columns"

    position: Mapped[int] = mapped_column(Integer)
    col_text: Mapped[str] = mapped_column(String)
    col_json: Mapped[str] = mapped_column(String)
    col_name: Mapped[str] = mapped_column(String)
    col_precision: Mapped[int] = mapped_column(Integer)
    col_scale: Mapped[int] = mapped_column(Integer)
    col_interval: Mapped[str] = mapped_column(String)
    nullable: Mapped[bool] = mapped_column(Integer)

    table_id: Mapped[UUID] = mapped_column(ForeignKey("tables.id"))

    table: Mapped["Tables"] = relationship(back_populates="columns")

    def __repr__(self) -> str:
        # pylint: disable=line-too-long
        return f"{{'name':'{self.name}','col_text':'{self.col_text}','col_json':'{self.col_json}','col_name':'{self.col_name}','col_precision':{self.col_precision},'col_scale':{self.col_scale},'col_interval_type':'{self.col_interval}','position':{self.position},'comment':'{self.comment}','nullable':{self.nullable}}}"
        # pylint: enable=line-too-long

