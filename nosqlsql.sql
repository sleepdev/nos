CREATE DATABASE nosqlsql;
CREATE USER "nosqlsql" IDENTIFIED BY "nosqlsql";
GRANT ALL ON nosqlsql.* TO "nosqlsql"@"localhost" IDENTIFIED BY "nosqlsql";

USE nosqlsql;
SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8" COLLATE "utf8_bin";


-- all objects are allocated on the heap, for simplicity
CREATE TABLE heap (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type ENUM('Void', 'Boolean', 'Integer','Float','String','List','Map','Object') NOT NULL
);
-- an index uniquely identifies an object on the heap
CREATE TABLE indx (
    indx VARBINARY(255) NOT NULL PRIMARY KEY,
    id INT NOT NULL    
);
-- object fields are relations between two objects on the heap
CREATE TABLE field (
    id INT NOT NULL,
    field VARBINARY(255) NOT NULL,
    value_id INT NOT NULL,
    PRIMARY KEY(id,field)
);

-- primitive types are not unique within the database
CREATE TABLE term_Bool (
    id INT NOT NULL PRIMARY KEY,
    value TINYINT(1) NOT NULL
);
CREATE TABLE term_Integer (
    id INT NOT NULL PRIMARY KEY,
    value BIGINT NOT NULL
);
CREATE TABLE term_Float (
    id INT NOT NULL PRIMARY KEY,
    value DOUBLE NOT NULL
);
CREATE TABLE term_String (
    id INT NOT NULL PRIMARY KEY,
    value TEXT NOT NULL
);

-- complex types are integrated into the database
CREATE TABLE term_List (
    id INT NOT NULL,
    i INT NOT NULL,
    value_id INT NOT NULL,
    PRIMARY KEY(id,i)
);
CREATE TABLE term_Map (
    id INT NOT NULL,
    key_hash INT NOT NULL,
    bucket INT NOT NULL,
    value_id INT NOT NULL,
    PRIMARY KEY(id,key_hash,bucket)
);

-- objects will look for a model to wrap themselves in
CREATE TABLE term_Object (
    id INT NOT NULL PRIMARY KEY,
    model VARBINARY(255) NOT NULL
);





