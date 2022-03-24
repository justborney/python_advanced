SELECT group_id,
       round(avg(counter), 3) AS average,
       max(counter) AS maximum,
       min(counter) AS minimum
FROM (
         SELECT COUNT(grade_id) AS counter, group_id
         FROM assignments_grades
                  INNER JOIN students s on s.student_id = assignments_grades.student_id
         WHERE grade_id IN (
             SELECT grade_id
             FROM assignments_grades
             WHERE assignments_grades.date > (
                 SELECT due_date
                 FROM assignments
                 WHERE assignments_grades.assisgnment_id = assignments.assisgnment_id
             )
         )
         GROUP BY assisgnment_id, group_id
     )
GROUP BY group_id