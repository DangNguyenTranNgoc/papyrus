#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Papyrus is a tool for storing and managing performance data.

This is the controller module for the Papyrus tool.
"""
from uuid import uuid4

from model import BaseModel, ColumnInfo, TableInfo, NamespaceInfo
from utils import (
    get_logger, start_logging,
    SQLAlchemyDatabase
)
from dao import TableRepository, Repositories


LOGGER = get_logger("papyrus.main")
start_logging()

LOGGER.info("Papyrus is starting...")
db = SQLAlchemyDatabase(
    "sqlite:////Users/tranngocdangnguyen/Projects/papyrus/papyrus/tests/data/uc.db"
)
db.connect()
LOGGER.info("Database connected")
BaseModel.metadata.create_all(db.session.get_bind())
repositories = Repositories(db)
LOGGER.info("Repositories created")

LOGGER.info("Database schema created")
with db.session as s:
    metric = NamespaceInfo(
        name="metric",
        comment="Metric namespace",
        created_by="nguyen",
        owner="nguyen",
        updated_by="nguyen",
        tables=[TableInfo(
        name="metric",
        comment="Metric table",
        column_count=2,
        data_source_format="csv",
        url="file://catalog/etc/db/uc.db",
        created_by="nguyen",
        owner="nguyen",
        updated_by="nguyen",
        columns=[ColumnInfo(
            name="metric_id",
            comment="Metric ID",
            position=1,
            dtype_text="integer",
            dtype_json="int",
            dtype_name="int",
            dtype_precision=10,
            dtype_scale=0,
            dtype_interval="",
            nullable=False,
            ),ColumnInfo(
            name="metric_name",
            comment="Metric Name",
            position=2,
            dtype_text="string",
            dtype_json="str",
            dtype_name="str",
            dtype_precision=0,
            dtype_scale=0,
            dtype_interval="",
            nullable=True,
        )]
    )])
    s.add(metric)
    s.commit()
    print(metric)

print("="*50)
table_repo = TableRepository(db, repositories)
table = table_repo.get_table_by_id(metric.id)
print(table)

print("="*50)
tables = table_repo.get_all_tables()
for t in tables:
    print(t)
