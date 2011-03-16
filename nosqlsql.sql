CREATE DATABASE nosqlsql;
CREATE USER nosqlsql IDENTIFIED BY nosqlsql;
GRANT ALL ON nosqlsql.* TO 'nosqlsql'@'localhost' IDENTIFIED BY 'nosqlsql';

USE nosqlsql;
SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8" COLLATE "utf8_bin";

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    unique_identifier VARBINARY(255) NOT NULL UNIQUE,
    pwdhash BINARY(20)
);

CREATE TABLE object (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type VARBINARY(255) NOT NULL,
    term_id INT,
    KEY (type)
);

CREATE TABLE term_int ();
CREATE TABLE term_str ();
CREATE TABLE term_float ();
CREATE TABLE term_list ();
CREATE TABLE term_dict ();

