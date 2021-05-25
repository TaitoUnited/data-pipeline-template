-- Deploy data-pipeline-template:dim_products to pg

BEGIN;

CREATE TABLE dim_products (
  key text PRIMARY KEY,
  sku text NOT NULL,
  name text NOT NULL,
  category text NOT NULL,
  subcategory text NOT NULL
);

COMMIT;
