CREATE DATABASE IF NOT EXISTS farmed;

 CREATE TABLE IF NOT EXISTS user_details(id INTEGER PRIMARY KEY AUTO_INCREMENT, user_name VARCHAR(50), email VARCHAR(50) UNIQUE,user_password VARCHAR(50));
-- CREATE TABLE date_joined(date_id INTEGER PRIMARY KEY,date_joined VARCHAR(12), user_id INTEGER, FOREIGN KEY (user_id) REFERENCES user_details(id));
-- CREATE TABLE posts(post_id INTEGER PRIMARY KEY, post VARCHAR (500), user_id INTEGER, FOREIGN KEY(user_id) REFERENCES user_details(id));
-- CREATE TABLE feedbacks(id INTEGER PRIMARY KEY, feedback VARCHAR (500), user_id INTEGER, FOREIGN KEY (user_id) REFERENCES user_details(id))
