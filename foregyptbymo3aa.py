#الملف مدفوع بس حبيت انزلة مجانا
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# ضع التوكن الخاص بك هنا
Token = "7918910288:AAGvu2OL6cq7NlBWZBTPvf_j4JMwG4zdKY8"
bot = telebot.TeleBot(Token, parse_mode="Markdown")

Owner = 7709706806
BayaTi = set()

user_data = {}
info_updated = {}  

start_spam_button = types.InlineKeyboardButton(text="بدء الإرسال", callback_data="start_spam")
view_accounts_button = types.InlineKeyboardButton(text="عرض حسابات", callback_data="view_accounts")
set_email_button = types.InlineKeyboardButton(text="تعيين ايميل شد", callback_data="set_email")
set_victim_email_button = types.InlineKeyboardButton(text="تعيين بريد الدعم", callback_data="set_victim_email")
set_message_subject_button = types.InlineKeyboardButton(text="تعيين موضوع", callback_data="set_message_subject")
set_message_button = types.InlineKeyboardButton(text="تعيين كليشة", callback_data="set_message")
set_send_count_button = types.InlineKeyboardButton(text="تعيين عدد إرسال", callback_data="set_send_count")
set_image_button = types.InlineKeyboardButton(text="تعيين صورة", callback_data="upload_image")
set_interval_button = types.InlineKeyboardButton(text="تعيين سليب", callback_data="set_interval")
clear_upload_image_button = types.InlineKeyboardButton(text="مسح صورة الرفع", callback_data="clear_upload_image")
view_info_button = types.InlineKeyboardButton(text="عرض معلوماتك", callback_data="view_info")
clear_info_button = types.InlineKeyboardButton(text="مسح معلوماتك", callback_data="clear_info")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if user_id in BayaTi:
        if user_id not in user_data:
            user_data[user_id] = {
                "accounts": [],
                "victim": [],
                "subject": None,
                "message_body": None,
                "number": None,
                "interval": 4,
                "image_data": None,
                "is_spamming": False,
                "messages_sent_count": 0,
                "messages_failed_count": 0,
                "last_message_id": None,
            }
        if user_id not in info_updated:
            info_updated[user_id] = False
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(start_spam_button)
        markup.add(view_accounts_button, set_email_button)
        markup.add(set_victim_email_button, set_message_subject_button)
        markup.add(set_message_button, set_send_count_button)
        markup.add(set_image_button, set_interval_button)
        markup.add(view_info_button, clear_upload_image_button)
        markup.add(clear_info_button)
        bot.reply_to(message, "مرحبا في بوت الرفع الخارجلي الخاص بـ لورد", reply_markup=markup)
    else:
        bot.reply_to(message, "*انتظر الموافقة من المالك، شكرٱ , @I2m_Lord*")
        request_approval(user_id, message.from_user.username)

def request_approval(user_id, username):
    key = InlineKeyboardMarkup(row_width=1)
    approve_button = InlineKeyboardButton(text="• موافقه •", callback_data=f"Done_{user_id}")
    reject_button = InlineKeyboardButton(text="• رفض الموافقة •", callback_data=f"Reject_{user_id}")
    key.add(approve_button, reject_button)
    bot.send_message(Owner, f'''*• لقد طلب أحدهم لاستخدام البوت؟ 
• هل تريد الموافقة عليه؟. 
- @{username} | {user_id}*''', reply_markup=key)

