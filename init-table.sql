DROP SCHEMA IF EXISTS inventory CASCADE;
CREATE SCHEMA rating;
SET search_path TO rating;

CREATE TABLE rating.product_rating (
	id SERIAL NOT NULL PRIMARY KEY,
	product_name varchar NULL,
	score FLOAT NULL,
	CONSTRAINT id_must_unique UNIQUE (id)
);

ALTER SEQUENCE product_rating_id_seq RESTART WITH 101;
ALTER TABLE product_rating REPLICA IDENTITY FULL;

INSERT INTO product_rating
VALUES (default,'scooter',3.14),
       (default,'car battery',8.1);