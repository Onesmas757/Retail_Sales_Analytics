-- ============================================================
-- Week 3: SQL analysis of the cleaned Superstore data (SQLite)
-- Tables: customers, products, orders, order_lines (see schema.sql)
-- Each query is labelled -- Q<number>: <business question>
-- ============================================================

-- Q1: What are the headline KPIs?
SELECT ROUND(SUM(ol.sales), 2)                                   AS total_sales,
       ROUND(SUM(ol.profit), 2)                                  AS total_profit,
       COUNT(DISTINCT ol.order_id)                               AS total_orders,
       COUNT(DISTINCT o.customer_id)                             AS total_customers,
       SUM(ol.quantity)                                          AS units_sold,
       ROUND(SUM(ol.profit) * 100.0 / SUM(ol.sales), 2)          AS profit_margin_pct,
       ROUND(SUM(ol.sales) / COUNT(DISTINCT ol.order_id), 2)     AS avg_order_value
FROM order_lines ol
JOIN orders o ON o.order_id = ol.order_id;

-- Q2: How do sales and profit change by year?
SELECT STRFTIME('%Y', o.order_date)                              AS year,
       ROUND(SUM(ol.sales), 2)                                   AS sales,
       ROUND(SUM(ol.profit), 2)                                  AS profit,
       COUNT(DISTINCT ol.order_id)                               AS orders
FROM order_lines ol
JOIN orders o ON o.order_id = ol.order_id
GROUP BY year
ORDER BY year;

-- Q3: Which five months had the highest sales?
SELECT STRFTIME('%Y-%m', o.order_date)                           AS year_month,
       ROUND(SUM(ol.sales), 2)                                   AS sales
FROM order_lines ol
JOIN orders o ON o.order_id = ol.order_id
GROUP BY year_month
ORDER BY sales DESC
LIMIT 5;

-- Q4: Which region performs best, and which earns the weakest margin?
SELECT o.region,
       ROUND(SUM(ol.sales), 2)                                   AS sales,
       ROUND(SUM(ol.profit), 2)                                  AS profit,
       COUNT(DISTINCT o.order_id)                                AS orders,
       ROUND(SUM(ol.profit) * 100.0 / SUM(ol.sales), 2)          AS margin_pct
FROM order_lines ol
JOIN orders o ON o.order_id = ol.order_id
GROUP BY o.region
ORDER BY sales DESC;

-- Q5: How do the three categories compare?
SELECT p.category,
       ROUND(SUM(ol.sales), 2)                                   AS sales,
       ROUND(SUM(ol.profit), 2)                                  AS profit,
       SUM(ol.quantity)                                          AS units,
       ROUND(SUM(ol.profit) * 100.0 / SUM(ol.sales), 2)          AS margin_pct
FROM order_lines ol
JOIN products p ON p.product_key = ol.product_key
GROUP BY p.category
ORDER BY sales DESC;

-- Q6: Which sub-categories lose money overall? (HAVING)
SELECT p.sub_category,
       ROUND(SUM(ol.sales), 2)                                   AS sales,
       ROUND(SUM(ol.profit), 2)                                  AS profit
FROM order_lines ol
JOIN products p ON p.product_key = ol.product_key
GROUP BY p.sub_category
HAVING SUM(ol.profit) < 0
ORDER BY profit;

-- Q7: What are the 10 best-selling products?
SELECT p.product_name,
       ROUND(SUM(ol.sales), 2)                                   AS sales,
       ROUND(SUM(ol.profit), 2)                                  AS profit
FROM order_lines ol
JOIN products p ON p.product_key = ol.product_key
GROUP BY p.product_name
ORDER BY sales DESC
LIMIT 10;

-- Q8: What are the 10 most profitable products?
SELECT p.product_name,
       ROUND(SUM(ol.profit), 2)                                  AS profit,
       ROUND(SUM(ol.sales), 2)                                   AS sales
FROM order_lines ol
JOIN products p ON p.product_key = ol.product_key
GROUP BY p.product_name
ORDER BY profit DESC
LIMIT 10;

-- Q9: Which 10 products lose the most money?
SELECT p.product_name,
       ROUND(SUM(ol.profit), 2)                                  AS profit,
       ROUND(SUM(ol.sales), 2)                                   AS sales,
       ROUND(AVG(ol.discount), 2)                                AS avg_discount
FROM order_lines ol
JOIN products p ON p.product_key = ol.product_key
GROUP BY p.product_name
ORDER BY profit ASC
LIMIT 10;

-- Q10: Who are the 10 customers with the highest sales?
SELECT c.customer_name,
       ROUND(SUM(ol.sales), 2)                                   AS sales,
       ROUND(SUM(ol.profit), 2)                                  AS profit,
       COUNT(DISTINCT o.order_id)                                AS orders
FROM order_lines ol
JOIN orders o    ON o.order_id = ol.order_id
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY sales DESC
LIMIT 10;

-- Q11: How does the size of the discount relate to profit? (CASE WHEN)
SELECT CASE WHEN discount = 0    THEN '1. No discount'
            WHEN discount <= 0.2 THEN '2. Up to 20%'
            WHEN discount <= 0.4 THEN '3. 21% to 40%'
            ELSE                      '4. Over 40%' END         AS discount_band,
       COUNT(*)                                                 AS order_lines,
       ROUND(SUM(sales), 2)                                     AS sales,
       ROUND(SUM(profit), 2)                                    AS profit
FROM order_lines
GROUP BY discount_band
ORDER BY discount_band;

-- Q12: Which customer segment is the most valuable?
SELECT c.segment,
       COUNT(DISTINCT c.customer_id)                            AS customers,
       ROUND(SUM(ol.sales), 2)                                  AS sales,
       ROUND(SUM(ol.profit), 2)                                 AS profit,
       ROUND(SUM(ol.sales) / COUNT(DISTINCT c.customer_id), 2)  AS sales_per_customer
FROM order_lines ol
JOIN orders o    ON o.order_id = ol.order_id
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.segment
ORDER BY sales DESC;

-- Q13: How many customers are loyal (10 or more orders)? (CTE + HAVING)
WITH orders_per_customer AS (
    SELECT customer_id, COUNT(*) AS n_orders
    FROM orders
    GROUP BY customer_id
)
SELECT COUNT(*)                                                 AS customers_with_10_plus_orders,
       (SELECT COUNT(*) FROM orders_per_customer)               AS all_customers,
       ROUND(AVG(n_orders), 1)                                  AS avg_orders_of_these
FROM orders_per_customer
WHERE n_orders >= 10;
