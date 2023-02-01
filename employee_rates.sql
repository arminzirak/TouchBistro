select employee_id,
       sum(GREATEST((extract(EPOCH from LEAST("end_time", '2022-04-17 17:00:00')-GREATEST("start_time", '2022-04-15 09:00:00')) / 3600), 0) * hourly_wage)
from employee_activity
where ("end_time" is not null or "start_time" >= '2022-04-14 21:00:00')
group by employee_id;

-- assumptions:
-- 1. Each employee_id refers to a unique employee and each employee has only one employee_id
-- 2. Datetime fields have no timezones