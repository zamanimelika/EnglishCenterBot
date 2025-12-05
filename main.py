#!/usr/bin/python

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, BotCommand
from telebot.util import antiflood
import os
import time
import json
from datetime import datetime

from config import API_TOKEN, ADMIN_CID, ENGLISH_CHANNEL_CID, ENGLISH_CHANNEL_LINK, COURSES_CHANNEL_CID, COURSES_CHANNEL_LINK, ADMIN_PASSWORD, PROXY
from DML import insert_user, insert_teacher, insert_course, register_user, insert_support_message, insert_class_session, insert_resource, insert_tuition
from DQL_JSON import get_course_data, insert_course_data, insert_registration_data, get_all_courses, get_course_by_title, delete_course

os.makedirs("Data", exist_ok=True)


###############################
# SAVE TO FILE - FALLBACK
###############################
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
        
        print(f"✔️ Registration saved to file for user {user_id}")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False


bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')

# تنظیم پروکسی در apihelper اگر موجود باشد
if PROXY:
    import telebot.apihelper
    telebot.apihelper.proxy = PROXY

user_steps = {}
registration_cart = {}
known_users = []
authenticated_admins = {}  # {user_id: True/False}

hideboard = ReplyKeyboardRemove()


###############################
# REGISTER COMMANDS (ADDED)
###############################
bot_commands = [
    BotCommand("start", "👋 شروع ربات"),
    BotCommand("setting", "⚙️ تنظیمات مدیریت (ادمین)")
]
try:
    bot.set_my_commands(bot_commands)
except Exception as e:
    pass  # خاموش


###############################
# SAFE SEND
###############################
def send_message(*args, **kwargs):
    try:
        return antiflood(bot.send_message, *args, **kwargs)
    except:
        return None


###############################
# LISTENER
###############################
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(f"[{m.chat.id}] {m.from_user.first_name}: {m.text[:50]}")

bot.set_update_listener(listener)


###############################
# COURSE CAPTION
###############################
def gen_course_caption(data: dict):
    return f"""
📘 دوره: {data.get('title', data.get('NAME', ''))}
📄 توضیحات: {data.get('description', data.get('DESC', ''))}
💰 هزینه دوره: {data.get('fee', data.get('PRICE', 0))} تومان
"""


