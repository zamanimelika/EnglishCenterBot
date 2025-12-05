import json
import os
from datetime import datetime

COURSES_FILE = "Data/courses.json"
REGISTRATIONS_FILE = "Data/registrations.json"

# ایجاد فایل اگر وجود نداشته باشد
os.makedirs("Data", exist_ok=True)


############################################################
# GET COURSE BY ID
############################################################

def get_course_data(course_id):
    try:
        courses = get_all_courses()
        for c in courses:
            if c.get('id') == int(course_id):
                return c
        return None
    except Exception as e:
        print(f"خطا در دریافت دوره: {e}")
        return None


############################################################
# GET ALL COURSES
############################################################

def get_all_courses():
    try:
        if os.path.exists(COURSES_FILE):
            with open(COURSES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if data else []
        return []
    except Exception as e:
        print(f"خطا در خواندن دوره‌ها: {e}")
        return []


############################################################
# GET COURSE BY TITLE
############################################################

def get_course_by_title(title):
    courses = get_all_courses()
    for c in courses:
        if c.get('title') == title:
            return c
    return None


############################################################
# INSERT COURSE (ADMIN PANEL)
############################################################

def insert_course_data(name, desc, price, file_id):
    try:
        courses = get_all_courses()
        
        course_id = len(courses) + 1
        
        new_course = {
            "id": course_id,
            "title": name,
            "description": desc,
            "fee": price,
            "file_id": file_id,
            "created_at": datetime.now().isoformat()
        }
        
        courses.append(new_course)
        
        with open(COURSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(courses, f, ensure_ascii=False, indent=2)
        
        print(f"✅ دوره ثبت شد - ID: {course_id}")
        return course_id
    except Exception as e:
        print(f"خطا در ذخیره دوره: {e}")
        return None


############################################################
# INSERT REGISTRATION
############################################################

def insert_registration_data(user_id, course_code, data):
    try:
        registrations = []
        
        if os.path.exists(REGISTRATIONS_FILE):
            with open(REGISTRATIONS_FILE, 'r', encoding='utf-8') as f:
                registrations = json.load(f)
        
        # یافتن دوره
        course = get_course_by_title(course_code)
        
        if not course:
            print(f"دوره '{course_code}' پیدا نشد")
            return None
        
        registration = {
            "id": len(registrations) + 1,
            "user_id": user_id,
            "course_id": course['id'],
            "course_title": course_code,
            "full_name": data.get("full_name", ""),
            "phone": data.get("phone", ""),
            "registered_at": datetime.now().isoformat()
        }
        
        registrations.append(registration)
        
        with open(REGISTRATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(registrations, f, ensure_ascii=False, indent=2)
        
        print(f"✅ ثبت‌نام کاربر {user_id} موفق")
        return registration['id']
    except Exception as e:
        print(f"خطا در ثبت‌نام: {e}")
        return None


############################################################
# DELETE COURSE
############################################################

def delete_course(course_id):
    try:
        course_id = int(course_id)
        courses = get_all_courses()
        
        # فیلتر کردن دوره
        courses = [c for c in courses if c.get('id') != course_id]
        
        with open(COURSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(courses, f, ensure_ascii=False, indent=2)
        
        print(f"✅ دوره {course_id} حذف شد")
        return True
    except Exception as e:
        print(f"خطا در حذف دوره: {e}")
        return False
