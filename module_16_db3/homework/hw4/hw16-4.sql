SELECT customer.full_name FROM customer
    LEFT JOIN "order"
    ON customer.customer_id = "order".customer_id
WHERE "order".customer_id IS NULL