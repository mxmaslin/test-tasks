CREATE TABLE basemodel (
    id SERIAL PRIMARY KEY
);

CREATE TABLE mailing (
    id SERIAL PRIMARY KEY,
    start timestamp with time zone NOT NULL,
    "end" timestamp with time zone NOT NULL
);

CREATE TABLE mailingrecipient (
    id SERIAL PRIMARY KEY,
    mailing_id integer NOT NULL,
    recipient_id integer NOT NULL
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    sent_at timestamp with time zone,
    status integer NOT NULL,
    value text NOT NULL,
    recipient_id integer NOT NULL
);

CREATE TABLE messagemailing (
    id SERIAL PRIMARY KEY,
    message_id integer NOT NULL,
    mailing_id integer NOT NULL
);

CREATE TABLE recipient (
    id SERIAL PRIMARY KEY,
    phone_number character varying(30) NOT NULL,
    op_code character varying(30),
    tz character varying(255)
);

CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    value text NOT NULL
);

CREATE TABLE tagrecipient (
    id SERIAL PRIMARY KEY,
    tag_id integer NOT NULL,
    recipient_id integer NOT NULL
);

CREATE INDEX mailing_end ON mailing USING btree ("end");

CREATE INDEX mailing_start ON mailing USING btree (start);

CREATE INDEX mailing_start_end ON mailing USING btree (start, "end");

CREATE INDEX mailingrecipient_mailing_id ON mailingrecipient USING btree (mailing_id);

CREATE UNIQUE INDEX mailingrecipient_mailing_id_recipient_id ON mailingrecipient USING btree (mailing_id, recipient_id);

CREATE INDEX mailingrecipient_recipient_id ON mailingrecipient USING btree (recipient_id);

CREATE INDEX message_recipient_id ON message USING btree (recipient_id);

CREATE INDEX message_sent_at ON message USING btree (sent_at);

CREATE INDEX message_sent_at_status ON message USING btree (sent_at, status);

CREATE INDEX messagemailing_mailing_id ON messagemailing USING btree (mailing_id);

CREATE INDEX messagemailing_message_id ON messagemailing USING btree (message_id);

CREATE UNIQUE INDEX messagemailing_message_id_mailing_id ON messagemailing USING btree (message_id, mailing_id);

CREATE UNIQUE INDEX recipient_phone_number ON recipient USING btree (phone_number);

CREATE INDEX tag_value ON tag USING btree (value);

CREATE INDEX tagrecipient_recipient_id ON tagrecipient USING btree (recipient_id);

CREATE INDEX tagrecipient_tag_id ON tagrecipient USING btree (tag_id);

CREATE UNIQUE INDEX tagrecipient_tag_id_recipient_id ON tagrecipient USING btree (tag_id, recipient_id);

ALTER TABLE ONLY mailingrecipient
    ADD CONSTRAINT fk_mailingrecipient_mailing_id_refs_mailing FOREIGN KEY (mailing_id) REFERENCES mailing(id);

ALTER TABLE ONLY mailingrecipient
    ADD CONSTRAINT fk_mailingrecipient_recipient_id_refs_recipient FOREIGN KEY (recipient_id) REFERENCES recipient(id);

ALTER TABLE ONLY message
    ADD CONSTRAINT fk_message_recipient_id_refs_recipient FOREIGN KEY (recipient_id) REFERENCES recipient(id);

ALTER TABLE ONLY messagemailing
    ADD CONSTRAINT fk_messagemailing_mailing_id_refs_mailing FOREIGN KEY (mailing_id) REFERENCES mailing(id);

ALTER TABLE ONLY messagemailing
    ADD CONSTRAINT fk_messagemailing_message_id_refs_message FOREIGN KEY (message_id) REFERENCES message(id);

ALTER TABLE ONLY tagrecipient
    ADD CONSTRAINT fk_tagrecipient_recipient_id_refs_recipient FOREIGN KEY (recipient_id) REFERENCES recipient(id);

ALTER TABLE ONLY tagrecipient
    ADD CONSTRAINT fk_tagrecipient_tag_id_refs_tag FOREIGN KEY (tag_id) REFERENCES tag(id);