@bot.callback_query_handler(func=lambda call: call.data.startswith("Done_") or call.data.startswith("Reject_"))
def handle_approval(call):
    user_id = int(call.data.split('_')[1])
    if call.data.startswith('Done_'):
        BayaTi.add(user_id)
        bot.send_message(user_id, "*Done √ | تمت الموافقة عليك*")
        bot.send_message(Owner, "*DONE √*")
    elif call.data.startswith("Reject_"):
        bot.send_message(user_id, "*Sorry, Note aprv | لم تتم الموافقه عليك.*")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    if user_id not in BayaTi:
        bot.send_message(user_id, "لم يتم الموافقة عليك بعد.")
        return

    if call.data == "set_email":
        bot.send_message(user_id, "أرسل الايميل:رمز تطبيقات")
        bot.register_next_step_handler(call.message, set_email, user_id)

    elif call.data == "set_victim_email":
        bot.send_message(user_id, "أرسل إيميلات الضحايا مفصولة بفواصل")
        bot.register_next_step_handler(call.message, set_victim_email, user_id)

    elif call.data == "set_message_subject":
        bot.send_message(user_id, "أرسل موضوع الرسالة")
        bot.register_next_step_handler(call.message, set_message_subject, user_id)

    elif call.data == "set_message":
        bot.send_message(user_id, "أرسل الكليشة ")
        bot.register_next_step_handler(call.message, set_message, user_id)

    elif call.data == "set_send_count":
        bot.send_message(user_id, "أرسل عدد الرسائل ")
        bot.register_next_step_handler(call.message, set_send_count, user_id)

    elif call.data == "set_interval":
        bot.send_message(user_id, "ارسل الوقت بين رسالة ورسالة بثواني")
        bot.register_next_step_handler(call.message, set_interval, user_id)

    elif call.data == "start_spam":
        user_data[user_id]['is_spamming'] = True
        start_spam(user_id)

    elif call.data == "view_info":
        if info_updated.get(user_id, False):
            bot.send_message(user_id, "تم تحديث المعلومات.")
            info_updated[user_id] = False
        info_text = f"البريد الإلكتروني: {', '.join([account['email'] for account in user_data[user_id]['accounts']])}\nرمز التطبيقات: {', '.join([account['password'] for account in user_data[user_id]['accounts']])}\nموضوع الرسالة: {user_data[user_id]['subject']}\nالرسالة: {user_data[user_id]['message_body']}\nسليب الرسائل: {user_data[user_id]['interval']} ثانية\nعدد الرسائل: {user_data[user_id]['number']}\nمسار الصورة: {'تم رفع الصورة' if user_data[user_id]['image_data'] else 'لم يتم تعيين صورة'}"
        bot.send_message(user_id, info_text)

    elif call.data == "clear_info":
        clear_info(user_id)
        info_updated[user_id] = True
        bot.send_message(user_id, "تم مسح جميع المعلومات.")

    elif call.data == "clear_upload_image":
        clear_uploaded_image(user_id)
        info_updated[user_id] = True
        bot.send_message(user_id, "تم مسح صورة الرفع.")

    elif call.data == "upload_image":
        bot.send_message(user_id, "ارسل الصورة")
        bot.register_next_step_handler(call.message, upload_image, user_id)

    elif call.data == "view_accounts":
        if user_data[user_id]['accounts']:
            accounts_text = "\n".join([f"{account['email']} : {account['password']}" for account in user_data[user_id]['accounts']])
            bot.send_message(user_id, f"الحسابات الموجودة:\n{accounts_text}")
            bot.send_message(user_id, "لحذف حساب، أرسل /cler ايميل:باسورد")
        else:
            bot.send_message(user_id, "لا توجد حسابات مضافة حتى الآن.")

@bot.message_handler(commands=['cler'])
def delete_account(message):
    user_id = message.from_user.id
    if message.text.startswith('/cler '):
        try:
            email_password = message.text.split('/cler ')[1].split(':')
            if len(email_password) == 2:
                email = email_password[0].strip()
                password = email_password[1].strip()
                user_data[user_id]['accounts'] = [acc for acc in user_data[user_id]['accounts'] if not (acc['email'] == email and acc['password'] == password)]
                bot.reply_to(message, f"تم حذف الحساب بنجاح: {email}:{password}")
            else:
                bot.reply_to(message, "الرجاء إدخال الأمر بالصيغة الصحيحة: /cler ايميل:باسورد")
        except IndexError:
            bot.reply_to(message, "الرجاء إدخال الأمر بالصيغة الصحيحة: /cler ايميل:باسورد")

def set_email(message, user_id):
    email_password = message.text.split(":")
    if len(email_password) != 2:
        bot.send_message(user_id, "الرجاء إدخال البريد الإلكتروني وكلمة المرور للتطبيقات بالصيغة الصحيحة (البريد:كلمة المرور).")
        return
    email = email_password[0].strip()
    password = email_password[1].strip()
    user_data[user_id]['accounts'].append({'email': email, 'password': password})
    info_updated[user_id] = True  # Mark info as updated
    bot.send_message(user_id, f"تمت إضافة الحساب بنجاح: {email}:{password}")

def set_victim_email(message, user_id):
    victim_emails = message.text.split(',')
    user_data[user_id]['victim'] = [email.strip() for email in victim_emails]
    info_updated[user_id] = True  # Mark info as updated
    bot.send_message(user_id, f"تم تعيين ايميل الدعم: {', '.join(user_data[user_id]['victim'])}")

def set_message_subject(message, user_id):
    user_data[user_id]['subject'] = message.text
    info_updated[user_id] = True  # Mark info as updated
    bot.send_message(user_id, f"تم تعيين موضوع الرسالة: {message.text}")

def set_message(message, user_id):
    user_data[user_id]['message_body'] = message.text
    info_updated[user_id] = True  # Mark info as updated
    bot.send_message(user_id, "تم تعيين نص الرسالة بنجاح.")

