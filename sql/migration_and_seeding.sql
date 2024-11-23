-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS farmed;

-- Use the created database
USE farmed;

-- Create the user_details table if it does not exist
CREATE TABLE IF NOT EXISTS user_details (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    user_password VARCHAR(100),
    date_joined VARCHAR(50)
);

-- Create the posts table if it does not exist
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50),
    post VARCHAR(500),
    date_posted VARCHAR(50),
    user_id INTEGER,
    category VARCHAR(40),
    likes INT,
    myfile VARCHAR(1000),
    FOREIGN KEY (user_id) REFERENCES user_details(id)
);

-- Create the reply table if it does not exist
CREATE TABLE IF NOT EXISTS reply (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    reply VARCHAR(1000),
    post_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (post_id) REFERENCES posts(id),
    FOREIGN KEY (user_id) REFERENCES user_details(id)
);
