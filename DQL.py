import mysql.connector
from config import db_config


############################################################
# GET COURSE BY ID
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
# GET ALL COURSES
############################################################

def get_all_courses():
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor(dictionary=True)
        SQL_QUERY = "SELECT * FROM course WHERE status='Active';"
        cur.execute(SQL_QUERY)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data if data else []
    except Exception as e:
        print(f"Database error in get_all_courses: {e}")
        return []


############################################################
# GET COURSE BY TITLE
############################################################

def get_course_by_title(title):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor(dictionary=True)
        SQL_QUERY = "SELECT * FROM course WHERE title=%s;"
        cur.execute(SQL_QUERY, (title,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data[0] if data else None
    except Exception as e:
        print(f"Database error in get_course_by_title: {e}")
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

def insert_registration_data(user_id, course_code, data):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        
        # اگر course_code string باشد، ابتدا آن را پیدا کنید
        if isinstance(course_code, str):
            course = get_course_by_title(course_code)
            if not course:
                print(f"Course not found: {course_code}")
                return None
            course_id = course['id']
        else:
            course_id = course_code
        
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
