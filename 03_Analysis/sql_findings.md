# Week 3: SQL Findings

Database: SQLite (`superstore.db`), built from `superstore_cleaned.csv`. Tables: customers, products, orders, order_lines (see `schema.sql`). All queries are in `queries.sql`.

## Q1: What are the headline KPIs?
*SQL concepts: JOIN, SUM, COUNT DISTINCT, ROUND*

The SQL result matches the Week 2 pandas result exactly: sales $2,296,919.49, profit $286,409.08, 5,009 orders, 793 customers, 37,871 units, a 12.47% margin and an average order value of $458.56. Two different tools giving the same numbers is a good check that both the cleaning and the database are correct.

## Q2: How do sales and profit change by year?
*SQL concepts: STRFTIME, GROUP BY, ORDER BY*

2017 was the best year (sales $733K, profit $93K, 1,687 orders). 2015 is the only year in which sales fell, yet profit still rose, from $49.6K to $61.6K.

## Q3: Which five months had the highest sales?
*SQL concepts: GROUP BY, ORDER BY DESC, LIMIT*

The five best months are November 2017 ($118.4K), December 2016 ($97.0K), September 2017 ($87.9K), December 2017 ($83.8K) and September 2014 ($81.8K). Every one falls in September, November or December, which confirms the seasonal pattern found in Week 2.

## Q4: Which region performs best, and which earns the weakest margin?
*SQL concepts: JOIN, GROUP BY, margin calculation*

West leads on sales ($725K) and profit ($108K) with the best margin (14.94%). Central has the weakest margin (7.92%). It sells more than South ($501K against $392K) but earns less profit ($39.7K against $46.7K).

## Q5: How do the three categories compare?
*SQL concepts: JOIN, GROUP BY, SUM*

Technology has the highest sales ($836K) and profit ($145K). Office Supplies sells by far the most units (22,906). Furniture has almost the same sales as Office Supplies but a margin of only 2.49%.

## Q6: Which sub-categories lose money overall?
*SQL concepts: HAVING (filters after grouping)*

Only three sub-categories lose money: Tables (-$17,725 on $206,966 of sales, a margin of about -8.6%), Bookcases (-$3,473) and Supplies (-$1,189). Tables is by far the largest problem, and two of the three are Furniture, which explains Furniture's thin margin.

## Q7: What are the 10 best-selling products?
*SQL concepts: JOIN, GROUP BY product name, ORDER BY, LIMIT*

The Canon imageCLASS 2200 Advanced Copier sells $61,600, more than double the number two product ($27,453). Of the ten best sellers, three lose money (Cisco TelePresence System EX90 -$1,811, GBC DocuBind P400 -$1,878, High Speed Automatic Electric Letter Opener -$262) and one breaks even. High sales do not guarantee profit.

## Q8: What are the 10 most profitable products?
*SQL concepts: JOIN, GROUP BY, ORDER BY, LIMIT*

The Canon imageCLASS 2200 Advanced Copier is also the most profitable product ($25,200), more than three times the number two (Fellowes PB500 binding machine, $7,753). The list is dominated by office technology equipment: copiers, printers, binding machines, a shredder and a headset system.

## Q9: Which 10 products lose the most money?
*SQL concepts: JOIN, GROUP BY, AVG, ORDER BY ASC*

The Cubify CubeX 3D Printer (double head) loses $8,880 at an average discount of 53%. Most of the worst products carry average discounts of 40% to 53%. Four of the ten are tables, which matches Q6. The Martin Yale electric letter opener loses $1,299 with only a 10% discount, so discounting is not the only cause; pricing or cost may also be wrong.

## Q10: Who are the 10 customers with the highest sales?
*SQL concepts: Multiple JOINs, GROUP BY, ORDER BY, LIMIT*

Sean Miller is the top customer by sales ($25,043) but the business lost $1,981 on his five orders. Tamara Chand ($19,052 in sales) delivered the highest profit of any customer ($8,981). The biggest buyer is not always the best customer.

## Q11: How does the size of the discount relate to profit?
*SQL concepts: CASE WHEN, GROUP BY on a calculated band*

Undiscounted lines earned $320,988 and lines with discounts up to 20% earned $100,785. Lines discounted 21% to 40% lost $35,805 and lines discounted over 40% lost $99,559. Every discount level above 20% loses money overall: 1,392 order lines lost about $135K in total. This is strong evidence for a discount cap.

## Q12: Which customer segment is the most valuable?
*SQL concepts: JOIN, GROUP BY, COUNT DISTINCT*

Consumer is the largest segment (409 customers, $1.16M, about half of all sales). Corporate has the highest sales per customer ($2,992), but the three segments are close ($2,840 to $2,992). The built-in segment label therefore explains little, which is why a behaviour-based segmentation is used in Part B.

## Q13: How many customers are loyal (10 or more orders)?
*SQL concepts: CTE (WITH), subquery, filtering on a calculated count*

88 of the 793 customers (11%) placed 10 or more orders, averaging 11 orders each over the four years. This small loyal group is worth protecting.
