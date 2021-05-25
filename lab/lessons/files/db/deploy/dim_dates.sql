-- Deploy data-pipeline-template:dim_dates to pg

BEGIN;

CREATE TABLE dim_dates (
  key text PRIMARY KEY,
  day integer NOT NULL,
  day_of_week integer NOT NULL,
  day_of_week_name text NOT NULL,
  month integer NOT NULL,
  month_name text NOT NULL,
  quarter integer NOT NULL,
  year integer NOT NULL,
  date timestamp NOT NULL
);

COMMIT;
