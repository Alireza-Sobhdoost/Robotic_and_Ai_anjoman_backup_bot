import logging
from uuid import uuid4
from typing import Final


import requests
from telegram import Update, InlineQueryResultPhoto ,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, InlineQueryHandler, \
    ConversationHandler , CallbackQueryHandler
from os import remove

TOKEN: Final = "6927513102:AAECGNdiBmEFHRhxK2AzS81J9agm1h3AZi0"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

REQUEST = 0
CAPTION = 1


caption = {}


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query
#     await query.answer()
#     await query.edit_message_text(text="You pressed a button. Let's start a conversation.")
#     return CAPTION


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    global Request

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    # print(query.data)
    # print(type(query.data))
    if query.data == "1":
        await query.edit_message_text(
            text=f"مدیریت در خدمته !")
        Request = 1
    if query.data == "2":
        await query.edit_message_text(
            text=f"Please enter your Logical problem\n🟪 You can use /b to back to the main menu")
        Request = 2
    if query.data == "3":
        keyboard = [
            [
                InlineKeyboardButton("Factorial", callback_data="5"),
                InlineKeyboardButton("Circular permutation", callback_data="6"),
            ],
            [
                InlineKeyboardButton("Permutation", callback_data="7"),
                InlineKeyboardButton("Combination", callback_data="8"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_reply_markup(reply_markup=reply_markup)
        await query.edit_message_text(
            text=f"Hi dear {update.effective_user.first_name}\nwhat DM operation can I do for you ?",
            reply_markup=reply_markup)
        Request = 3
    if query.data == "5":
        await query.edit_message_text(
            text=f"Please enter the factorail problrm\n🟪 You can use /b to back to the main menu")
        Request = 5
    if query.data == "6":
        await query.edit_message_text(
            text=f"Please enter the Circular permutation problrm\n🟪 You can use /b to back to the main menu")
        Request = 6
    if query.data == "7":
        await query.edit_message_text(
            text=f"Please enter two numbers you want to calcaulate their permutation in the order bellow\n 👉 n r\n🟪 You can use /b to back to the main menu")
        Request = 7
    if query.data == "8":
        await query.edit_message_text(
            text=f"Please enter two numbers you want to calcaulate their combinition in the order bellow\n 👉 n r\n🟪 You can use /b to back to the main menu")
        Request = 8
    if query.data == "4":
        await query.edit_message_text(
            text=f"Please enter your problem to find out how many ways we have to distribute n thing to k choise in the order bellow\n 👉  X1 + X2 + .... + Xk = n\n 👉  Ai < X1 < Bi ,Ai <= X2 <= Bi , X3 = j\n🟪 You can use /b to back to the main menu")
        Request = 4
        # await query.edit_message_text(text=f"Selected option: {query.data}")
    REQUEST = Request
    return REQUEST


async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    print(update)
    await update.inline_query.answer(results, auto_pagination=True)


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if Request == 1 :
        await context.bot.send_message(text="ok you just started the conversation, now give me caption of your image",
                                   chat_id=update.effective_chat.id)
        return CAPTION


async def caption_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption[update.effective_chat.id] = update.message.text
    await context.bot.send_message(text="ok now send me your image",
                                   chat_id=update.effective_chat.id , reply_to_message_id=update.effective_message.id)




async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="you just canceled the conversation")


if __name__ == "__main__":
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()
    # Command Handler
    # application.add_handler(CommandHandler("start", start_handler))

    # Conversation Handler
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start_handler) ],
        states={
            REQUEST: [CallbackQueryHandler(button)],
            CAPTION: [MessageHandler(filters.TEXT, caption_handler)],
        },
        fallbacks=[MessageHandler(filters.ALL, cancel_handler)],
        allow_reentry=True
    )
    application.add_handler(conv)
    
    # application.add_handler(MessageHandler(filters.TEXT, echo_handler))
    application.add_handler(CallbackQueryHandler(button))
    # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))
    # Run the Bot
    application.run_polling()

