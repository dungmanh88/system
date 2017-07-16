CREATE DATABASE IF NOT EXISTS album;

USE album;

CREATE TABLE IF NOT EXISTS image(
  ima_name INT AUTO_INCREMENT PRIMARY KEY,
  img_description VARCHAR(30),
  img_size VARCHAR(30),
  img_type VARCHAR(30),
  img_data LONGBLOB
)
