import mysql.connector
from config import db_config


# ==============================
# INSERT USER
# ==============================
def insert_user(name, address=None, phone=None, gender=None, level=None, birth=None):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO user (name, address, phone, gender, level, birth)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cur.execute(SQL, (name, address, phone, gender, level, birth))
    conn.commit()
    cid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"user inserted with id: {cid}")
    return cid


# ==============================
# INSERT TEACHER
# ==============================
def insert_teacher(name, phone, email, status="Active", gender="Other", work_history=None):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO teacher (name, phone, email, status, gender, work_history)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cur.execute(SQL, (name, phone, email, status, gender, work_history))
    conn.commit()
    tid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"teacher inserted with id: {tid}")
    return tid


# ==============================
# INSERT COURSE
# ==============================
def insert_course(title, description=None, level="Beginner", language="English", start_date=None, end_date=None, fee=0, status="Active"):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO course (title, description, level, language, start_date, end_date, fee, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(SQL, (title, description, level, language, start_date, end_date, fee, status))
    conn.commit()
    cid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"course inserted with id: {cid}")
    return cid



# ==============================
# DELETE COURSE  (NEW)
# ==============================
def delete_course(course_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        SQL = "DELETE FROM course WHERE id = %s"
        cur.execute(SQL, (course_id,))

        conn.commit()

        cur.close()
        conn.close()

        print(f"course deleted with id: {course_id}")
        return True

    except Exception as e:
        print(f"Error deleting course: {e}")
        return False



# ==============================
# REGISTER USER TO COURSE
# ==============================
def register_user(user_id, course_id, status="Pending"):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO register (user_id, course_id, status)
        VALUES (%s, %s, %s);
    """
    cur.execute(SQL, (user_id, course_id, status))
    conn.commit()
    rid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"user {user_id} registered in course {course_id}")
    return rid



# ==============================
# INSERT CLASS SESSION
# ==============================
def insert_class_session(course_id, teacher_id=None, date=None, time=None, location="Online", link=None):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO class_session (course_id, teacher_id, date, time, location, link)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cur.execute(SQL, (course_id, teacher_id, date, time, location, link))
    conn.commit()
    sid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"class session inserted with id: {sid}")
    return sid



# ==============================
# INSERT RESOURCE
# ==============================
def insert_resource(course_id, title, type):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO resource (course_id, title, type)
        VALUES (%s, %s, %s);
    """
    cur.execute(SQL, (course_id, title, type))
    conn.commit()
    rid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"resource inserted with id: {rid}")
    return rid



# ==============================
# INSERT SUPPORT MESSAGE
# ==============================
def insert_support_message(user_id, text):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO support_message (user_id, text)
        VALUES (%s, %s);
    """
    cur.execute(SQL, (user_id, text))
    conn.commit()
    mid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"support message inserted with id: {mid}")
    return mid



# ==============================
# INSERT TUITION
# ==============================
def insert_tuition(register_id, method="Online", status="Pending"):
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    SQL = """
        INSERT INTO tuition (register_id, method, status)
        VALUES (%s, %s, %s);
    """
    cur.execute(SQL, (register_id, method, status))
    conn.commit()
    pid = cur.lastrowid
    cur.close()
    conn.close()
    print(f"payment inserted with id: {pid}")
    return pid




# ==============================
# TEST AREA
# ==============================
if __name__ == "__main__":

    u1 = insert_user("Ali Reza", phone="09000000000", gender="Male", level="Beginner")

    t1 = insert_teacher("Sara Moradi", "09120000000", "sara@email.com")

    c1 = insert_course("English A1", "Basic English course")

    r1 = register_user(u1, c1)

    insert_class_session(c1, teacher_id=t1, date="2025-02-01", time="15:00:00")

    insert_resource(c1, "Lesson 1 PDF", "PDF")

    insert_support_message(u1, "I need class schedule")

    insert_tuition(r1)

    delete_course(c1)     # Test deletion
