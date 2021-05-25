-- Verify data-pipeline-template:dim_products on pg

BEGIN;

SELECT key FROM dim_products LIMIT 1;

ROLLBACK;
