#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID

from model import NamespaceInfo
from utils.database import Database
from utils.logger import get_logger

LOGER = get_logger("repository.table")

class NamespaceRepository:
    """
    Repository for working with namespace info
    """

    def __init__(self, db: Database, repositories):
        self.session = db.connect()
        self.repositories = repositories


    def get_namespace_by_name(self, namespace_name: str) -> NamespaceInfo|None:
        """
        Get namespace by namespace name
        """
        LOGER.info("Find namespace by name: %s", namespace_name)
        namespace = self.session \
                        .query(NamespaceInfo) \
                        .filter(NamespaceInfo.name == namespace_name) \
                        .first()
        return namespace


    def get_namespace_by_id(self, namespace_id: UUID) -> NamespaceInfo|None:
        """
        Get namespace by namespace ID 
        """
        LOGER.info("Find namespace by ID: %s", namespace_id)
        namespace = self.session \
                        .query(NamespaceInfo) \
                        .filter(NamespaceInfo.id == namespace_id) \
                        .first()
        return namespace


    def get_all_namespaces(self) -> list[NamespaceInfo]:
        """
        Get all namespaces
        """
        LOGER.info("Find all namespaces")
        namespaces = self.session.query(NamespaceInfo).all()
        return namespaces
    

    def create_namespace(self, namespace: NamespaceInfo):
        """
        Create namespace
        """
        LOGER.info("Create namespace: %s", namespace)
        self.session.add(namespace)
        self.session.commit()


    def delete_namespace(self, namespace: NamespaceInfo):
        """
        Delete namespace
        """
        LOGER.info("Delete namespace: %s", namespace)
        self.session.delete(namespace)
        self.session.commit()