###############################
# BUTTON BELOW COURSE
###############################
def gen_course_keyboard(course_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📝 ثبت‌نام در دوره", callback_data=f"register_{course_id}"))
    return markup



###############################
# MAIN MENU
###############################
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🧾 مشاهده دوره‌ها", callback_data="show_courses"))
    markup.add(InlineKeyboardButton("📝 ثبت‌نام در دوره", callback_data="start_register"))
    markup.add(InlineKeyboardButton("📚 منابع آموزشی", callback_data="resources"))
    markup.add(InlineKeyboardButton("💬 پشتیبانی", callback_data="support"))
    return markup



###############################
# ADMIN MENU
###############################
def admin_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ افزودن دوره", callback_data="admin_add_course"))
    markup.add(InlineKeyboardButton("❌ حذف دوره", callback_data="admin_delete_course"))
    markup.add(InlineKeyboardButton("📋 لیست دوره‌ها", callback_data="admin_list_courses"))
    return markup


###############################
# START + HELP
###############################
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    cid = message.chat.id
    send_message(
        cid,
        "👋 سلام!\nبه ربات رسمی مؤسسه زبان خوش اومدی.\n\nاز منوی زیر گزینه‌ای را انتخاب کن:",
        reply_markup=main_menu()
    )


###############################
# ADMIN COMMANDS
###############################



@bot.message_handler(commands=['setting'])
def admin_setting(message):
    cid = message.chat.id
    
    # اگر قبلاً احراز هویت شده، صرفاً منوی ادمین را نشان بده
    if authenticated_admins.get(cid):
        send_message(cid, "⚙️ تنظیمات مدیریت:", reply_markup=admin_menu())
        return
    
    # در غیر این صورت، برای رمز عبور سؤال کن
    user_steps[cid] = "waiting_admin_password"
    send_message(cid, "🔐 لطفاً رمز عبور ادمین را وارد کنید:")


@bot.message_handler(func=lambda m: user_steps.get(m.chat.id) == "waiting_admin_password")
def check_admin_password(message):
    cid = message.chat.id
    password = message.text.strip()
    
    if password == ADMIN_PASSWORD:
        authenticated_admins[cid] = True
        user_steps.pop(cid, None)
        send_message(cid, "✅ احراز هویت موفق!", reply_markup=admin_menu())
    else:
        send_message(cid, "❌ رمز عبور نادرست است.")
        user_steps.pop(cid, None)



###############################
# ADMIN - ADD COURSE
###############################
@bot.callback_query_handler(func=lambda call: call.data == "admin_add_course")
def admin_add_course_click(call):
    cid = call.message.chat.id
    
    if not authenticated_admins.get(cid):
        send_message(cid, "⛔️ ابتدا احراز هویت کنید.")
        return

    send_message(cid,
        "📤 لطفاً *عکس دوره* را ارسال کنید.\n"
        "کپشن باید دقیقاً با این ساختار باشد:\n\n"
        "name: نام دوره\n"
        "desc: توضیحات دوره\n"
        "price: مبلغ دوره"
    )

    user_steps[cid] = "adding_course"



###############################
# PHOTO HANDLER FOR ADD COURSE
###############################
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    cid = message.chat.id

    if user_steps.get(cid) != "adding_course":
        return
    
    if cid != ADMIN_CID:
        send_message(cid, "⛔️ شما ادمین نیستید.")
        user_steps.pop(cid, None)
        return
        
    try:
        if not message.caption:
            send_message(cid, "❌ عکس باید کپشن داشته باشد. لطفاً دوباره سعی کنید.")
            return
            
        caption = message.caption.strip()
        lines = caption.split("\n")

        name = lines[0].split(":")[1].strip()
        desc = lines[1].split(":")[1].strip()
        price = int(lines[2].split(":")[1].strip())

        file_id = message.photo[-1].file_id

        course_id = insert_course_data(name, desc, price, file_id)
        
        if not course_id:
            send_message(cid, "❌ خطا در ذخیره دوره.")
            user_steps.pop(cid, None)
            return

        bot.send_photo(
            COURSES_CHANNEL_CID,
            file_id,
            caption=gen_course_caption({"title": name, "description": desc, "fee": price}),
            reply_markup=gen_course_keyboard(course_id)
        )

        send_message(cid, "✔ دوره با موفقیت ثبت و منتشر شد.")
        user_steps.pop(cid)

    except Exception as e:
        send_message(cid, f"❌ خطا: {str(e)}")



###############################
# ADMIN - LIST COURSES
###############################
@bot.callback_query_handler(func=lambda call: call.data == "admin_list_courses")
def admin_list_courses(call):
    cid = call.message.chat.id
    
    if not authenticated_admins.get(cid):
        send_message(cid, "⛔️ ابتدا احراز هویت کنید.")
        return

    courses = get_all_courses()

    if not courses:
        send_message(cid, "❗ هیچ دوره‌ای وجود ندارد.")
        return

    text = "📘 لیست دوره‌ها:\n\n"
    for c in courses:
        text += f"ID: {c['id']} | {c['title']} - {c['fee']} تومان\n"

    send_message(cid, text)



###############################
# ADMIN - DELETE COURSE
###############################
@bot.callback_query_handler(func=lambda call: call.data == "admin_delete_course")
def admin_delete_course(call):
    cid = call.message.chat.id
    
    if not authenticated_admins.get(cid):
        send_message(cid, "⛔️ ابتدا احراز هویت کنید.")
        return

    courses = get_all_courses()

    if not courses:
        send_message(cid, "❗ دوره‌ای برای حذف نیست.")
        return

    markup = InlineKeyboardMarkup()

    for c in courses:
        markup.add(InlineKeyboardButton(f"❌ حذف {c['title']}", callback_data=f"delete_course_{c['id']}"))

    send_message(cid, "یک دوره را برای حذف انتخاب کنید:", reply_markup=markup)



###############################
# ADMIN - DELETE CONFIRM
###############################
@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_course_"))
def delete_course_final(call):
    cid = call.message.chat.id
    
    if not authenticated_admins.get(cid):
        send_message(cid, "⛔️ ابتدا احراز هویت کنید.")
        return

    course_id = call.data.replace("delete_course_", "")

    result = delete_course(course_id)

    if result:
        send_message(cid, f"✔ دوره با موفقیت حذف شد.\nID: {course_id}")
    else:
        send_message(cid, "❌ خطا در حذف دوره.")



###############################
# CALLBACK HANDLER (USER)
###############################
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cid = call.message.chat.id
    data = call.data

    # ثبت‌نام مستقیم از دکمه دوره در کانال
    if data.startswith("register_") and not data.startswith("register_user"):
        course_id = data.replace("register_", "")
        try:
            course = get_course_data(int(course_id))
            if course:
                send_message(cid, 
                    f"✅ کد دوره کپی شد:\n\n"
                    f"<code>{course.get('title', course_id)}</code>\n\n"
                    f"اکنون می‌توانید برای ثبت‌نام /start را انتخاب کنید و 'ثبت‌نام در دوره' را بزنید."
                )
                return
        except:
            pass

    if data == "show_courses":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📘 ورود به کانال دوره‌ها", url=ENGLISH_CHANNEL_LINK))
        send_message(cid, "📚 لیست دوره‌ها در کانال زیر است:", reply_markup=markup)
        return


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
        send_message(cid, "📌 کد دوره را انتخاب کنید:", reply_markup=markup)
        return


    if data.startswith("select_code_"):
        code = data.replace("select_code_", "")
        registration_cart[cid] = {"course_code": code}

        user_steps[cid] = "waiting_fullname"

        send_message(cid, f"📝 دوره انتخاب‌شده: {code}\n\nلطفاً *نام کامل* را وارد کنید:")
        return


    if data == "go_to_payment":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💳 پرداخت", url="https://mylanguageclass.ir/payments"))
        markup.add(InlineKeyboardButton("✔ پرداخت انجام شد", callback_data="payment_done"))
        send_message(cid, "برای تکمیل ثبت‌نام، پرداخت شهریه لازم است:", reply_markup=markup)
        return


    if data == "payment_done":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🎓 جلسات کلاس", url="https://mylanguageclass.ir/login"))
        markup.add(InlineKeyboardButton("👨‍🏫 ارتباط با معلم", url="https://t.me/Teacherzaban45"))
        send_message(cid, "🎉 ثبت‌نام شما تکمیل شد!", reply_markup=markup)
        return


    if data == "resources":
        send_message(cid, "📚 منابع:\nOxford – SpeakOut – Duolingo")

    elif data == "support":
        send_message(cid, "💬 پشتیبانی:\n📞 021-445578\n📧 zabanenglish@gmail.ir")



###############################
# FULL NAME
###############################
@bot.message_handler(func=lambda m: user_steps.get(m.chat.id) == "waiting_fullname")
def receive_fullname(message):
    cid = message.chat.id
    registration_cart[cid]["full_name"] = message.text

    user_steps[cid] = "waiting_phone"
    send_message(cid, "📞 شماره تماس خود را وارد کنید:")



###############################
# PHONE + PAYMENT
###############################
@bot.message_handler(func=lambda m: user_steps.get(m.chat.id) == "waiting_phone")
def receive_phone(message):
    cid = message.chat.id
    phone = message.text.strip()
    registration_cart[cid]["phone"] = phone

    course_code = registration_cart[cid]["course_code"]
    result = insert_registration_data(cid, course_code, registration_cart[cid])

    if not result:
        save_registration_to_file(cid, course_code, registration_cart[cid])

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💳 پرداخت شهریه", callback_data="go_to_payment"))

    send_message(
        cid,
        f"نام: {registration_cart[cid]['full_name']}\n"
        f"شماره: {phone}\n"
        f"دوره: {course_code}\n\n"
        "برای ادامه، پرداخت را انجام دهید:",
        reply_markup=markup
    )



###############################
# OTHER MESSAGES
###############################
@bot.message_handler(func=lambda m: True)
def echo(message):
    send_message(message.chat.id, "برای شروع از /start استفاده کنید 😊")



###############################
# BOT RUN
###############################
print("🤖 Language Institute Bot is running...")

try:
    bot.infinity_polling(skip_pending=True)
except KeyboardInterrupt:
    print("🛑 ربات متوقف شد.")
except Exception as e:
    print(f"❌ خطا: {str(e)[:50]}...")
    print("🔄 دوباره تلاش...")
    import time
    time.sleep(3)
