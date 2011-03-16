CREATE DATABASE nosqlsql;
CREATE USER "nosqlsql" IDENTIFIED BY "nosqlsql";
GRANT ALL ON nosqlsql.* TO "nosqlsql"@"localhost" IDENTIFIED BY "nosqlsql";

USE nosqlsql;
SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8" COLLATE "utf8_bin";



-- convenience for web programming
CREATE TABLE auth (
    unique_identifier VARBINARY(255) NOT NULL PRIMARY KEY,
    pwdhash BINARY(20) NOT NULL,
    user_id INT NOT NULL
);



-- a standard heap allocated term
-- value can be resolved in one simple call to db
CREATE TABLE term (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type VARBINARY(255) NOT NULL,
    term_bool TINYINT(1),
    term_int BIGINT,
    term_float DOUBLE,
    term_str LONGTEXT,
    KEY (type)
);
CREATE TABLE term_object (
    id INT NOT NULL,
    field VARBINARY(255) NOT NULL,
    value_id INT NOT NULL,
    PRIMARY KEY(id,field)
);
CREATE TABLE term_list (
    id INT NOT NULL,
    i INT NOT NULL,
    value_id INT NOT NULL,
    PRIMARY KEY(id,i)
);
CREATE TABLE term_dict (
    id INT NOT NULL,
    key_hash INT NOT NULL,
    bucket INT NOT NULL,
    value_id INT NOT NULL,
    PRIMARY KEY(id,key_hash,bucket)
);





