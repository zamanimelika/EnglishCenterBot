CREATE DATABASE class;
USE class;

-- 1. user
CREATE TABLE users (
    `id`        INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name`      VARCHAR(100),
    `email`     VARCHAR(255) NOT NULL,
    `address`   VARCHAR(255) DEFAULT 'Tehran',
    `phone`     VARCHAR(100) NOT NULL,
    `gender`    ENUM('Male', 'Female', 'Other'),
    `level`     ENUM('Beginner', 'Intermediate', 'Advanced'),
    `birth`     DATE
);

-- 2. teacher
CREATE TABLE teacher (
    `id`           INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name`         VARCHAR(100) NOT NULL,
    `phone`        VARCHAR(50) NOT NULL,
    `email`        VARCHAR(255) NOT NULL ,
    `status`       ENUM('Active', 'Inactive', 'On Leave', 'Retired') DEFAULT 'Active',
    `gender`       ENUM('Male', 'Female', 'Other') DEFAULT 'Other',
    `work_history` TEXT
);

-- 3. course
CREATE TABLE course (
    `id`          INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title`       VARCHAR(255) NOT NULL,
    `description` TEXT,
    `level`       ENUM('Beginner', 'Intermediate', 'Advanced') DEFAULT 'Beginner',
    `language`    VARCHAR(50) DEFAULT 'English',
    `start_date`  DATE,
    `end_date`    DATE,
    `fee`         DECIMAL(10,2) DEFAULT 0.00,
    `status`      ENUM('Active', 'Inactive', 'Completed', 'Canceled') DEFAULT 'Active'
);


-- 4. register 
CREATE TABLE register (
    `id`         INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id`    INT UNSIGNED NOT NULL,
    `course_id`  INT UNSIGNED NOT NULL,
    `date`       DATETIME DEFAULT CURRENT_TIMESTAMP,
    `status`     ENUM('Pending', 'Confirmed', 'Cancelled', 'Completed') DEFAULT 'Pending',
    UNIQUE KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 5. class_session 
CREATE TABLE class_session (
    `session_id`           INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `course_id`            INT UNSIGNED NOT NULL,
    `teacher_id`           INT UNSIGNED,
    `date`                 DATE NOT NULL,
    `time`                 TIME NOT NULL,
    `location`             VARCHAR(255) DEFAULT 'Online',
    `link`                 VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- 6.resource 
CREATE TABLE resource (
    `id`             INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `course_id`      INT UNSIGNED NOT NULL,
    `title`          VARCHAR(255) NOT NULL,
    `type`           ENUM('PDF', 'Book', 'Video') NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 7. support_message 
CREATE TABLE support_message (
    `message_id`          INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id`             INT UNSIGNED NOT NULL,
    `text`                TEXT NOT NULL,
    `date`                DATETIME DEFAULT CURRENT_TIMESTAMP,
    `response`            TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 8. tuition 
CREATE TABLE tuition (
    `payment_id`       INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `register_id`      INT UNSIGNED NOT NULL,
    `status`           ENUM('Pending', 'Paid', 'Failed', 'Refunded') DEFAULT 'Pending',
    `date`             DATETIME DEFAULT CURRENT_TIMESTAMP,
    `method`           ENUM('Online', 'Cash', 'Card') NOT NULL DEFAULT 'Online',
    FOREIGN KEY (register_id) REFERENCES register(id) ON DELETE CASCADE ON UPDATE CASCADE
);
