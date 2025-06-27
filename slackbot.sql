CREATE DATABASE IF NOT EXISTS slackbot;
USE slackbot;

CREATE TABLE IF NOT EXISTS preferences (
    user_id VARCHAR(50) PRIMARY KEY,
    wants_tips BOOLEAN NOT NULL
);
