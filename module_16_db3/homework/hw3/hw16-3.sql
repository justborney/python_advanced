SELECT customer.full_name,
       manager.full_name,
       "order".purchase_amount, "order".date
FROM "order"
INNER JOIN
    customer
    ON "order".customer_id = customer.customer_id
INNER JOIN
    manager
ON "order".manager_id = manager.manager_id
