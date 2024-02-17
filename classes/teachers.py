# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
"""
Implements the Teachers class, which represents a teacher in the database.
"""
from typing import Optional, Any

from classes.db_object import DbObject

class Teachers(DbObject):
    """
    Implements the Teachers class, which represents a teacher in the database.
    """
    __cache = dict[int, 'Teachers']()

    def __new__(cls, db_id: Optional[int] = None, name: str = "", signature: Any = None) -> 'Teachers':
        if db_id in cls.__cache:
            obj = cls.__cache[db_id]
            obj.read_data_from_db()
        else:
            obj = super().__new__(cls)
            obj.db_id = db_id
            if db_id is None or not obj.read_data_from_db():
                obj.name = name
                obj.signature = signature

            cls.__cache[db_id] = obj

        return obj
    
    def __repr__(self) -> str:
        return f"Teacher(id={self.db_id}, name={self.name})"
    
    @classmethod
    def create_tables(cls):
        """
        Creates the 'teachers' table in the database.
        """
        cls._cursor.execute("CREATE TABLE IF NOT EXISTS teachers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, signature BLOB)")

    @classmethod
    def read_all_objects_from_db(cls) -> list['Teachers']:
        """
        Reads all objects from the database and populates the 'name' attribute.
        """
        result = list['Teachers']()
        cls._cursor.execute("SELECT * FROM teachers")
        rows = cls._cursor.fetchall()
        for row in rows:
            result.append(cls(db_id=row[0], name=row[1], signature=row[2]))
        return result
    
    
    def read_data_from_db(self) -> None:
        """
        Reads an object from the database by the 'db_id' and populates the object properties.
        """
        self._cursor.execute("SELECT * FROM teachers WHERE id = :id", {"id": self.db_id})
        row = self._cursor.fetchone()
        if not row is None:
            self.name = row[1]
            self.signature = row[2]

    def save_object_to_db(self) -> None:
        """
        Saves an object to the database.
        """
        if self.db_id is None:
            self._cursor.execute("INSERT INTO teachers (name, signature) VALUES (:name, :signature)", {"name": self.name, "signature": self.signature})
            self.db_id = self._cursor.lastrowid
        else:
            self._cursor.execute("UPDATE teachers SET name = :name, signature = :signature WHERE id = :id", {"name": self.name, "signature": self.signature, "id": self.db_id})
        self._db.commit()
