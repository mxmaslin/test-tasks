CREATE DATABASE "test_social";

CREATE USER "test_social";

GRANT ALL PRIVILEGES ON DATABASE "test_social" to "test_social";

CREATE TABLE IF NOT EXISTS "users" ("id" SERIAL NOT NULL PRIMARY KEY, "email" VARCHAR(255) NOT NULL, "disabled" BOOLEAN DEFAULT FALSE, "password_hash" VARCHAR(255) NOT NULL);

CREATE TABLE IF NOT EXISTS "likes" ("id" SERIAL NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "post_id" INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS "posts" ("id" SERIAL NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "title" VARCHAR(255) NOT NULL, "content" TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS "dislikes" ("id" SERIAL NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "post_id" INTEGER NOT NULL);

ALTER TABLE "posts" ADD CONSTRAINT "fk_post_user_id_refs_user" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "likes" ADD CONSTRAINT "fk_like_user_id_refs_user" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "likes" ADD CONSTRAINT "fk_like_post_id_refs_post" FOREIGN KEY ("post_id") REFERENCES "posts" ("id");
ALTER TABLE "dislikes" ADD CONSTRAINT "fk_dislike_user_id_refs_user" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "dislikes" ADD CONSTRAINT "fk_dislike_post_id_refs_post" FOREIGN KEY ("post_id") REFERENCES "posts" ("id");

CREATE UNIQUE INDEX IF NOT EXISTS "user_email" ON "users" ("email");
CREATE INDEX IF NOT EXISTS "post_user_id" ON "posts" ("user_id");
CREATE INDEX IF NOT EXISTS "like_post_id" ON "likes" ("post_id");
CREATE INDEX IF NOT EXISTS "like_user_id" ON "likes" ("user_id");
CREATE INDEX IF NOT EXISTS "dislike_user_id" ON "dislikes" ("user_id");
CREATE INDEX IF NOT EXISTS "dislike_post_id" ON "dislikes" ("post_id");
