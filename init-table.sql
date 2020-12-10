DROP SCHEMA IF EXISTS inventory CASCADE;
CREATE SCHEMA rating;
SET search_path TO rating;

-- CREATE TABLE public.product_rating (
-- 	id varchar NULL,
-- 	product_name varchar NULL,
-- 	score INT NULL,
-- 	CONSTRAINT id_must_unique UNIQUE (id)
-- );


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

-- CREATE TABLE public.trips (
-- 	trip_id varchar NULL,
-- 	bus_code varchar NULL,
-- 	koridor varchar NULL,
-- 	"timestamp" timestamp NULL,
-- 	CONSTRAINT trips_unique UNIQUE (trip_id),
-- 	CONSTRAINT trips_buses_fk FOREIGN KEY (bus_code) REFERENCES public.buses(bus_code)
-- );