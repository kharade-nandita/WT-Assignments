CREATE DATABASE IF NOT EXISTS python_login_db;
USE python_login_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT IGNORE INTO users (username, password)
VALUES ('nandita', '1234');
