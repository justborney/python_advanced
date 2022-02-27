SELECT "order".order_no,
       manager.full_name,
       customer.full_name
FROM "order"
INNER JOIN
    customer
    ON "order".customer_id = customer.customer_id
INNER JOIN
    manager
ON "order".manager_id = manager.manager_id
WHERE manager.city != customer.city
