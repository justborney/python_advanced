SELECT full_name, avg(grade) AS avg_grade
FROM assignments_grades
INNER JOIN students s on s.student_id = assignments_grades.student_id
GROUP BY assignments_grades.student_id
ORDER BY avg_grade DESC
LIMIT 10;