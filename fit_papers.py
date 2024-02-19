# pylint: disable=line-too-long
# pylint: disable=trailing-whitespace

from typing import List, Tuple
from datetime import datetime
import os
import sqlite3
from  classes.courses import Courses
from  classes.modules import Modules
from  classes.assessments import Assessments
from  classes.student_groups import StudentGroups
from  classes.teachers import Teachers

CURRENT_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(CURRENT_DIR, 'db', 'papers.db')

def create_course():
    course_path = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
    course = Courses(file_path = course_path)
    course.save_object_to_db()
    return course

def scan_assessments(course):
    # first_level_dirs = [d for d in os.listdir(course.file_path) 
    #                     if os.path.isdir(os.path.join(course.file_path, d))]
    unregisteres_assessments_dirs: List[Tuple[str, str, str]] = []
    for d in os.listdir(course.file_path):
        if course.prefix in d and \
                os.path.isdir(os.path.join(course.file_path, d)):
            folder_path = os.path.join(course.file_path, d)
            if Assessments.check_folder_registered(folder_path):
                continue
            else:
                dir_path = os.path.join(course.file_path, d)
                dir_create_date = datetime.utcfromtimestamp(os.path.getctime(dir_path)).strftime('%Y-%m-%d')
                unregisteres_assessments_dirs.append((d, dir_path, dir_create_date))

    return unregisteres_assessments_dirs

def convert_dirs_to_assessments(dirs: List[Tuple[str, str, str]]) -> list[Assessments]:
    result = list[Assessments]()
    for dir_name, dir_path, dir_date in dirs:
        prefix, name = dir_name.split(' ', 1)
        assessment = Assessments(file_path = dir_path, date_data = dir_date)
        assessment.module = Modules.find_by_attribute('code', prefix)
        assessment.additional_data.update({'name': name})
        assessment.additional_data.update({'prefix': prefix})
        result.append(assessment)

    return result


def main():


    db = sqlite3.connect(DB_PATH)

    list_of_classes = [
        Courses,
        Modules,
        Assessments,
        StudentGroups,
        Teachers
    ]

    cur = db.cursor()

    for cls in list_of_classes:
        cls.setup_db(db, cur)
        cls.create_tables()

    for cls in list_of_classes:
        cls.read_all_objects_from_db()

    # print(Courses.read_all_objects_from_db())

    if Courses.check_if_exists_in_db(1):
        course = Courses(1)
    else:
        course = create_course()

    for cls in list_of_classes:
        cls.setup_course_path(course.file_path)
        
    unregisteres_assessments_dirs = scan_assessments(course)
    # print(unregisteres_assessments_dirs)
    new_assessments = convert_dirs_to_assessments(unregisteres_assessments_dirs)
    print(new_assessments)


    db.close()


if __name__ == "__main__":
    main()
