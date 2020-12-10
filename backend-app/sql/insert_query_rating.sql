
INSERT INTO rating.product_rating VALUES (default,'{product_name}','{score}') ON CONFLICT (id) DO NOTHING;