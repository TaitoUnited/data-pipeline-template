-- Delete all old data

delete from fact_sales;
delete from dim_products;
delete from dim_dates;

-- Generate dates

SELECT dim_dates_generate(DATE '20210101', DATE '20211231');

-- Add some products

INSERT INTO dim_products (
  key, sku, name, category, subcategory
) values (
  '1-1',
  '1-1',
  'Gibson Les Paul Studio SB',
  'Guitars',
  'Electric guitars'
);

INSERT INTO dim_products (
  key, sku, name, category, subcategory
) values (
  '1-2',
  '1-2',
  'PRS Custom 24 Aqua',
  'Guitars',
  'Electric guitars'
);
