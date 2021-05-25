-- Revert data-pipeline-template:dim_products from pg

BEGIN;

DROP TABLE dim_products;

COMMIT;
