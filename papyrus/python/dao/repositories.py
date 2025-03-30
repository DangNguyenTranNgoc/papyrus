#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .table_repository import TableRepository
from .namespace_repository import NamespaceRepository
from utils.database import Database

class Repositories:
    """
    Repositories manager
    """

    def __init__(self, database: Database):
        self.table_repository = TableRepository(database, self)
        self.namespace_repository = NamespaceRepository(database, self)


    def get_table_repository(self) -> TableRepository:
        """
        Get table repository
        """
        return self.table_repository


    def get_namespace_repository(self) -> NamespaceRepository:
        """
        Get namespace repository
        """
        return self.namespace_repository
