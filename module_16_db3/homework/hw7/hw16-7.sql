SELECT customer.full_name,
       "order".order_no
FROM "order"
         INNER JOIN
     customer
     ON "order".customer_id = customer.customer_id
       WHERE "order".manager_id IS NULL
