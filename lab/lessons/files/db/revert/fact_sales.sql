-- Revert data-pipeline-template:fact_sales from pg

BEGIN;

DROP TRIGGER load_sales ON load_sales;
DROP FUNCTION load_sales;
DROP VIEW load_sales;
DROP TABLE fact_sales;

COMMIT;
