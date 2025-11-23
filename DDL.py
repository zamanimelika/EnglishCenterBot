import mysql.connector
from config import db_config

database_name = db_config['database']  


def drop_n_create_database(database_name):
    conn = mysql.connector.connect(
        user=db_config['user'], 
        password=db_config['password'], 
        host=db_config['host']
    )
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS {database_name} "
        f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f'database {database_name} created successfully')


def create_table_user():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name          VARCHAR(100),
            address       TEXT,
            phone         VARCHAR(100) NOT NULL,
            gender        ENUM('Male', 'Female', 'Other'),
            level         ENUM('Beginner', 'Intermediate', 'Advanced'),
            birth         DATE,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("user table created successfully.")


def create_table_teacher():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teacher (
            id              INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name            VARCHAR(100) NOT NULL,
            phone           VARCHAR(50) NOT NULL,
            email           VARCHAR(255) NOT NULL,
            status          ENUM('Active', 'Inactive', 'On Leave', 'Retired') DEFAULT 'Active',
            gender          ENUM('Male', 'Female', 'Other') DEFAULT 'Other',
            work_history    TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("teacher table created successfully.")


def create_table_course():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course (
            id              INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            title           VARCHAR(255) NOT NULL,
            description     TEXT,
            level           ENUM('Beginner', 'Intermediate', 'Advanced') DEFAULT 'Beginner',
            language        VARCHAR(50) DEFAULT 'English',
            start_date      DATE,
            end_date        DATE,
            fee             DECIMAL(10,2) DEFAULT 0.00,
            status          ENUM('Active', 'Inactive', 'Completed', 'Canceled') DEFAULT 'Active'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("course table created successfully.")


def create_table_register():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS register (
            id          INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_id     BIGINT UNSIGNED NOT NULL,
            course_id   INT UNSIGNED NOT NULL,
            date        DATETIME DEFAULT CURRENT_TIMESTAMP,
            status      ENUM('Pending', 'Confirmed', 'Cancelled', 'Completed') DEFAULT 'Pending',
            UNIQUE KEY(user_id, course_id),

            FOREIGN KEY (user_id) REFERENCES user(id)
                ON DELETE CASCADE ON UPDATE CASCADE,

            FOREIGN KEY (course_id) REFERENCES course(id)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("register table created successfully.")


def create_table_class_session():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS class_session (
            session_id  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            course_id   INT UNSIGNED NOT NULL,
            teacher_id  INT UNSIGNED,
            date        DATE NOT NULL,
            time        TIME NOT NULL,
            location    VARCHAR(255) DEFAULT 'Online',
            link        VARCHAR(255),

            FOREIGN KEY (course_id) REFERENCES course(id)
                ON DELETE CASCADE ON UPDATE CASCADE,

            FOREIGN KEY (teacher_id) REFERENCES teacher(id)
                ON DELETE SET NULL ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("class_session table created successfully.")


def create_table_resource():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resource (
            id          INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            course_id   INT UNSIGNED NOT NULL,
            title       VARCHAR(255) NOT NULL,
            type        ENUM('PDF', 'Book', 'Video') NOT NULL,

            FOREIGN KEY (course_id) REFERENCES course(id)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("resource table created successfully.")


def create_table_support_message():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS support_message (
            message_id  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_id     BIGINT UNSIGNED NOT NULL,
            text        TEXT NOT NULL,
            date        DATETIME DEFAULT CURRENT_TIMESTAMP,
            response    TEXT,

            FOREIGN KEY (user_id) REFERENCES user(id)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("support_message table created successfully.")


def create_table_tuition():

    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tuition (
            payment_id  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            register_id INT UNSIGNED NOT NULL,
            status      ENUM('Pending', 'Paid', 'Failed', 'Refunded') DEFAULT 'Pending',
            date        DATETIME DEFAULT CURRENT_TIMESTAMP,
            method      ENUM('Online', 'Cash', 'Card') NOT NULL DEFAULT 'Online',

            FOREIGN KEY (register_id) REFERENCES register(id)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("tuition table created successfully.")


if __name__ == "__main__":
    drop_n_create_database(database_name)
    create_table_user()
    create_table_teacher()
    create_table_course()
    create_table_register()
    create_table_class_session()
    create_table_resource()
    create_table_support_message()
    create_table_tuition()
