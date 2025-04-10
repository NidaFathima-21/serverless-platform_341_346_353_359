CREATE DATABASE IF NOT EXISTS serverless_platform;

USE serverless_platform;

CREATE TABLE functions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    route VARCHAR(100) NOT NULL,
    language VARCHAR(50) NOT NULL,
    timeout INT DEFAULT 5
);
