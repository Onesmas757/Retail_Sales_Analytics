CREATE TABLE customers (
    customer_id   TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment       TEXT NOT NULL
);

CREATE TABLE products (
    product_key  INTEGER PRIMARY KEY,
    product_id   TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    sub_category TEXT NOT NULL
);

CREATE TABLE orders (
    order_id    TEXT PRIMARY KEY,
    order_date  TEXT NOT NULL,
    ship_date   TEXT NOT NULL,
    ship_mode   TEXT,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    city        TEXT,
    state       TEXT,
    postal_code TEXT,
    region      TEXT
);

CREATE TABLE order_lines (
    row_id      INTEGER PRIMARY KEY,
    order_id    TEXT NOT NULL REFERENCES orders(order_id),
    product_key INTEGER NOT NULL REFERENCES products(product_key),
    sales       REAL NOT NULL,
    quantity    INTEGER NOT NULL,
    discount    REAL NOT NULL,
    profit      REAL NOT NULL
);