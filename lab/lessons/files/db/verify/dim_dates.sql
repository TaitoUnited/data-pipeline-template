-- Verify data-pipeline-template:dim_dates on pg

BEGIN;

SELECT key FROM dim_dates LIMIT 1;

ROLLBACK;
