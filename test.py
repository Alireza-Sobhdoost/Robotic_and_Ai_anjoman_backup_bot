import logging  
from uuid import uuid4  
from typing import Final  
from Message import *


import requests  
from telegram import Update, InlineQueryResultArticle, InlineKeyboardButton, InlineKeyboardMarkup  , InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, InlineQueryHandler, \
    ConversationHandler, CallbackQueryHandler  
from os import remove  

TOKEN: Final = "6927513102:AAECGNdiBmEFHRhxK2AzS81J9agm1h3AZi0"


logging.basicConfig(  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO  
)  
# Set higher logging level for httpx to avoid all GET and POST requests being logged  
logging.getLogger("httpx").setLevel(logging.WARNING)  

logger = logging.getLogger(__name__)  

# Conversation states  
REQUEST, CAPTION = range(2)  

def orm_create (text , messageID , userID , tag , status):
    
    Message.create(Message(text , messageID , userID , tag , status))   

class Bot:  
    def __init__(self):  
        self.caption = {}  

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  
        """Sends a message with three inline buttons attached."""  
        keyboard = [  
            [  
                InlineKeyboardButton("ارتباط با دبیر", callback_data="1"),  
                InlineKeyboardButton("انتقادات و پیشنهادات", callback_data="4"),  

            ],  
            [  
                InlineKeyboardButton("ارتباط با رویداد ها", callback_data="3"),  
                InlineKeyboardButton("ارتباط با آموزش", callback_data="2"),  

            ],  
             [  
                InlineKeyboardButton("ارتباط با آزمون", callback_data="5"),   

            ], 
        ]  

        reply_markup = InlineKeyboardMarkup(keyboard)  

        await update.message.reply_text(  
            f"روز بخیر {update.effective_user.first_name}\nبه بات پشتیبانی انجمن رباتیک و هوش مصنوعی دانشگاه گیلان خوش آمدید\nچطور میتونم کمکتون کنم ؟",  
            reply_markup=reply_markup)  

        return REQUEST  # Transition to REQUEST state  

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
        global REQUEST
        """Parses the CallbackQuery and updates the message text."""  
        query = update.callback_query  
        await query.answer()  
        if query.data == "1":  
            await query.edit_message_text(text="مدیریت در خدمته !")  
            REQUEST = 1
            return CAPTION

        # Handle other button actions similarly if needed  
        if query.data == "2":
            keyboard = [
                [
                    InlineKeyboardButton("ثبت نام در دوره های آموزشی", callback_data="21")
                    
                ],
                [
                    InlineKeyboardButton("BP سوال خصوصی دوره", callback_data="22")
                    
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_reply_markup(reply_markup=reply_markup)
            await query.edit_message_text(
                text=f"درود\nآموزش در خدمته !",
                reply_markup=reply_markup)
            REQUEST = 2

            # return REQUEST

        if query.data == "3":
            keyboard = [
                [
                    InlineKeyboardButton("ثبت نام رویداد ", callback_data="31")
                    
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)
            await query.edit_message_text(
                text=f"درود \nبخش رویداد در خدمته !",
                reply_markup=reply_markup)
            REQUEST = 3
            # return CAPTION
            
        if query.data == "4":

            await query.edit_message_text(
                text=f"درود \nبی صبرانه منتظر دریافت انتقادات ونظراتتون هستیم")
            REQUEST = 4
            return CAPTION

        if query.data == "5":

            await query.edit_message_text(
                text=f"درود \nپشتیبانی آزمون در خدمته مشکلی پیش اومده ؟")
            REQUEST = 5
        if query.data == "21":
            await query.edit_message_text(
                text=f"درود\nآیا میخواید در دوره ای شرکت کنید ؟ تیم ما برای مشاوره و ثبت نام در خدمت شماست")
            
            REQUEST = 21
            return CAPTION

        if query.data == "22":
            await query.edit_message_text(
                text=f"درود\nسوالتون در راستای دوره مبانی عنوان کنید !\nاساتید ما در اسرع وقت به شما پاسخ خواهند داد")
            REQUEST = 22
            return CAPTION

        if query.data == "31":
            await query.edit_message_text(
                text=f"درود\nآیا میخواید در رویدادی شرکت کنید ؟ تیم ما برای مشاوره و ثبت نام در خدمت شماست")
            REQUEST = 31
            return CAPTION

            #  return CAPTION  # Transition to CAPTION state  
    

    async def caption_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
        """Handles the caption input from the user."""  
        self.caption[update.effective_chat.id] = update.message.text  
        global REQUEST

        # print()
        # m1 = Message(update.message.text, update.message.message_id, update.effective_chat.id, "دبیر", "active")
        # Message.create(m1)

        if REQUEST == 1:
            orm_create(update.message.text, update.message.message_id, update.effective_chat.id, "دبیر", "active")
            await context.bot.send_message(  
                text=f"{int(update.message.message_id)}\n{update.message.text}\n#دبیر\n#{update.effective_chat.id}",  
                chat_id= -4107388966,  
            ) 
            await context.bot.send_message(  
                text=f"پیام شما با موفقت برای تیم پشتیبانی ارسال شد",  
                chat_id= update.effective_chat.id,  
            ) 
        if REQUEST == 2 or REQUEST == 21 or REQUEST == 22:
            if REQUEST == 21:
                tag = "آموزش_ثبت_نام_دوره"
            elif REQUEST == 22 :
                tag = "آموزش_ابهام_در_دوره_BP"
            orm_create(update.message.text, update.message.message_id, update.effective_chat.id, tag, "active")
            await context.bot.send_message(  
                text=f"{int(update.message.message_id)}\n{update.message.text}\n#{tag}\n#{update.effective_chat.id}",  
                chat_id= -4107388966,  
            ) 
            await context.bot.send_message(  
                text=f"پیام شما با موفقت برای تیم پشتیبانی ارسال شد",  
                chat_id= update.effective_chat.id,  
            ) 
            

        if REQUEST == 3 or REQUEST == 31:
            tag = "رویداد_ثبت_نام_رویداد"
            orm_create(update.message.text, update.message.message_id, update.effective_chat.id, tag, "active")
            await context.bot.send_message(  
                text=f"{int(update.message.message_id)}\n{update.message.text}\n#{tag}\n#{update.effective_chat.id}",  
                chat_id= -4107388966,  
            ) 
            await context.bot.send_message(  
                text=f"پیام شما با موفقت برای تیم پشتیبانی ارسال شد",  
                chat_id= update.effective_chat.id,  
            ) 

        if REQUEST == 4:
            orm_create(update.message.text, update.message.message_id, update.effective_chat.id, "انتقادات_و_پیشنهادات", "active")
            await context.bot.send_message(  
                text=f"{int(update.message.message_id)}\n{update.message.text}\n#انتقادات_و_پیشنهادات\n#{update.effective_chat.id}",  
                chat_id= -4107388966,  
            ) 
            await context.bot.send_message(  
                text=f"پیام شما با موفقت برای تیم پشتیبانی ارسال شد",  
                chat_id= update.effective_chat.id,  
            ) 
    

        if REQUEST == 5:
            orm_create(update.message.text, update.message.message_id, update.effective_chat.id, "ارتباط_با_آزمون" , "active")
            await context.bot.send_message(  
            text=f"{int(update.message.message_id)}\n{update.message.text}\n#ارتباط_با_آزمون\n#{update.effective_chat.id}",  
            chat_id= -4107388966,  
            ) 
            await context.bot.send_message(  
            text=f"پیام شما با موفقت برای تیم پشتیبانی ارسال شد",  
            chat_id= update.effective_chat.id,  
            ) 
        REQUEST = 0
        
        return ConversationHandler.END  # End the conversation, or change this if you expect to stay in conversation  

    async def cancel_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
        """Handles the cancellation of the conversation."""  
        await context.bot.send_message(  
            chat_id=update.effective_chat.id,  
            text="you just canceled the conversation"  
        )  
        return ConversationHandler.END  
    
    async def inline_query(self ,update, context):
        query = update.inline_query.query
        if not query:
            return
        elif query == "actives":
            messages = await Message.find_by_status('active')

            results = []
            for message in messages:
                results.append(
                    InlineQueryResultArticle(
                        id=message['messageID'],
                        title=message['text'],
                        input_message_content=InputTextMessageContent(f"{message['messageID']}\n{message['text']}\n#{message['tag']}"),
                    )
                )

            await context.bot.answer_inline_query(update.inline_query.id, results)


    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):  
        try:  
            if update.message.reply_to_message:  
                original_message = update.message.reply_to_message  
                txt = original_message.text.split("\n")  
                print(txt[0])  
                selected_m = dict()
                selected_m = Message.find_by_messageID(int(txt[0]))
                selected_m["answer"] = update.message.text
                selected_m["end_date"] = str(datetime.now())
                selected_m["status"] = "done"
                Message.update_message(selected_m["messageID"], selected_m) 

                if selected_m:  # Check if a message was found  
                    
                    await context.bot.send_message(  
                        chat_id=selected_m['userID'],  # Access using subscript notation  
                        text=update.message.text,  
                        reply_to_message_id=selected_m['messageID']  # Access using subscript notation  
                    )  
                else:  
                    print("Message not found")  # Handle the case when the message is not found  
        except Exception as e:  
            logging.error(f"Error in handle_message: {e}")



if __name__ == "__main__":  
    # Create the Application and pass it your bot's token  
    Message.read_from_json()
    print(MESSAGE)
    application = Application.builder().token(TOKEN).build()  
    bot = Bot()  

    # Conversation Handler  
    conv = ConversationHandler(  
        entry_points=[CommandHandler("start", bot.start_handler)],  
        states={  
            REQUEST: [CallbackQueryHandler(bot.button)],  
            CAPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.caption_handler)],  
        },  
        fallbacks=[MessageHandler(filters.ALL, bot.cancel_handler)],  
        allow_reentry=True  
    )  
    
    application.add_handler(conv)  
    application.add_handler(InlineQueryHandler(bot.inline_query))
    application.add_handler(MessageHandler(filters.REPLY, bot.handle_message))



    # Run the Bot  
    application.run_polling()

    