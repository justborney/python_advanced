SELECT DISTINCT Product.maker, MAX(PC.price)
FROM Product
INNER JOIN PC
ON Product.model = PC.model
GROUP BY Product.maker
