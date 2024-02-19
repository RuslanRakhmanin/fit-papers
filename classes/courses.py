# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
"""
Implements the Courses class, which represents a course in the database.
"""
from typing import Optional

from classes.db_object import DbObject

class Courses(DbObject):
    """
    Represents a course in the database.
    """
    __cache = dict[int, 'Courses']()

    def __new__(cls,
                 db_id : Optional[int] = None,
                 name: str = "",
                 prefix: str = "",
                 description: str = "",
                 file_path: str = ""
                 ) -> 'Courses':
        if db_id in cls.__cache:
            obj = cls.__cache[db_id]
        else:
            obj = super(Courses, cls).__new__(cls)
            assert isinstance(obj, Courses) # This idiotic assertion is here to make mypy and pylint happy
        return obj

    def __init__(self,
                 db_id : Optional[int] = None,
                 name: str = "",
                 prefix: str = "",
                 description: str = "",
                 file_path: str = "") -> None:
        super().__init__()
        if db_id is not None and db_id in self.__cache:
            self.read_data_from_db()
        else:
            self.db_id = db_id
            if db_id is None or not self.read_data_from_db():
                self.name = name
                self.prefix = prefix
                self.description = description
                self.file_path = file_path

            if db_id is not None:
                self.__cache[db_id] = self


    @classmethod
    def read_all_objects_from_db(cls) -> list['Courses']:
        """
        Reads all objects from the database and populates the 'name' and 'description' attributes.
        """
        result = list['Courses']()
        cls._cursor.execute("SELECT * FROM courses")
        rows = cls._cursor.fetchall()
        for row in rows:
            result.append(cls(db_id=row[0], name=row[1], prefix=row[2], description=row[3], file_path=row[4]))
        return result

    @classmethod
    def create_tables(cls) -> None:
        """
        Creates the 'courses' table in the database.
        """
        cls._cursor.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, prefix TEXT, description TEXT, file_path TEXT)")
        cls._db.commit()

    @classmethod
    def check_if_exists_in_db(cls, db_id) -> bool:
        """
        Checks if the object exists in the database.
        """
        cls._cursor.execute("SELECT * FROM courses WHERE id = :id", {"id": db_id})
        row = cls._cursor.fetchone()
        return not row is None
    
    def read_data_from_db(self) -> bool:
        """
        Reads an object from the database by the 'db_id' and populates the 'name' and 'description' attributes.
        """
        self._cursor.execute("SELECT * FROM courses WHERE id = :id", {"id": self.db_id})
        row = self._cursor.fetchone()
        if not row is None:
            self.name = row[1]
            self.prefix = row[2]
            self.description = row[3]
            self.file_path = row[4]
            return True
        else:
            return False

    def save_object_to_db(self) -> None:
        """
        Saves an object to the database.
        """
        if self.db_id is not None:
            self._cursor.execute("UPDATE courses SET name = :name, prefix = :prefix, description = :description, file_path = :file_path WHERE id = :id",
                                {"name": self.name, "prefix": self.prefix, "description": self.description, "file_path": self.file_path, "id": self.db_id})
        else:
            self._cursor.execute("INSERT INTO courses (name, prefix, description, file_path) VALUES (:name, :prefix, :description, :file_path)",
                                {"name": self.name, "prefix": self.prefix, "description": self.description, "file_path": self.file_path})
            self.db_id = self._cursor.lastrowid
        self._db.commit()

    def __repr__(self) -> str:
        return f"Course(id={self.db_id}, name={self.name}, prefix={self.prefix}, description={self.description}, file_path={self.file_path})"
    