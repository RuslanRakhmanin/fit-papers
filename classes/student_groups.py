# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
"""
Implements the StudentGroups class, which represents a module in the database.
"""
from typing import Optional

from classes.db_object import DbObject

class StudentGroups(DbObject):
    """
    Implements the StudentGroups class, which represents a group in the database.
    """
    __cache = dict[int, 'StudentGroups']()

    def __new__(cls,
                 db_id: Optional[int] = None,
                 name: str = "",
                 description: str = ""
                 ) -> 'StudentGroups':
        
        if db_id is not None and db_id in cls.__cache:
            obj = cls.__cache[db_id]
        else:
            obj = super().__new__(cls)
            assert(isinstance(obj, StudentGroups)) # This idiotic assertion is here to make mypy and pylint happy
        return obj

    def __init__(self,
                db_id: Optional[int] = None,
                name: str = "",
                description: str = "") -> None:
        
        super().__init__()
        if db_id is not None and db_id in self.__cache:
            self.read_data_from_db()
        else:
            self.db_id = db_id
            if db_id is None or not self.read_data_from_db():
                self.name = name
                self.description = description
        if db_id is not None:
            self.__cache[db_id] = self
        

    def __repr__(self) -> str:
        return f"StudentGroup(id={self.db_id}, name={self.name}, description={self.description}"

    @classmethod
    def create_tables(cls) -> None:
        """
        Creates the 'student_groups' table in the database.
        """
        cls._cursor.execute("CREATE TABLE IF NOT EXISTS student_groups (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")
        cls._db.commit()        

    @classmethod
    def read_all_objects_from_db(cls) -> list['StudentGroups']:
        """
        Reads all objects from the database and populates the 'name' and 'description' attributes.
        """
        result = list['StudentGroups']()
        cls._cursor.execute("SELECT * FROM student_groups")
        rows = cls._cursor.fetchall()
        for row in rows:
            result.append(cls(db_id=row[0], name=row[1], description=row[2]))
        return result
    
       
    def read_data_from_db(self) -> None:
        """
        Reads an object from the database by the 'db_id', creates an object
          and populates the object properties.
        """
        self._cursor.execute("SELECT * FROM student_groups WHERE id = :id", {"id": self.db_id})
        row = self._cursor.fetchone()
        if not row is None:
            self.name = row[1]
            self.description = row[2]

    def save_object_to_db(self) -> None:
        """
        Saves an object to the database.
        """
        if self.db_id is None:
            self._cursor.execute("INSERT INTO student_groups (name, description) VALUES (:name, :description)",
                                {"name": self.name, "description": self.description})
            self.db_id = self._cursor.lastrowid
        else:
            self._cursor.execute("UPDATE student_groups SET name = :name, description = :description WHERE id = :id",
                                {"id": self.db_id, "name": self.name, "description": self.description})
        self._db.commit()
