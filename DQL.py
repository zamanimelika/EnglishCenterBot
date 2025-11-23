import mysql.connector
from config import db_config


############################################################
# GET COURSE
############################################################

def get_course_data(course_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor(dictionary=True)
        SQL_QUERY = "SELECT * FROM course WHERE id=%s;"
        cur.execute(SQL_QUERY, (course_id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data[0] if data else None
    except Exception as e:
        print(f"Database error in get_course_data: {e}")
        return None


############################################################
# INSERT COURSE (ADMIN PANEL)
############################################################

def insert_course_data(name, desc, price, file_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        SQL = "INSERT INTO course (title, description, fee) VALUES (%s, %s, %s);"
        cur.execute(SQL, (name, desc, price))
        conn.commit()
        course_id = cur.lastrowid
        cur.close()
        conn.close()
        return course_id
    except Exception as e:
        print(f"Database error in insert_course_data: {e}")
        return None


############################################################
# INSERT REGISTRATION (USER REGISTER COURSE)
############################################################

def insert_registration_data(user_id, course_id, data):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        # بررسی اگر course_id string باشد (کد دوره)
        if isinstance(course_id, str):
            SQL = "INSERT INTO register (user_id, course_id) VALUES (%s, %s);"
            cur.execute(SQL, (user_id, 1))  # مقدار پیش‌فرض برای دوره نامشخص
        else:
            SQL = "INSERT INTO register (user_id, course_id) VALUES (%s, %s);"
            cur.execute(SQL, (user_id, course_id))
        conn.commit()
        reg_id = cur.lastrowid
        cur.close()
        conn.close()
        return reg_id
    except Exception as e:
        print(f"Database error in insert_registration_data: {e}")
        return None
