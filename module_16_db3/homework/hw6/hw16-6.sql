SELECT COUNT("order".order_no), customer.full_name FROM "order"
INNER JOIN customer
ON "order".customer_id = customer.customer_id
GROUP BY "order".customer_id