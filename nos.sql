SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "latin1" COLLATE "latin1_bin";


-- all objects are allocated on the heap, for simplicity
CREATE TABLE heap (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type ENUM('json','object') NOT NULL
);
-- an index uniquely identifies an object on the heap
CREATE TABLE indx (
    indx VARBINARY(767) NOT NULL PRIMARY KEY,
    id INT NOT NULL    
);

CREATE TABLE json (
    id INT NOT NULL PRIMARY KEY,
    js TEXT NOT NULL
);

CREATE TABLE obj_class (
    id INT NOT NULL PRIMARY KEY,
    klass VARBINARY(767) NOT NULL
);
CREATE TABLE obj_field (
    id INT NOT NULL,
    field VARBINARY(767) NOT NULL,
    value_id INT NOT NULL,
    PRIMARY KEY (id,field)
);




