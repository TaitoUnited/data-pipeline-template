-- Revert data-pipeline-template:dim_dates_generate from pg

BEGIN;

DROP FUNCTION dim_dates_generate;

COMMIT;
