CREATE DATABASE IF NOT EXISTS vcs_automat;
USE vcs_automat;

DROP TABLE IF EXISTS archive;
CREATE TABLE archive (
  id int unsigned NOT NULL AUTO_INCREMENT UNIQUE,
  uid varchar(255) NOT NULL,
  unixtime int unsigned NOT NULL,
  time varchar(255) NOT NULL,
  slot int NOT NULL,
  PRIMARY KEY (id)
);


DROP TABLE IF EXISTS stats;
CREATE TABLE stats (
  id int unsigned NOT NULL AUTO_INCREMENT UNIQUE,
  time int unsigned NOT NULL,
  slot int NOT NULL,
  PRIMARY KEY (id)
);


DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id int unsigned NOT NULL AUTO_INCREMENT UNIQUE,
  uid varchar(255) NOT NULL UNIQUE,
  credits int unsigned NOT NULL,
  rfid varchar(255) NOT NULL UNIQUE,
  tracking int NOT NULL DEFAULT 1,
  PRIMARY KEY (id)
);
LOCK TABLES users WRITE;
INSERT INTO users VALUES (1,'default',100,'000000',1);
UNLOCK TABLES;


DROP TABLE IF EXISTS nonces;
CREATE TABLE nonces (
    nonce varchar(255) NOT NULL UNIQUE,
    timestamp int unsigned NOT NULL,
    PRIMARY KEY (nonce)
);

DROP TABLE IF EXISTS settings;
CREATE TABLE settings (
    id int unsigned NOT NULL AUTO_INCREMENT UNIQUE,
    name varchar(255) NOT NULL UNIQUE,
    value varchar(255) NOT NULL,
    PRIMARY KEY (id)
);
LOCK TABLES settings WRITE;
INSERT INTO settings VALUES (1,'frontend_active','0'),(2,'api_active','0'),(3,'standard_credits','2'),(4,'reset_interval','7'),(5,'last_reset','0'),(6,'next_reset','0');
UNLOCK TABLES;

