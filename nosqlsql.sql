CREATE DATABASE nosqlsql;
CREATE USER nosqlsql IDENTIFIED BY nosqlsql;
GRANT ALL ON nosqlsql.* TO 'nosqlsql'@'localhost' IDENTIFIED BY 'nosqlsql';

USE nosqlsql;
SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8" COLLATE "utf8_bin";


CREATE TABLE object (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type VARBINARY(255) NOT NULL,
    term_id INT,
    KEY (type)
);

CREATE TABLE term_int (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    value BIGINT NOT NULL
);
CREATE TABLE term_str (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    value VARBINARY(65535) NOT NULL
);
CREATE TABLE term_float (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    value DOUBLE NOT NULL
);
CREATE TABLE term_list (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    index INT NOT NULL,
    value_id INT NOT NULL,
    KEY(id,index)
);
CREATE TABLE term_dict (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    key_hash INT NOT NULL,
    bucket INT NOT NULL,
    value_id INT NOT NULL,
    KEY(id,key_hash,bucket)
);
CREATE TABLE term_user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    unique_identifier VARBINARY(255) NOT NULL UNIQUE,
    pwdhash BINARY(20)
);

