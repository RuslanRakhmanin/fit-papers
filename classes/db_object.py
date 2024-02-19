# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
"""
The abstract base class for database objects.
"""

from abc import abstractmethod
from typing import Any
from sqlite3 import Cursor, Connection
import os

class DbObject:
    """
    Represents an object in the database.
    """
    _db: Connection
    _cursor: Cursor
    _course_path = ""

    def __new__(cls) -> 'DbObject':
        obj = super().__new__(cls)
        return obj

    def __init__(self) -> None:
        self.additional_data = dict[str, Any]()

    @classmethod
    def setup_db(cls, db, cursor) -> None:
        """
        Sets up the database connection.
        """
        cls._db = db
        cls._cursor = cursor
    @classmethod
    def setup_course_path(cls, course_path) -> None:
        """
        Sets the course path.
        """
        cls._course_path = course_path

    @classmethod
    def check_path_exists(cls, path: str) -> bool:
        """
        Checks if the path exists.
        """
        return os.path.exists(path)
    
    @classmethod
    @abstractmethod
    def create_tables(cls) -> None:
        """
        Creates table/tables for the class in the database.
        """

    @classmethod
    @abstractmethod
    def read_all_objects_from_db(cls) -> list[Any]:
        """
        Reads all objects of the class from the database and creates 
        a list of objects that are populated from the database.
        """


    @abstractmethod
    def read_data_from_db(self) -> None:
        """
        Reads an object from the database and populates the object properties.
        """    

    @abstractmethod
    def save_object_to_db(self) -> None:
        """
        Saves the object to the database.
        """
