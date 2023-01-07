CREATE TABLE basemodel (
    id integer NOT NULL
);

CREATE SEQUENCE basemodel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE apartment (
    id integer NOT NULL,
    room_number integer NOT NULL
);

CREATE SEQUENCE apartment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE apartment_id_seq OWNED BY apartment.id;

ALTER SEQUENCE basemodel_id_seq OWNED BY basemodel.id;

CREATE TABLE booking (
    id integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    person_id integer NOT NULL,
    apartment_id integer NOT NULL
);

CREATE SEQUENCE booking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE booking_id_seq OWNED BY booking.id;

CREATE TABLE person (
    id integer NOT NULL,
    first_name character varying(255) NOT NULL,
    second_name character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL
);

CREATE SEQUENCE person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE person_id_seq OWNED BY person.id;

ALTER TABLE ONLY apartment ALTER COLUMN id SET DEFAULT nextval('apartment_id_seq'::regclass);

ALTER TABLE ONLY basemodel ALTER COLUMN id SET DEFAULT nextval('basemodel_id_seq'::regclass);

ALTER TABLE ONLY booking ALTER COLUMN id SET DEFAULT nextval('booking_id_seq'::regclass);

ALTER TABLE ONLY person ALTER COLUMN id SET DEFAULT nextval('person_id_seq'::regclass);

INSERT INTO apartment VALUES (1, 667);
INSERT INTO apartment VALUES (2, 669);

INSERT INTO booking VALUES (6, '2023-01-01', '2024-01-01', 4, 1);
INSERT INTO booking VALUES (7, '2023-01-01', '2024-01-01', 6, 1);
INSERT INTO booking VALUES (12, '2023-01-01', '2024-01-01', 4, 1);
INSERT INTO booking VALUES (13, '2021-01-01', '2022-01-01', 6, 2);

INSERT INTO person VALUES (4, 'Vava', 'Vovo', 'vovan', 'pbkdf2:sha256:260000$hwTOqJBAgQmWMNCg$f0f56146d0fa324f34c1613ec52711d87e628f4445df6b2964fb57f9a35f638f');
INSERT INTO person VALUES (6, 'Vava', 'Vovo', 'bibin', 'pbkdf2:sha256:260000$xDhJ1UrT4eGop4iC$e3a8bbdaa11c8430affa6e2241f678308f8e87069bde0204bb5105646d07b04a');

SELECT pg_catalog.setval('apartment_id_seq', 4, true);

SELECT pg_catalog.setval('basemodel_id_seq', 1, false);

SELECT pg_catalog.setval('booking_id_seq', 13, true);

SELECT pg_catalog.setval('person_id_seq', 7, true);

ALTER TABLE ONLY apartment
    ADD CONSTRAINT apartment_pkey PRIMARY KEY (id);

ALTER TABLE ONLY basemodel
    ADD CONSTRAINT basemodel_pkey PRIMARY KEY (id);

ALTER TABLE ONLY booking
    ADD CONSTRAINT booking_pkey PRIMARY KEY (id);

ALTER TABLE ONLY person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);

CREATE INDEX booking_apartment_id ON booking USING btree (apartment_id);

CREATE INDEX booking_person_id ON booking USING btree (person_id);

CREATE UNIQUE INDEX person_username ON person USING btree (username);

ALTER TABLE ONLY booking
    ADD CONSTRAINT fk_booking_apartment_id_refs_apartment FOREIGN KEY (apartment_id) REFERENCES apartment(id);

ALTER TABLE ONLY booking
    ADD CONSTRAINT fk_booking_person_id_refs_person FOREIGN KEY (person_id) REFERENCES person(id);
