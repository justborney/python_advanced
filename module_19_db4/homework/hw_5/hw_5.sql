SELECT students.group_id,
       count(students.student_id) AS stud_amount,
       round(avg(grade), 3)       AS avg_grade,
       aaa
FROM students
         INNER JOIN assignments_grades ag
                    ON students.student_id = ag.student_id
         INNER JOIN
     (
         SELECT count(assisgnment_id) AS aaa
         FROM assignments_grades
                  INNER JOIN students
                             ON assignments_grades.student_id = students.student_id
         WHERE grade = 0
     )
group by group_id