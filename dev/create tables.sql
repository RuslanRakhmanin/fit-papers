CREATE TABLE courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name STRING,
  description STRING,
  file_path STRING
);

CREATE TABLE teachers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name STRING,
  signature BLOB
);

CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  name STRING
);

CREATE TABLE student_groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name STRING,
  description STRING  
);

CREATE TABLE students_in_groups (
  group_id INTEGER,
  student_id INTEGER,
  "date" date,
  FOREIGN KEY(group_id) REFERENCES student_groups(id),
  FOREIGN KEY(student_id) REFERENCES students(id),
  PRIMARY KEY (group_id, student_id)
) WITHOUT ROWID;

CREATE TABLE modules (
  id INTEGER PRIMARY KEY,
  code STRING,
  name STRING,
  description STRING
);

CREATE TABLE assessments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  module_id INTEGER,
  group_id INTEGER,
  teacher_id INTEGER,
  "date" date,
  file_path STRING,
  FOREIGN KEY(module_id) REFERENCES modules(id),
  FOREIGN KEY(group_id) REFERENCES student_groups(id),
  FOREIGN KEY(teacher_id) REFERENCES teachers(id)
);

CREATE TABLE marking_sheets (
  id INTEGER PRIMARY KEY,
  module_id INTEGER,
  FOREIGN KEY(module_id) REFERENCES modules(id)
);


CREATE TABLE marks (
  assessment_id INTEGER,
  marking_sheet_id INTEGER,
  task_id INTEGER,
  instructions STRING,
  max INTEGER,
  mark INTEGER,
  FOREIGN KEY(assessment_id) REFERENCES assessments(id),
  FOREIGN KEY(marking_sheet_id) REFERENCES marking_sheets(id),
  PRIMARY KEY (assessment_id, marking_sheet_id, task_id)
) WITHOUT ROWID;

CREATE TABLE assessment_raw (
  assessment_id INTEGER,
  student_id INTEGER,
  "date" DATETIME,
  FOREIGN KEY(assessment_id) REFERENCES assessments(id),
  FOREIGN KEY(student_id) REFERENCES students(id),
  PRIMARY KEY (assessment_id, student_id, "date")
);

CREATE TABLE assessment_graded (
  id INTEGER PRIMARY KEY,
  assessment_id INTEGER,
  student_id INTEGER,
  teacher_id INTEGER,
  total INTEGER,
  "date" DATETIME,
  FOREIGN KEY(assessment_id) REFERENCES assessments(id),
  FOREIGN KEY(student_id) REFERENCES students(id),
  FOREIGN KEY(teacher_id) REFERENCES teachers(id)
);

CREATE TABLE comments (
  id INTEGER PRIMARY KEY,
  table_name STRING,
  element_id INTEGER,
  "date" DATETIME,
  author_id INTEGER,
  text STRING,
  FOREIGN KEY(author_id) REFERENCES teachers(id)
);

CREATE TABLE files (
  id INTEGER PRIMARY KEY,
  table_name STRING,
  element_id INTEGER,
  file_path STRING
);