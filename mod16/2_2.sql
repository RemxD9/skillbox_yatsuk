SELECT c.full_name
FROM customer c
EXCEPT
SELECT c.full_name
FROM customer c
INNER JOIN "order" o ON c.customer_id = o.customer_id;
