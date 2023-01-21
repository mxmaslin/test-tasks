CREATE TABLE IF NOT EXISTS "basemodel" ("id" SERIAL NOT NULL PRIMARY KEY); 
CREATE TABLE IF NOT EXISTS "user" ("id" SERIAL NOT NULL PRIMARY KEY, "email" VARCHAR(255) NOT NULL, "disabled" BOOLEAN DEFAULT FALSE, "password_hash" VARCHAR(255) NOT NULL); 
CREATE TABLE IF NOT EXISTS "like" ("id" SERIAL NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "post_id" INTEGER NOT NULL); 
CREATE TABLE IF NOT EXISTS "post" ("id" SERIAL NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "title" VARCHAR(255) NOT NULL, "content" TEXT NOT NULL); 
CREATE TABLE IF NOT EXISTS "dislike" ("id" SERIAL NOT NULL PRIMARY KEY, "user_id" INTEGER NOT NULL, "post_id" INTEGER NOT NULL); 

ALTER TABLE "post" ADD CONSTRAINT "fk_post_user_id_refs_user" FOREIGN KEY ("user_id") REFERENCES "user" ("id"); 
ALTER TABLE "like" ADD CONSTRAINT "fk_like_user_id_refs_user" FOREIGN KEY ("user_id") REFERENCES "user" ("id"); 
ALTER TABLE "like" ADD CONSTRAINT "fk_like_post_id_refs_post" FOREIGN KEY ("post_id") REFERENCES "post" ("id"); 
ALTER TABLE "dislike" ADD CONSTRAINT "fk_dislike_user_id_refs_user" FOREIGN KEY ("user_id") REFERENCES "user" ("id"); 
ALTER TABLE "dislike" ADD CONSTRAINT "fk_dislike_post_id_refs_post" FOREIGN KEY ("post_id") REFERENCES "post" ("id"); 

CREATE UNIQUE INDEX IF NOT EXISTS "user_email" ON "user" ("email"); 
CREATE INDEX IF NOT EXISTS "post_user_id" ON "post" ("user_id"); 
CREATE INDEX IF NOT EXISTS "like_post_id" ON "like" ("post_id"); 
CREATE INDEX IF NOT EXISTS "like_user_id" ON "like" ("user_id"); 
CREATE INDEX IF NOT EXISTS "dislike_user_id" ON "dislike" ("user_id"); 
CREATE INDEX IF NOT EXISTS "dislike_post_id" ON "dislike" ("post_id");
