/* Query 1 - Query used for first insight */
SELECT f.title, c.name category, COUNT(*)
FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN film f
ON fc.film_id = f.film_id
JOIN inventory i
ON i.film_id = f.film_id
JOIN rental r
ON i.inventory_id = r.inventory_id
WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
GROUP BY 1, 2
ORDER BY 2, 1

/* Query 2 */
SELECT f.title, c.name category, f.rental_duration,
NTILE(4) OVER (ORDER BY f.rental_duration) AS standard_quartile
FROM category c
JOIN film_category fc
ON c.category_id = fc.category_id
JOIN film f
ON fc.film_id = f.film_id
WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')

/* Query 3 - Query used for second insight */
SELECT category, standard_quartile,
COUNT(*)
FROM
    (SELECT c.name category, f.rental_duration,
     NTILE(4) OVER (ORDER BY f.rental_duration) AS standard_quartile
     FROM category c
     JOIN film_category fc
     ON c.category_id = fc.category_id
     JOIN film f
     ON fc.film_id = f.film_id
     WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')) t1
GROUP BY category, standard_quartile
ORDER BY category, standard_quartile

/* Query 4 */
SELECT  DATE_PART('year', r.rental_date) AS year, 
DATE_PART('month', r.rental_date) AS month, 
store.store_id, COUNT(*) count_rentals
FROM store
JOIN staff
ON store.store_id = staff.store_id
JOIN rental r
ON r.staff_id = staff.staff_id
GROUP BY 1, 2, 3
ORDER BY count_rentals DESC

/* Query 5 - Query used for third insight */
WITH top10 AS (SELECT c.customer_id, SUM(p.amount) AS total_payments
FROM customer c
JOIN payment p
ON p.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_payments DESC
LIMIT 10)

SELECT DATE_TRUNC('month', payment_date) AS pay_mon, (first_name || ' ' || last_name) AS full_name, COUNT(p.amount) AS pay_countpermon, SUM(p.amount) AS pay_amount
FROM top10
JOIN customer c
ON top10.customer_id = c.customer_id
JOIN payment p
ON p.customer_id = c.customer_id
WHERE payment_date >= '2007-01-01' AND payment_date < '2008-01-01'
GROUP BY 1, 2
ORDER BY 2, 1

/* Query 6 - query used for fourth insight */
WITH top10 AS (SELECT c.customer_id, SUM(p.amount) AS total_payments
FROM customer c
JOIN payment p
ON p.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_payments DESC
LIMIT 10),

t2 AS (SELECT DATE_TRUNC('month', payment_date) AS pay_mon, (first_name || ' ' || last_name) AS full_name, 
SUM(p.amount) AS pay_amount
FROM top10
JOIN customer c
ON top10.customer_id = c.customer_id
JOIN payment p
ON p.customer_id = c.customer_id
WHERE payment_date >= '2007-01-01' AND payment_date < '2008-01-01'
GROUP BY 1, 2)

SELECT *, 
LAG(t2.pay_amount) OVER (PARTITION BY full_name ORDER BY t2.pay_amount) AS lag, 
(pay_amount - COALESCE(LAG(t2.pay_amount) OVER (PARTITION BY full_name ORDER BY t2.pay_mon), 0)) AS diff
FROM t2
ORDER BY diff DESC