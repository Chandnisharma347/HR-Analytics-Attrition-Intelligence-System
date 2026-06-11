alter table employees add column tenure_years int;

update employees
set tenure_years = extract(year from age(coalesce(exit_date, current_date), join_date));