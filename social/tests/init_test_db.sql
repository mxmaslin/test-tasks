CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    disabled BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS likes (
    id SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

CREATE TABLE IF NOT EXISTS dislikes (
    id SERIAL NOT NULL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS user_email ON users (email);
CREATE INDEX IF NOT EXISTS post_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS like_post_id ON likes(post_id);
CREATE INDEX IF NOT EXISTS like_user_id ON likes(user_id);
CREATE INDEX IF NOT EXISTS dislike_user_id ON dislikes(user_id);
CREATE INDEX IF NOT EXISTS dislike_post_id ON dislikes (post_id);
