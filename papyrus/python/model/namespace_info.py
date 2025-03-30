#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import (
    mapped_column, Mapped, relationship
)
from sqlalchemy import (
    String
)

from .base_model import BaseModel

@dataclass
class NamespaceInfo(BaseModel):
    """
    Entity store info about a Namespace
    ---
    """
    __tablename__ = "namespaces"

    created_by: Mapped[str] = mapped_column("created_by", String)
    owner: Mapped[str] = mapped_column("owner", String)
    updated_by: Mapped[str] = mapped_column("updated_by", String)

    tables: Mapped[List["TableInfo"]] = relationship(
        back_populates="namespace", cascade="all, delete-orphan"
    )
