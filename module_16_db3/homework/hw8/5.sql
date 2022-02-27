SELECT ship AS name
FROM Outcomes
INNER JOIN Classes
ON Outcomes.ship = Classes.class
UNION
SELECT name
FROM Ships
INNER JOIN Classes
ON Ships.name = Classes.class