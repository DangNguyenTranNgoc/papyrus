#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database(ABC):
    """
    Abstract class for database connector
    """
    def __init__(self):
        super().__init__()


    @abstractmethod
    def connect(self):
        """
        Open connection
        """
        raise NotImplementedError()


    @abstractmethod
    def close(self):
        """
        Close connection
        """
        raise NotImplementedError()


    def __del__(self):
        self.close()


class SQLAlchemyDatabase(Database):
    """
    Connect to SQLAlchemy database

    Attributes:
    db_url: str -- database URL
    session: Session -- SQLAlchemy session
    """
    __db_type = "SQLAlchemy"

    def __init__(self, db_url: str):
        super().__init__()
        self.db_url = db_url
        self.session = None


    def connect(self):
        """
        Open new session and connect to database
        """
        if self.session is not None:
            return self.session
        enigne = create_engine(self.db_url, echo=True)
        session = sessionmaker(bind=enigne)
        self.session = session()
        return self.session


    def close(self):
        """
        Close session if it is opened
        """
        if self.session is not None:
            self.session.close()
            self.session = None
