CREATE USER 'eWaste_user'@'localhost' IDENTIFIED BY 'CSC3005';

CREATE DATABASE IF NOT EXISTS auth_eWaste;

GRANT ALL PRIVILEGES ON auth_eWaste.* TO 'eWaste_user'@'localhost';

USE auth_eWaste;

CREATE TABLE IF NOT EXISTS user (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	admin BOOLEAN NOT NULL DEFAULT false,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO user (email, username, password, admin) VALUES ('shunyaoteo99@gmail.com', 'Shun Yao', 'Admin123', true);
INSERT INTO user (email, username, password, admin) VALUES ('test@test.com', 'tester619', 'test', true);
INSERT INTO user (email, username, password) VALUES ('user1@user.com', 'user1', 'user1');
INSERT INTO user (email, username, password) VALUES ('user2@user.com', 'user2', 'user2');
INSERT INTO user (email, username, password) VALUES ('user3@user.com','user3', 'user3');