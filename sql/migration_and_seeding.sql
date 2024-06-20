CREATE DATABASE IF NOT EXISTS farmed;

CREATE DATABASE IF NOT EXISTS farmed;CREATE TABLE IF NOT EXISTS user_details(id INTEGER PRIMARY KEY AUTO_INCREMENT,user_name VARCHAR(50),email VARCHAR(50) UNIQUE,user_password  VARCHAR(100),date_joined VARCHAR(50));



CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTO_INCREMENT,title VARCHAR(50),post VARCHAR(500),date_posted VARCHAR(50),user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users_details(id));


CREATE TABLE IF NOT EXISTS reply(
       id INTEGER PRIMARY KEY AUTO_INCREMENT,
       reply VARCHAR(1000),
       post_id INTEGER,
       user_id INTEGER,
       FOREIGN KEY (post_id) REFERENCES posts(id),
       FOREIGN KEY (user_id) REFERENCES user_details(id))


CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY AUTO_INCREMENT,post_category VARCHAR(34));
INSERT INTO categories(post_category) VALUES('Dailyfarming'), ('Poultry'), ('Coffee'), ("Tea"),('MaizeFarming'),('Others');

ALTER TABLE posts
ADD CONSTRAINT
FOREIGN KEY (categories_id) REFERENCES categories(id);