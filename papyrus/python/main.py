#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Papyrus is a tool for storing and managing performance data.

This is the controller module for the Papyrus tool.
"""
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import Sessions

from model import BaseModel, Columns, Tables

engine = create_engine("sqlite:////Users/tranngocdangnguyen/Projects/papyrus/papyrus/tests/data/uc.db", echo=True)

BaseModel.metadata.create_all(engine)

with Session(engine) as session:
    metric = Tables(
        name="metric",
        comment="Metric table",
        schema_id=uuid4(),
        column_count=2,
        data_source_format="csv",
        url="file://home/nguyen/projects/unitycatalog/etc/db/uc.db",
        created_by="nguyen",
        owner="nguyen",
        updated_by="nguyen",
        columns=[Columns(
            name="metric_id",
            comment="Metric ID",
            position=1,
            col_text="integer",
            col_json="int",
            col_name="int",
            col_precision=10,
            col_scale=0,
            col_interval="",
            nullable=False,
            ),Columns(
            name="metric_name",
            comment="Metric Name",
            position=2,
            col_text="string",
            col_json="str",
            col_name="str",
            col_precision=0,
            col_scale=0,
            col_interval="",
            nullable=True,
        )]
    )
    session.add(metric)
    session.commit()
    print(metric)
    print(metric.columns)



