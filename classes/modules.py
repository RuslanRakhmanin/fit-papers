# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
"""
Implements the Modules class, which represents a module in the database.
"""
from typing import Optional

from classes.db_object import DbObject

class Modules(DbObject):
    """
    Represents a module in the database.
    """
    __cache = dict[int, 'Modules']()
    __table_name = "modules"

    def __new__(cls, db_id: Optional[int] = None, name: str = "", description: str = "", code: str = "") -> 'Modules':
        if db_id in cls.__cache:
            obj = cls.__cache[db_id]
        else:
            obj = super().__new__(cls)
            assert isinstance(obj, Modules) # This idiotic assertion is here to make mypy and pylint happy
        return obj

    def __init__(self, db_id: Optional[int] = None, name: str = "", description: str = "", code: str = "") -> None:
        super().__init__()
        self.db_id = db_id
        if db_id is None or not self.read_data_from_db():
            self.name = name
            self.description = description
            self.code = code
        if db_id is not None:
            self.__cache[db_id] = self


    def __repr__(self) -> str:
        return f"Module(id={self.db_id}, code={self.code}, name={self.name}, description={self.description})"
    
    @classmethod
    def create_tables(cls) -> None:
        """
        Creates the 'modules' table in the database.
        """
        cls._cursor.execute("CREATE TABLE IF NOT EXISTS modules (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT, name TEXT, description TEXT)")
        cls._db.commit()       

    @classmethod
    def read_all_objects_from_db(cls) -> list['Modules']:
        """
        Reads all objects from the database and populates all the attributes.
        """
        result = list['Modules']()
        cls._cursor.execute("SELECT * FROM modules")
        rows = cls._cursor.fetchall()
        for row in rows:
            result.append(cls(db_id=row[0], code=row[1], name=row[2], description=row[3]))
        return result
    
    def read_data_from_db(self) -> None:
        """
        Reads an object from the database by the 'db_id', creates an object
          and populates the object properties.
        """
        self._cursor.execute("SELECT * FROM modules WHERE id = :id", {"id": self.db_id})
        row = self._cursor.fetchone()
        if not row is None:
            self.code = row[1]
            self.name = row[2]
            self.description = row[3]

    def save_object_to_db(self) -> None:
        """
        Saves an object to the database.
        """
        if self.db_id is not None:
            self._cursor.execute("UPDATE modules SET code = :code, name = :name, description = :description WHERE id = :id",
                                {"code": self.code, "name": self.name, "description": self.description, "id": self.db_id})
        else:
            self._cursor.execute("INSERT INTO modules (code, name, description) VALUES (:code, :name, :description)",
                                {"code": self.code, "name": self.name, "description": self.description})
            self.db_id = self._cursor.lastrowid
        self._db.commit()
    
    @classmethod
    def find_by_attribute(cls, attribute_name: str, attribute_value: str) -> Optional['Modules']:
        """
        Finds an object in the database by the 'attribute_name' and 'attribute_value'.
        """
        cls._cursor.execute(f"SELECT * FROM {cls.__table_name} WHERE {attribute_name} = :attribute_value", {"attribute_value": attribute_value})
        row = cls._cursor.fetchone()
        if not row is None:
            return cls(db_id=row[0], code=row[1], name=row[2], description=row[3])
        else:
            return None
        