#!/usr/bin/python

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telebot.util import antiflood
import os
import time
import json
from datetime import datetime

from config import API_TOKEN, ADMIN_CID, ENGLISH_CHANNEL_CID, ENGLISH_CHANNEL_LINK, COURSES_CHANNEL_CID, COURSES_CHANNEL_LINK
from DML import insert_user, insert_teacher, insert_course, register_user, insert_support_message, insert_class_session, insert_resource, insert_tuition
from DQL import get_course_data , insert_course_data , insert_registration_data

os.makedirs("Data", exist_ok=True)

# Fallback: Save to file if DB fails
def save_registration_to_file(user_id, course_id, data):
    try:
        filepath = "Data/registrations.json"
        registrations = []
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                registrations = json.load(f)
        
        registration = {
            "user_id": user_id,
            "course_id": str(course_id),
            "full_name": data.get("full_name", ""),
            "phone": data.get("phone", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        registrations.append(registration)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(registrations, f, ensure_ascii=False, indent=2)
        
        print(f"✔ Registration saved to file for user {user_id}")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

bot = telebot.TeleBot(API_TOKEN)

user_steps = {}
registration_cart = {}
known_users = []

hideboard = ReplyKeyboardRemove()

############################################################
# SAFE SEND
############################################################

def send_message(*args, **kwargs):
    try:
        return antiflood(bot.send_message, *args, **kwargs)
    except:
        return None


############################################################
# LISTENER
############################################################

def listener(messages):
    for m in messages:
        print(f"[{m.chat.id}]: {m.content_type} -> {m.text if m.content_type=='text' else ''}")

bot.set_update_listener(listener)


############################################################
# COURSE CAPTION
############################################################

def gen_course_caption(data: dict):
    return f"""
📘 دوره: {data['NAME']}
📄 توضیحات: {data['DESC']}
💰 هزینه دوره: {data['PRICE']} تومان
"""


############################################################
# BUTTON BELOW COURSE POST
############################################################

def gen_course_keyboard(course_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📝 ثبت‌نام در دوره", callback_data=f"register_{course_id}"))
    return markup


############################################################
# 🔥 MAIN MENU (اصلاح‌شده طبق درخواست)
############################################################

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🧾 مشاهده دوره‌ها", callback_data="show_courses"))
    markup.add(InlineKeyboardButton("📝 ثبت‌نام در دوره", callback_data="start_register"))
    markup.add(InlineKeyboardButton("📚 منابع آموزشی", callback_data="resources"))
    markup.add(InlineKeyboardButton("💬 پشتیبانی", callback_data="support"))
    return markup


############################################################
# START
############################################################

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    cid = message.chat.id
    send_message(
        cid,
        "👋 سلام!\nبه ربات رسمی مؤسسه زبان خوش اومدی.\n\nاز منوی زیر گزینه‌ای را انتخاب کن:",
        reply_markup=main_menu()
    )


############################################################
# ADMIN: ADD COURSE
############################################################

@bot.message_handler(commands=['add_course'])
def admin_add_course(message):
    cid = message.chat.id
    if cid != ADMIN_CID:
        send_message(cid, "⛔ شما ادمین نیستید.")
        return

    send_message(cid,
        "📤 لطفاً *عکس دوره* را ارسال کنید.\n"
        "کپشن باید دقیقاً با این ساختار باشد:\n\n"
        "name: نام دوره\n"
        "desc: توضیحات دوره\n"
        "price: مبلغ دوره"
    )

    user_steps[cid] = "adding_course"


############################################################
# PHOTO HANDLER FOR ADD COURSE
############################################################

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    cid = message.chat.id

    if user_steps.get(cid) == "adding_course" and cid == ADMIN_CID:
        try:
            caption = message.caption.strip()
            lines = caption.split("\n")

            name = lines[0].split(":")[1].strip()
            desc = lines[1].split(":")[1].strip()
            price = int(lines[2].split(":")[1].strip())

            file_id = message.photo[-1].file_id

            course_id = insert_course_data(name, desc, price, file_id)
            
            if not course_id:
                send_message(cid, "❌ خطا در ذخیره دوره. لطفاً دوباره تلاش کنید.")
                user_steps.pop(cid, None)
                return

            bot.send_photo(
                COURSES_CHANNEL_CID,
                file_id,
                caption=gen_course_caption({"NAME": name, "DESC": desc, "PRICE": price}),
                reply_markup=gen_course_keyboard(course_id)
            )

            send_message(cid, "✔ دوره با موفقیت ثبت و در کانال منتشر شد.")
            user_steps.pop(cid)

        except Exception as e:
            send_message(cid, f"❌ خطا در پردازش: {e}")


############################################################
# CALLBACK HANDLER (اصلاح شده)
############################################################

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cid = call.message.chat.id
    data = call.data

    ########################################################
    # 1) دکمه مشاهده دوره‌ها
    ########################################################
    if data == "show_courses":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📘 ورود به کانال دوره‌ها", url=ENGLISH_CHANNEL_LINK))
        send_message(cid, "📚 لیست دوره‌ها در کانال زیر قرار دارد:", reply_markup=markup)
        return

    ########################################################
    # 2) شروع فرآیند ثبت‌نام
    ########################################################
    if data == "start_register":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("A1", callback_data="select_code_A1"),
            InlineKeyboardButton("B2", callback_data="select_code_B2")
        )
        markup.add(
            InlineKeyboardButton("IELTS", callback_data="select_code_IELTS"),
            InlineKeyboardButton("TOEFL", callback_data="select_code_TOEFL")
        )
        send_message(cid, "📌 کد دوره موردنظر را انتخاب کنید:", reply_markup=markup)
        return

    ########################################################
    # 3) کد انتخاب شد → واردکردن نام
    ########################################################
    if data.startswith("select_code_"):
        code = data.replace("select_code_", "")
        registration_cart[cid] = {"course_code": code}

        user_steps[cid] = "waiting_fullname"

        send_message(cid, f"📝 دوره‌ی انتخاب‌شده: {code}\n\nلطفاً *نام کامل* خود را وارد کنید:")
        return

    ########################################################
    # 4) پرداخت شهریه بعد از شماره تلفن
    ########################################################
    if data == "go_to_payment":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💳 پرداخت شهریه", url="https://mylanguageclass.ir/payments"))
        markup.add(InlineKeyboardButton("✔ پرداخت انجام شد", callback_data="payment_done"))

        send_message(cid, "برای تکمیل ثبت‌نام، پرداخت شهریه لازم است:", reply_markup=markup)
        return

    ########################################################
    # 5) پس از پرداخت — پیام نهایی + دکمه‌های جلسات/معلم
    ########################################################
    if data == "payment_done":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🎓 مشاهده جلسات کلاس", url="https://mylanguageclass.ir/login"))
        markup.add(InlineKeyboardButton("👨‍🏫 ارتباط با معلم", url="https://t.me/Teacherzaban45"))

        send_message(cid, "🎉 ثبت‌نام شما با موفقیت تکمیل شد!\n\nاز دکمه‌های زیر استفاده کنید:", reply_markup=markup)
        return

    ########################################################
    # دکمه‌های ساده دیگر
    ########################################################
    if data == "resources":
        send_message(cid, "📚 منابع آموزشی:\nOxford – SpeakOut – Duolingo")
    elif data == "support":
        send_message(cid, "💬 پشتیبانی:\n📞 021-445578\n📧 zabanenglish@gmail.ir")


############################################################
# RECEIVE FULL NAME
############################################################

@bot.message_handler(func=lambda m: user_steps.get(m.chat.id) == "waiting_fullname")
def receive_fullname(message):
    cid = message.chat.id
    registration_cart[cid]["full_name"] = message.text

    user_steps[cid] = "waiting_phone"
    send_message(cid, "📞 شماره تماس خود را وارد کنید:")


############################################################
# RECEIVE PHONE → مرحله پرداخت
############################################################

@bot.message_handler(func=lambda m: user_steps.get(m.chat.id) == "waiting_phone")
def receive_phone(message):
    cid = message.chat.id
    phone = message.text.strip()
    registration_cart[cid]["phone"] = phone

    # ذخیره در دیتابیس یا فایل
    course_code = registration_cart[cid]["course_code"]
    result = insert_registration_data(cid, course_code, registration_cart[cid])

    if not result:
        save_registration_to_file(cid, course_code, registration_cart[cid])

    # رفتن به منوی پرداخت
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💳 پرداخت شهریه", callback_data="go_to_payment"))

    send_message(
        cid,
        f"نام: {registration_cart[cid]['full_name']}\n"
        f"شماره: {phone}\n"
        f"دوره: {course_code}\n\n"
        "برای ادامه، پرداخت شهریه را انجام دهید:",
        reply_markup=markup
    )


############################################################
# OTHER MESSAGES
############################################################

@bot.message_handler(func=lambda m: True)
def echo(message):
    send_message(message.chat.id, "برای شروع از /start استفاده کنید 😊")


############################################################

print("🤖 Language Institute Bot is running...")

try:
    bot.infinity_polling()
except Exception as e:
    print(f"❌ Error in polling: {e}")
    print("🔄 Bot will restart in 10 seconds...")
    time.sleep(10)
