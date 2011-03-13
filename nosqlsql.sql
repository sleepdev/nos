SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8" COLLATE "utf8_bin";

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    unique_identifier VARBINARY(255) NOT NULL UNIQUE,
    pwdhash BINARY(20)
);

CREATE TABLE user_data (
    user_id INT NOT NULL,
    _key VARBINARY(255) NOT NULL,
    _value VARBINARY(4294967295),
    PRIMARY KEY (user_id,_key)
);
