-- Verify data-pipeline-template:fact_sales on pg

BEGIN;

SELECT key FROM load_sales LIMIT 1;
SELECT key FROM fact_sales LIMIT 1;

ROLLBACK;
