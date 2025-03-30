#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dao import TableRepository

class TableService:
    """
    Table service
    """

    def __init__(self, table_repository: TableRepository):
        self.table_repository:TableRepository = table_repository

    def get_table(self, table_name: str):
        """
        Get table by table full name <namespace>.<table_name>
        """
        pass

    def list_tables(self):
        """
        List all tables
        """
        return self.table_repository.get_tables()

    def create_table(self, table):
        """
        Create a table.
        Validate the table before creating it.
        """
        # Validate table
        return self.table_repository.create_table(table)


    def delete_table(self, table_id: int):
        """
        Delete a table by table ID
        """
        table = self.table_repository.get_table_by_id(table_id)
        if not table:
            raise ValueError(f"Table with ID {table_id} not found")
        self.table_repository.delete_table(table_id)
        return table
