DROP SCHEMA IF EXISTS inventory CASCADE;
CREATE SCHEMA rating;
SET search_path TO rating;

CREATE TABLE rating.product_rating (
	id SERIAL NOT NULL PRIMARY KEY,
	clothing_id int NOT NULL,
	age int NOT NULL,
	title varchar NULL,
	review varchar NULL,
	rating int NOT NULL,
	recommended int NOT NULL,
	positive_feedback int NOT NULL,
	division varchar NOT NULL,
	department varchar NOT NULL,
	class_name varchar NOT NULL,
	CONSTRAINT id_must_unique UNIQUE (id)
);

ALTER SEQUENCE product_rating_id_seq RESTART WITH 101;
ALTER TABLE product_rating REPLICA IDENTITY FULL;

INSERT INTO product_rating
VALUES (default,767,33,NULL,'Absolutely wonderful - silky and sexy and comfortable',4,1,0,'Initmates','Intimate','Intimates');