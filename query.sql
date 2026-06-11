DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS performance CASCADE;
DROP TABLE IF EXISTS salary_history CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS job_roles CASCADE;
DROP TABLE IF EXISTS locations CASCADE;


-- -----------------------------
-- MASTER TABLES
-- -----------------------------
CREATE TABLE departments (
department_id SERIAL PRIMARY KEY,
department_name VARCHAR(50) UNIQUE
);

CREATE TABLE job_roles (
job_role_id SERIAL PRIMARY KEY,
job_role_name VARCHAR(50) UNIQUE
);

CREATE TABLE locations (
location_id SERIAL PRIMARY KEY,
location_name VARCHAR(50) UNIQUE
);


-- -----------------------------
-- EMPLOYEES
-- -----------------------------
CREATE TABLE employees(
employee_id SERIAL PRIMARY KEY,
name VARCHAR(60),
email VARCHAR(100) UNIQUE,
phone VARCHAR(15),
age INT,
gender VARCHAR(10),

department_id INT REFERENCES departments(department_id),
job_role_id INT REFERENCES job_roles(job_role_id),
location_id INT REFERENCES locations(location_id),

join_date DATE,
exit_date DATE,

attrition VARCHAR(5),

tenure_years NUMERIC(5,2)
);


-- -----------------------------
-- ATTENDANCE
-- -----------------------------
CREATE TABLE attendance(
attendance_id SERIAL PRIMARY KEY,
employee_id INT REFERENCES employees(employee_id),
month DATE,
working_days INT,
present_days INT
);


-- -----------------------------
-- PERFORMANCE
-- -----------------------------
CREATE TABLE performance(
performance_id SERIAL PRIMARY KEY,
employee_id INT REFERENCES employees(employee_id),
review_date DATE,
performance_score NUMERIC(3,1)
);


-- -----------------------------
-- SALARY HISTORY
-- -----------------------------
CREATE TABLE salary_history(
salary_id SERIAL PRIMARY KEY,
employee_id INT REFERENCES employees(employee_id),
salary INT,
effective_from DATE
);