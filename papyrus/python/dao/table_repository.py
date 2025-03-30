#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID
from sqlalchemy.orm import Session

from model import TableInfo, NamespaceInfo
from utils.database import Database
from utils.logger import get_logger

LOGER = get_logger("repository.table")

class TableRepository:
    """
    Repository for working with table info
    """

    def __init__(self, db: Database, repositories):
        self.session:Session = db.connect()
        self.repositories = repositories


    def get_table_by_name(self, table_name: str) -> TableInfo|None:
        """
        Get table by table name
        """
        LOGER.info("Find table by name: %s", table_name)
        try:
            name_parts = table_name.split(".")
            if len(name_parts) != 2:
                raise ValueError(f"Invalid table name: {table_name}")
            # Name of namespace
            ns = name_parts[0]
            # Name of table
            tbl_name = name_parts[1]
            table = self.find_table(ns, tbl_name)
            return table
        except Exception as e:
            #TODO: This catch block is prepared for transaction management
            LOGER.error("Error when find table by name: %s", table_name)
            raise e


    def find_table(self, namespace: str, table_name:str) -> TableInfo|None:
        """
        Find table with namespace and name of table
        """
        LOGER.info("Find table: %s.%s", namespace, table_name)
        ns_id = self.get_namespace_id(namespace)
        table = self.find_table_by_ns_id_and_name(ns_id, table_name)
        return table


    def get_namespace_id(self, namespace) -> UUID:
        """
        Find namespace by name and return it's id
        """
        ns = self.repositories.get_namespace_repository().get_namespace_by_name(namespace)
        if not ns:
            raise ValueError(f"Namespace [{namespace}] is not found")
        return ns.id


    def find_table_by_ns_id_and_name(self, namespace_id:UUID, table_name:str) -> TableInfo:
        """
        Find a table with namespace id and name of table
        """
        LOGER.info("Find table with namespace id: %s  and name: %s", namespace_id, table_name)
        table: TableInfo = self.session \
                               .query(TableInfo) \
                               .filter(
                                   TableInfo.name == table_name,
                                   TableInfo.namespace_id == namespace_id) \
                               .first()
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
