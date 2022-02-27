SELECT DISTINCT Outcomes.battle
FROM Outcomes
INNER JOIN Ships
ON Outcomes.ship = Ships.name
WHERE Ships.class = 'Kongo'
