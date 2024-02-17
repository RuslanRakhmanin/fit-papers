# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace
"""
Implements the Assessments class, which represents an assessment in the database.
"""
from datetime import date
from typing import Optional

from classes.db_object import DbObject

from classes.modules import Modules
from classes.teachers import Teachers
from classes.student_groups import StudentGroups

class Assessments(DbObject):
    """
    Represents an assessment in the database.
    """
    __cache = dict[int, 'Assessments']()

    def __new__(cls, db_id: Optional[int] = None,
                    module: Modules = None,
                    teacher: Teachers = None,
                    student_group: StudentGroups = None,
                    date_data: date = None,
                    file_path: str = ""
                ) -> 'Assessments':
        if db_id in cls.__cache:
            obj = cls.__cache[db_id]
            obj.read_data_from_db()
        else:
            obj = super().__new__(cls)
            obj.db_id = db_id
            if db_id is None or not obj.read_data_from_db():
                obj.module = module
                obj.teacher = teacher
                obj.student_group = student_group
                obj.date = date_data
                obj.file_path = file_path
            obj.path_is_present = cls.check_path_exists(obj.file_path)
            cls.__cache[db_id] = obj

        return obj

    def __repr__(self) -> str:
        return f"""Assessment(id={self.db_id}, 
                    module={self.module}, 
                    teacher={self.teacher}, 
                    student_group={self.student_group}, 
                    date={self.date}, 
                    file_path={self.file_path})"""
    
    @classmethod
    def create_tables(cls):
        """
        Creates the 'assessments' table in the database.
        """
        cls._cursor.execute("""CREATE TABLE IF NOT EXISTS assessments 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    module INTEGER,
                                    teacher INTEGER,
                                    student_group INTEGER,
                                    date DATE,
                                    file_path TEXT)""")
        cls._db.commit()

    @classmethod
    def read_all_objects_from_db(cls) -> list['Assessments']:
        """
        Reads all objects from the database and populates all the attributes.
        """
        result = list['Assessments']()
        cls._cursor.execute("SELECT * FROM assessments")
        rows = cls._cursor.fetchall()
        for row in rows:
            result.append(cls(db_id=row[0], 
                              module = Modules.read_data_from_db(row[1]),
                              teacher = Teachers.read_data_from_db(row[2]),
                              student_group = StudentGroups.read_data_from_db(row[3]),
                              date_data=row[4],
                              file_path=row[5]))
        return result
    
    @classmethod
    def check_if_exists_in_db(cls, db_id) -> bool:
        """
        Checks if the object exists in the database.
        """
        cls._cursor.execute("SELECT * FROM assessments WHERE id = :id", {"id": db_id})
        row = cls._cursor.fetchone()
        return not row is None
            
    def read_data_from_db(self) -> None:
        """
        Reads an object from the database by the 'db_id' and populates all attributes.
        """
        self._cursor.execute("SELECT * FROM assessments WHERE id = :id", {"id": self.db_id})
        row = self._cursor.fetchone()
        if not row is None:
            self.module = Modules(row[1])
            self.teacher = Teachers(row[2])
            self.student_group = StudentGroups(row[3])
            self.date = row[4]
            self.file_path = row[5]

    def save_object_to_db(self) -> None:
        """
        Saves an object to the database.
        """
        self._cursor.execute("INSERT INTO assessments VALUES (:id, :module, :teacher, :student_group, :date, :file_path)",
            {"id": self.db_id,
            "module": self.module.db_id,
            "teacher": self.teacher.db_id,
            "student_group": self.student_group.db_id,
            "date": self.date,
            "file_path": self.file_path})
        self._db.commit()
    
    @classmethod
    def check_folder_registered(cls, folder_path: str) -> bool:
        """
        Checks if the folder is registered in the list of assessments.
        """
        return any(assessment.file_path == folder_path for assessment in cls.__cache.values())
        