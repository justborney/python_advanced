SELECT DISTINCT Product.maker from Product
INNER JOIN PC
ON Product.model = PC.model
WHERE PC.speed >= 450