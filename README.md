Telegram Course Management Bot
مدیریت دوره‌های آموزشی با ربات تلگرام + MySQL

این پروژه یک ربات تلگرام برای مدیریت و نمایش دوره‌های آموزشی است.
ادمین می‌تواند دوره‌ها را اضافه، حذف، ویرایش یا مشاهده کند و کاربران می‌توانند لیست دوره‌ها را مشاهده کنند.

⭐️ امکانات ربات

پنل مدیریت کامل برای ادمین

افزودن دوره (عنوان، توضیحات، قیمت)

حذف دوره

مشاهده لیست دوره‌ها

ذخیره‌سازی در MySQL Database

طراحی شده با کتابخانه pyTelegramBotAPI

مدیریت ساده و قابل توسعه

پشتیبانی از پیام‌های دکمه‌ای (Inline Keyboard)

📁 ساختار پروژه
project/
│
├── bot.py                 # فایل اصلی ربات
├── database.py            # توابع دیتابیس
├── config.py              # تنظیمات API و دیتابیس
├── requirements.txt       # پکیج‌های مورد نیاز
└── README.md              # این فایل

🔧 نصب و راه‌اندازی
1️⃣ نصب کتابخانه‌ها
pip install -r requirements.txt


requirements.txt:

pyTelegramBotAPI
mysql-connector-python

2️⃣ ساخت دیتابیس

در MySQL اجرا کنید:

CREATE DATABASE coursebot CHARACTER SET utf8mb4;

USE coursebot;

CREATE TABLE course (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    description TEXT,
    fee INT
);

3️⃣ تنظیمات پروژه

فایل config.py را تنظیم کنید:

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ADMIN_CID = 123456789  # chat id admin

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DB_PASSWORD',
    'database': 'coursebot'
}

4️⃣ اجرای ربات
python bot.py

🧩 نحوه عملکرد ربات
👨‍💼 دستورات ادمین

ادمین با /admin وارد پنل می‌شود و گزینه‌های زیر را می‌بیند:

دکمه  توضیح
➕ افزودن دوره  ایجاد دوره جدید
📘 لیست دوره‌ها  نمایش همه دوره‌ها
❌ حذف دوره  انتخاب و حذف یک دوره
📝 ویرایش دوره  (قابل افزودن در نسخه بعد)
👤 دستورات کاربران

کاربران با /start پیام زیر را دریافت می‌کنند:

📘 دوره‌های موجود:

ID: 1 | Python Basic – 250,000 تومان
ID: 2 | Django Advanced – 480,000 تومان
...

🗄 API داخلی پروژه (Database)
گرفتن همه دوره‌ها
get_all_courses()

گرفتن یک دوره
get_course_data(course_id)

حذف دوره
delete_course(course_id)

📷 اسکرین‌شات (در صورت داشتن)

می‌توانید تصویر ربات را اینجا اضافه کنید:

![Bot Screenshot](images/screenshot.jpg)

📌 TODO – لیست توسعه‌های آینده

سیستم ویرایش دوره

مدیریت چند ادمین

افزودن عکس برای دوره‌ها

ساخت فرم خرید و پرداخت

ارسال پیام گروهی به کاربران

افزودن جستجو بین دوره‌ها

داشبورد تحت وب
