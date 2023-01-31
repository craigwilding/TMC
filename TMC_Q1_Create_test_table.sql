-- Table: test.contact_types

-- DROP TABLE IF EXISTS test.contact_types;

CREATE TABLE IF NOT EXISTS test.contact_types
(
    id integer NOT NULL,
    emailsubscribed_raw character varying(10) COLLATE pg_catalog."default",
    name character varying(30) COLLATE pg_catalog."default",
    CONSTRAINT contact_types_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS test.contact_types
    OWNER to postgres;