DROP TABLE IF EXISTS posts;
CREATE TABLE IF NOT EXISTS `posts`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `url` VARCHAR(300),
    `datetime` VARCHAR(50),
    `title` VARCHAR(300),
    `type` VARCHAR(50),
    `content` JSON,
    PRIMARY KEY (id)
);