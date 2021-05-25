-- Deploy data-pipeline-template:fact_sales to pg

BEGIN;

CREATE TABLE fact_sales (
  key text PRIMARY KEY,
  date_key text NOT NULL REFERENCES dim_dates (key),
  store_key text NOT NULL REFERENCES dim_stores (key),
  product_key text NOT NULL REFERENCES dim_products (key),
  order_number text NOT NULL,
  quantity integer NOT NULL,
  price numeric(12,2) NOT NULL
);

CREATE VIEW load_sales AS SELECT * FROM fact_sales;

CREATE OR REPLACE FUNCTION load_sales() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO fact_sales VALUES (NEW.*)
  ON CONFLICT (key) DO
    UPDATE SET
      date_key = EXCLUDED.date_key,
      product_key = EXCLUDED.product_key,
      order_number = EXCLUDED.order_number,
      quantity = EXCLUDED.quantity,
      price = EXCLUDED.price;
  RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER load_sales
INSTEAD OF INSERT ON load_sales
FOR EACH ROW EXECUTE PROCEDURE load_sales();

COMMIT;
