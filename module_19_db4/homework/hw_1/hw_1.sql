SELECT full_name, min(avg_grade)
FROM (SELECT avg(grade) AS avg_grade
FROM assignments_grades
GROUP BY assisgnment_id)
    INNER JOIN assignments
        ON assisgnment_id
    INNER JOIN teachers
        ON teachers.teacher_id;