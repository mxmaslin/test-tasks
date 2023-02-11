CREATE TABLE users (
	id serial4 NOT NULL,
	user_id varchar(12) NOT NULL,
	"name" varchar(50) NOT NULL,
	surname varchar(50) NOT NULL,
	patronymic varchar(50) NULL,
	phone_number varchar(11) NOT NULL,
	email varchar NULL,
	country varchar(50) NOT NULL,
	date_created timestamp NOT NULL,
	date_modified timestamp NOT NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id),
	CONSTRAINT users_user_id_key UNIQUE (user_id)
);
CREATE UNIQUE INDEX ix_users_phone_number ON public.users USING btree (phone_number);