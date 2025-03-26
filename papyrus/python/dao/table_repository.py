#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID

from model.table_info import TableInfo
from utils.database import Database
from utils.logger import get_logger

LOGER = get_logger("repository.table")

class TableRepository:
    """
    Repository for working with table info
    """

    def __init__(self, db: Database):
        self.session = db.connect()


    def get_table_by_name(self, table_name: str) -> TableInfo|None:
        """
        Get table by table name
        """
        LOGER.info("Find table by name: %s", table_name)
        table = self.session.query(TableInfo).filter(TableInfo.name == table_name).first()
        return table


    def get_table_by_id(self, table_id: UUID) -> TableInfo|None:
        """
        Get table by table ID 
        """
        LOGER.info("Find table by ID: %s", table_id)
        table = self.session.query(TableInfo).filter(TableInfo.id == table_id).first()
        return table


    def get_all_tables(self) -> list[TableInfo]:
        """
        Get all tables
        """
        LOGER.info("Find all tables")
        tables = self.session.query(TableInfo).all()
        return tables


    def create_table(self, table: TableInfo):
        """
        Create table
        """
        LOGER.info("Create table: %s", table)
        self.session.add(table)
        self.session.commit()


    def delete_table(self, table: TableInfo):
        """
        Delete table
        """
        LOGER.info("Delete table: %s", table)
        self.session.delete(table)
        self.session.commit()
