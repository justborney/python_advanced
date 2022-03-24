SELECT full_name
FROM students
WHERE group_id = (
    SELECT group_id
    FROM students_groups
    WHERE teacher_id = (
        SELECT teacher_id
        FROM assignments
        WHERE assisgnment_id = (
            SELECT assisgnment_id
            FROM assignments_grades
            GROUP BY assisgnment_id
            ORDER BY avg(grade) DESC
    LIMIT 1
    )
    )
    )