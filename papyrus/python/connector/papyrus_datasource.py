#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Data Source/Connector for Spark

1. First, create schema read from Papyrus
Example:
schema = StructType([
    StructField("id", LongType(), True),
    StructField("desc", StringType(), True)
])

2. Create new Catalog Table
Example:
new_table = spark.catalog.createTable(
    "my_table",
    schema=schema,
    source="parquet",
    path="/Users/tranngocdangnguyen/Projects/unitycatalog/mnt/data/"
)

"""
from pyspark.sql.datasource import DataSource, DataSourceReader, DataSourceWriter, WriterCommitMessage
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)
from typing import Iterator, List
from pyspark.sql.types import Row
from dataclasses import dataclass