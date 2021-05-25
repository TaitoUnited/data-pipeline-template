-- Verify data-pipeline-template:dim_dates_generate on pg

BEGIN;

SELECT 'dim_dates_generate'::regproc;

ROLLBACK;
