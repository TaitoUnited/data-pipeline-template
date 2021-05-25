-- Deploy data-pipeline-template:dim_dates_generate to pg

BEGIN;

CREATE FUNCTION dim_dates_generate(date, date) RETURNS integer AS $$
DECLARE
    generated RECORD;
BEGIN
  FOR generated IN
    SELECT generate_series(
      $1, $2, interval '1' day
    ) as d
  LOOP
    INSERT INTO dim_dates (
      key, day, day_of_week, day_of_week_name, month, month_name, quarter, year, date
    ) values (
      to_char(generated.d, 'YYYY-MM-DD'),
      EXTRACT(DAY FROM generated.d),
      EXTRACT(DOW FROM generated.d),
      to_char(generated.d, 'Day'),
      EXTRACT(MONTH FROM generated.d),
      to_char(generated.d, 'Month'),
      EXTRACT(QUARTER FROM generated.d),
      EXTRACT(YEAR FROM generated.d),
      generated.d
    );
  END LOOP;
  RAISE NOTICE 'Done generating dim_dates.';
  RETURN 1;
END;
$$ LANGUAGE plpgsql;

COMMIT;
