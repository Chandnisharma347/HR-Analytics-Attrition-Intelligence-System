import random
from faker import Faker
from datetime import date
import psycopg2
from psycopg2.extras import execute_values

fake = Faker()
fake.unique.clear()

# --------------------------------
# DATABASE CONNECTION
# --------------------------------
conn = psycopg2.connect(
    host="localhost",
    database="employee_lifecycle",
    user="postgres",
    password="xxxxxxxx"

)

cur = conn.cursor()

NUM_EMPLOYEES=5000


# --------------------------------
# CLEAN TABLES FOR RE-RUN
# --------------------------------
cur.execute("""
TRUNCATE attendance,
performance,
salary_history,
employees
RESTART IDENTITY CASCADE;
""")

conn.commit()


# --------------------------------
# MASTER DATA
# --------------------------------
departments=[
"HR","IT","Sales",
"Finance","Operations","Marketing"
]

roles=[
"Manager","Executive","Analyst",
"Associate","Lead","Intern"
]

locations=[
"Delhi","Mumbai","Bangalore",
"Noida","Hyderabad","Pune"
]

for d in departments:
    cur.execute("""
    INSERT INTO departments
    (department_name)
    VALUES(%s)
    ON CONFLICT DO NOTHING
    """,(d,))

for r in roles:
    cur.execute("""
    INSERT INTO job_roles
    (job_role_name)
    VALUES(%s)
    ON CONFLICT DO NOTHING
    """,(r,))

for l in locations:
    cur.execute("""
    INSERT INTO locations
    (location_name)
    VALUES(%s)
    ON CONFLICT DO NOTHING
    """,(l,))

conn.commit()



# --------------------------------
# EMPLOYEES
# --------------------------------
employee_rows=[]

for i in range(NUM_EMPLOYEES):

    join_year=random.choice(
        [2018,2019,2020,
         2021,2022,2023,2024]
    )

    join_date=fake.date_between(
        start_date=date(join_year,1,1),
        end_date=date(join_year,12,31)
    )

    salary=random.randint(
        20000,
        120000
    )

    dept_id=random.randint(1,6)

    # attrition probability
    if dept_id==3:
        attr_prob=.40
    elif dept_id==5:
        attr_prob=.35
    else:
        attr_prob=.20

    if salary<30000:
        attr_prob+=.20

    elif salary>90000:
        attr_prob-=.10

    attrition=(
        "Yes"
        if random.random()<attr_prob
        else "No"
    )

    if attrition=="Yes":
        exit_date=fake.date_between(
            start_date=join_date,
            end_date=date(2025,12,31)
        )
    else:
        exit_date=None

    employee_rows.append(
        (
            fake.name()[:60],
            f"employee{i}@company.com",
            str(
                random.randint(
                    6000000000,
                    9999999999
                )
            ),
            random.randint(22,55),
            random.choice(
                ["Male","Female"]
            ),
            dept_id,
            random.randint(1,6),
            random.randint(1,6),
            join_date,
            exit_date,
            attrition
        )
    )

execute_values(
cur,
"""
INSERT INTO employees
(
name,email,phone,
age,gender,
department_id,
job_role_id,
location_id,
join_date,
exit_date,
attrition
)
VALUES %s
""",
employee_rows
)

conn.commit()

print("Employees inserted")


# --------------------------------
# GET EMPLOYEE IDs
# --------------------------------
cur.execute("""
SELECT employee_id
FROM employees
ORDER BY employee_id
""")

employee_ids=[
r[0]
for r in cur.fetchall()
]


# --------------------------------
# ATTENDANCE
# --------------------------------
attendance_rows=[]

for emp in employee_ids:

    for year in range(2022,2026):
        for month in range(1,13):

            attendance_rows.append(
                (
                    emp,
                    date(year,month,1),
                    22,
                    random.randint(15,22)
                )
            )

execute_values(
cur,
"""
INSERT INTO attendance
(
employee_id,
month,
working_days,
present_days
)
VALUES %s
""",
attendance_rows
)

conn.commit()

print("Attendance inserted")


# --------------------------------
# PERFORMANCE
# --------------------------------
performance_rows=[]

for emp in employee_ids:

    for year in range(
        2021,
        2026
    ):

        r=random.random()

        if r<0.20:
            score=round(
                random.uniform(
                    4.2,5.0
                ),1
            )

        elif r<0.40:
            score=round(
                random.uniform(
                    1.5,2.5
                ),1
            )

        else:
            score=round(
                random.uniform(
                    2.6,4.1
                ),1
            )

        performance_rows.append(
            (
                emp,
                date(year,12,31),
                score
            )
        )

execute_values(
cur,
"""
INSERT INTO performance
(
employee_id,
review_date,
performance_score
)
VALUES %s
""",
performance_rows
)

conn.commit()

print("Performance inserted")


# --------------------------------
# SALARY HISTORY
# --------------------------------
salary_rows=[]

for emp in employee_ids:

    salary=random.randint(
        20000,
        50000
    )

    for year in range(
        2020,
        2026
    ):

        salary+=random.randint(
            3000,
            12000
        )

        salary_rows.append(
            (
                emp,
                salary,
                date(year,1,1)
            )
        )

execute_values(
cur,
"""
INSERT INTO salary_history
(
employee_id,
salary,
effective_from
)
VALUES %s
""",
salary_rows
)

conn.commit()

print("Salary history inserted")


# --------------------------------
# TENURE UPDATE
# --------------------------------
cur.execute("""
UPDATE employees
SET tenure_years=
ROUND(
EXTRACT(
EPOCH FROM AGE(
COALESCE(
exit_date,
DATE '2025-12-31'
),
join_date
)
)/(365.25*24*60*60),
2
);
""")

conn.commit()

cur.close()
conn.close()

print("🔥 5000 employee HR dataset created successfully!")