def set_send_count(message, user_id):
    try:
        user_data[user_id]['number'] = int(message.text)
        info_updated[user_id] = True  # Mark info as updated
        bot.send_message(user_id, f"تم تعيين عدد الإرسال: {message.text}")
    except ValueError:
        bot.send_message(user_id, "يرجى إرسال رقم صحيح لعدد الإرسال.")

def set_interval(message, user_id):
    try:
        user_data[user_id]['interval'] = int(message.text)
        info_updated[user_id] = True  # Mark info as updated
        bot.send_message(user_id, f"تم تعيين سليب الرسائل إلى {message.text} ثانية.")
    except ValueError:
        bot.send_message(user_id, "يرجى إرسال رقم صحيح للسليب.")

def upload_image(message, user_id):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_data[user_id]['image_data'] = downloaded_file
        info_updated[user_id] = True  # Mark info as updated
        bot.send_message(user_id, "تم رفع الصورة بنجاح.")
    else:
        bot.send_message(user_id, "الرجاء إرسال صورة فقط.")

def start_spam(user_id):
    user_info = user_data[user_id]
    if not user_info['accounts'] or not user_info['victim'] or not user_info['subject'] or not user_info['message_body'] or not user_info['number'] or not user_info['interval']:
        bot.send_message(user_id, "الرجاء تعيين جميع المعلومات المطلوبة قبل البدء بالسبام.")
        return

    bot.send_message(user_id, "جارٍ بدء السبام...")

    attempt = 0
    max_attempts = 3
    successful_attempts = 0
    failed_attempts = 0
    while attempt < max_attempts:
        try:
            for i in range(user_info['number']):
                if not user_info['is_spamming']:
                    break

                for account in user_info['accounts']:
                    msg = MIMEMultipart()
                    msg['From'] = account['email']
                    msg['To'] = ", ".join(user_info['victim'])
                    msg['Subject'] = user_info['subject']
                    body = user_info['message_body']
                    msg.attach(MIMEText(body, 'plain'))

                    if user_info['image_data']:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(user_info['image_data'])
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
                        msg.attach(part)

                    text = msg.as_string()
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(account['email'], account['password'])
                    try:
                        server.sendmail(account['email'], user_info['victim'], text)
                        successful_attempts += 1
                    except smtplib.SMTPRecipientsRefused:
                        bot.send_message(user_id, f"تم حظر إيميل: {account['email']}.")
                        failed_attempts += 1
                        break
                    finally:
                        server.quit()

                    user_info['messages_sent_count'] += 1
                    if user_info['last_message_id']:
                        bot.edit_message_text(chat_id=user_id, message_id=user_info['last_message_id'], text=f"جار إرسال الرسائل...\nالمحاولات الناجحة: {successful_attempts} √ \nالمحاولات الفاشلة: {failed_attempts} × \nالايقاف /stop")
                    else:
                        sent_msg = bot.send_message(user_id, f"جار إرسال الرسائل...\nالمحاولات الناجحة: {successful_attempts} √ \nالمحاولات الفاشلة: {failed_attempts} × \nالايقاف /stop")
                        user_info['last_message_id'] = sent_msg.message_id

                    sleep(user_info['interval'])

            bot.send_message(user_id, "تم إرسال جميع الرسائل بنجاح\nادا لم يكتمل العدد في الارسال اضغط بدء الارسال مجددا")
            break
        except Exception as e:
            attempt += 1
            if attempt < max_attempts:
                bot.send_message(user_id, f"حدث خطأ أثناء الإرسال: {str(e)}. سيتم إعادة المحاولة ({attempt}/{max_attempts}).")
                sleep(5)  # انتظر قليلاً قبل إعادة المحاولة
            else:
                bot.send_message(user_id, f"فشلت جميع محاولات الإرسال: {str(e)}")
        finally:
            user_info['is_spamming'] = False
            user_info['image_data'] = None
            user_info['last_message_id'] = None

def clear_info(user_id):
    user_data[user_id] = {
        "accounts": [],
        "victim": [],
        "subject": None,
        "message_body": None,
        "number": None,
        "interval": 4,
        "image_data": None,
        "is_spamming": False,
        "messages_sent_count": 0,
        "messages_failed_count": 0,
        "last_message_id": None,
    }
    info_updated[user_id] = True  

def clear_uploaded_image(user_id):
    user_data[user_id]['image_data'] = None
    info_updated[user_id] = True  

@bot.message_handler(commands=['stop'])
def stop_spam(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id]['is_spamming']:
        user_data[user_id]['is_spamming'] = False
        bot.reply_to(message, "تم إيقاف الإرسال.")
    else:
        bot.reply_to(message, "لا يوجد شيء لإيقافه.")

bot.infinity_polling(none_stop=True)