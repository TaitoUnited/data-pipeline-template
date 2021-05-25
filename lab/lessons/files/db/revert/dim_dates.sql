-- Revert data-pipeline-template:dim_dates from pg

BEGIN;

DROP TABLE dim_dates;

COMMIT;
