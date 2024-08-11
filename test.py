import logging  
from uuid import uuid4  
from typing import Final  

import requests  
from telegram import Update, InlineQueryResultPhoto, InlineKeyboardButton, InlineKeyboardMarkup  
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

class Bot:  
    def __init__(self):  
        self.caption = {}  

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  
        """Sends a message with three inline buttons attached."""  
        keyboard = [  
            [  
                InlineKeyboardButton("ارتباط با دبیر", callback_data="1"),  
                InlineKeyboardButton("ارتباط با آموزش", callback_data="2"),  
            ],  
            [  
                InlineKeyboardButton("ارتباط با رویداد ها", callback_data="3"),  
                InlineKeyboardButton("انتقادات و پیشنهادات", callback_data="4"),  
            ],  
        ]  

        reply_markup = InlineKeyboardMarkup(keyboard)  

        await update.message.reply_text(  
            f"روز بخیر {update.effective_user.first_name}\nبه بات پشتیبانی انجمن رباتیک و هوش مصنوعی دانشگاه گیلان خوش آمدید\nچطور میتونم کمکتون کنم ؟",  
            reply_markup=reply_markup)  

        return REQUEST  # Transition to REQUEST state  

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
        """Parses the CallbackQuery and updates the message text."""  
        query = update.callback_query  
        await query.answer()  
        if query.data == "1":  
            await query.edit_message_text(text="مدیریت در خدمته !")  
            return CAPTION  # Transition to CAPTION state  
        # Handle other button actions similarly if needed  
        return REQUEST  

    async def caption_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
        """Handles the caption input from the user."""  
        self.caption[update.effective_chat.id] = update.message.text  
        print(update)
        await context.bot.send_message(  
            text=f"{update.message.text}\n #دبیر",  
            chat_id= 7212319806,  
        )  
        return ConversationHandler.END  # End the conversation, or change this if you expect to stay in conversation  

    async def cancel_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
        """Handles the cancellation of the conversation."""  
        await context.bot.send_message(  
            chat_id=update.effective_chat.id,  
            text="you just canceled the conversation"  
        )  
        return ConversationHandler.END  
    
    async def inline_query(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.inline_query.query
        data = requests.get("https://thronesapi.com/api/v2/Characters")
        data = data.json()
        characters = {}
        for character in data:
            characters[character["fullName"]] = character["imageUrl"]
        if not query:
            results = []

            for name, url in characters.items():
                newItem = InlineQueryResultPhoto(
                    id=str(uuid4()),
                    photo_url=url,
                    thumbnail_url=url,
                    caption=name
                )
                results.append(newItem)
        else:
            results = []
            for name, url in characters.items():
                if query in name:
                    newItem = InlineQueryResultPhoto(
                        id=str(uuid4()),
                        photo_url=url,
                        thumbnail_url=url,
                        caption=name
                    )
                    results.append(newItem)
        print(update.effective_chat.id)
        
        await update.inline_query.answer(results, auto_pagination=True)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):  
        try:  
            if update.message.reply_to_message:  
                original_message = update.message.reply_to_message  
                # Processing message reply  
                await context.bot.send_message(chat_id=774601286, text=update.message.text ,reply_to_message_id=617)  
        except Exception as e:  
            logging.error(f"Error in handle_message: {e}")  



if __name__ == "__main__":  
    # Create the Application and pass it your bot's token  
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