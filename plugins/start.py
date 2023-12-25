from pyrogram import Client,filters
from pyrogram.types import Message,ReplyKeyboardMarkup,InlineKeyboardMarkup,ReplyKeyboardRemove,InlineKeyboardButton,CallbackQuery
from collections import defaultdict
from pyrogram.types import ChatPermissions
import json
from nowpayments import NOWPayments
import time
import random
import asyncio

#ایجاد دیکشنری دو لایه برای اطلاعات یوزر
def Tree():
    return defaultdict(Tree)
user_pocket = Tree()

#تابغ تغییر دیتابیس
def db_editor(jsonAddress,id,data,dataAfter):
    with open(jsonAddress , "r") as file:
        db = json.load(file)
    db[str(id)][data] = dataAfter
    with open(jsonAddress , "w") as file:
        json.dump(db,file,indent=4)

#تابع نمایش دیتابیس
def db_reader(jsonAddress,id,data):
    with open(jsonAddress , "r") as file:
        s = json.load(file)
        return s[str(id)][data]

#اضافه کننده دیتابیس
def db_adder(user_id,amount,wallet,status,code):
    with open("db/payments.json" , "r+") as file:
        db = json.load(file)
        db[str(user_id)][code] = {"amount" : amount ,"wallet" : wallet , "status" : status , "payed" : "no" }
        file.seek(0)
        json.dump(db,file,indent=4)

#گزینه /start و عضویت
@Client.on_message(filters.command("start"))
async def check_register(client: Client, message: Message):
    #اگر کاربر وجود داشت
    if str(message.from_user.id) in json.load(open("db/users.json", "r+")):
        await message.reply_text("Welcome to LOREM DOUBLER 🦁️ BOT To continue working,  you can use the following menu",reply_to_message_id=message.id,reply_markup=ReplyKeyboardMarkup(
            [["📎 REF‌‌‌‌E‌RAL‌‌‌ L‌I‌N‌‌K"],["📤WITHDRAWAL‌‌","📥DEPOSIT"],["📧DEPOSIT HISTORY","🧰BALANCE"],["👨🏻‍💻SUPPORT TEAM"]],resize_keyboard=True
        ))
        db_editor("db/users.json",message.from_user.id,"step","dashboard")

    #عضویت
    else:

        user_pocket[message.from_user.id]["is_register"] = True
        user_pocket[message.from_user.id]["step"] = "dashboard"
        user_pocket[message.from_user.id]["temp"] = ""
        user_pocket[message.from_user.id]["usd"] = 0
        user_pocket[message.from_user.id]["myrefs"] = 0
        user_pocket[message.from_user.id]["ref"] = 0
        user_pocket[message.from_user.id]["channel"] = False
        if message.text != "/start":
            user_pocket[message.from_user.id]["ref"] = int(message.text.split(" ")[1])
            db_editor("db/users.json",message.text.split(" ")[1],"usd",db_reader("db/users.json",message.text.split(" ")[1],"usd") + 0.05)
            await client.send_message(chat_id=message.text.split(" ")[1],text="✅A user has joined the bot through your invitation link.")
            await client.send_message(chat_id=message.text.split(" ")[1],text="✅0.05 USD have been deposited into your account. Congratulations!")
        else:
            user_pocket[message.from_user.id]["ref"] = 1291477413
        db_editor("db/users.json",message.text.split(" ")[1],"myrefs",db_reader("db/users.json",message.text.split(" ")[1],"myrefs") + 1)

        
        with open("db/users.json", "r+") as file:
            db_user = json.load(file)
            db_user[message.from_user.id] = user_pocket[message.from_user.id]
            file.seek(0)
            json.dump(db_user , file , indent=4)

        await message.reply_text("Welcome to LOREM DOUBLER 🦁️ BOT To continue working,  you can use the following menu",reply_to_message_id=message.id,reply_markup=ReplyKeyboardMarkup(
            [["📎 REF‌‌‌‌E‌RAL‌‌‌ L‌I‌N‌‌K"],["📤WITHDRAWAL‌‌","📥DEPOSIT"],["📧DEPOSIT HISTORY","🧰BALANCE"],["👨🏻‍💻SUPPORT TEAM"]],resize_keyboard=True
        ))
        

@Client.on_message(filters.text)
async def text_handler(client: Client, message: Message):
    if message.text == "📎 REF‌‌‌‌E‌RAL‌‌‌ L‌I‌N‌‌K":
        await client.send_photo(message.from_user.id,"AgACAgQAAxkBAAIxtWWJmxBDpAQJqDEVFM6lVVEtYIdKAAKbwjEbi4xRUEOyvptV9lZUAAgBAAMCAAN4AAceBA",
                                caption="What is LOREM DOUBLER?\n\nLOREM DOUBLER is the name of a margin trading robot that automatically trades using various analysis technologies in crypto and forex.\n\nBy investing in this robot, you can deposit your profits and transactions to this robot, and the robot will give you a daily profit, and you can claim your profit on a daily basis. (Unlimited)You can with the invitations of investors and marketing (without investment)\nReceive gifts.\n\nReceive a gift for each person equal to 20% of the amount invested by the person and 0.05 usd.!\n\nyour link for share:👇\nhttps://t.me/Ersalidebot?start=" + str(message.from_user.id))
        
    elif message.text == "📤WITHDRAWAL‌‌":
        await message.reply_text(text="**⚠️Minimum withdraw is 14 USDT.**",reply_to_message_id=message.id)
    elif message.text == "📧DEPOSIT HISTORY‌‌":
        await message.reply_text(text="**❗️You have no deposit**",reply_to_message_id=message.id)
    elif message.text == "🧰BALANCE":
        await message.reply_text("╔═══════════════════════╗\n"+
                                 "*Your account information*\n\n" + 
                                 "✍🏻 User Name : " +message.from_user.first_name + "\n\n" +
                                 "📟 ID: " + str(message.from_user.id) + "\n\n" +
                                 "🧰 balance : "+str(db_reader("db/users.json",message.from_user.id,"usd"))+" USDT\n\n"+
                                 "🙆🏻‍♂ Your referral : " + str(db_reader("db/users.json",message.from_user.id,"myrefs")) + "\n\n" +
                                 "")