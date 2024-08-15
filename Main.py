import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, CallbackQueryHandler

Request = 0
import Token
TOKEN = Token.Token.getToken()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Create a file handler and set the file name to log to "bot_log.txt"
file_handler = logging.FileHandler('bot_log.txt')
file_handler.setLevel(logging.INFO)

# Create a formatter for the file handler
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("King polynomial", callback_data="1"),
            InlineKeyboardButton("Logical calculator", callback_data="2"),
        ],
        [
            InlineKeyboardButton("DM calaculator", callback_data="3"),
            InlineKeyboardButton("caught the red-handed", callback_data="4"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Hi dear {update.effective_user.first_name}\nwellcome to my Dm bot\nplease choose one of our services!",
        reply_markup=reply_markup)


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
            text=f"Please enter your Board description to calculate thr King Polynomial there is a valid exaple\n3 3\n0 0 0\n0 0 0\n0 1 0\n🟪 You can use /b to back to the main menu")
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


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""


async def logic(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    import Logic
    result = Logic.expression(job.data)
    await context.bot.send_message(job.chat_id, text=f"Result: {result}")


async def set_logicalCalculator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    # Get the raw input string from the user's message
    input_data = update.message.text
    if not input_data:
        await context.bot.send_message(chat_id, text="Please provide input data.")
        return

    due = 1.0
    context.job_queue.run_once(logic, due, chat_id=chat_id, name=str(chat_id), data=input_data)


async def DM_factorial(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    import DmCalc
    result = DmCalc.Factorial_operator(job.data)
    await context.bot.send_message(job.chat_id, text=f"Result: {result}")


async def set_factorial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    # Get the raw input string from the user's message
    input_data = update.message.text
    if not input_data:
        await context.bot.send_message(chat_id, text="Please provide input data.")
        return

    due = 1.0
    context.job_queue.run_once(DM_factorial, due, chat_id=chat_id, name=str(chat_id), data=input_data)


async def DM_circular_permutation(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    import DmCalc
    result = DmCalc.Circular_permutation(job.data)
    await context.bot.send_message(job.chat_id, text=f"Result: {result}")


async def set_circular_permutation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    # Get the raw input string from the user's message
    input_data = update.message.text
    if not input_data:
        await context.bot.send_message(chat_id, text="Please provide input data.")
        return

    due = 1.0
    context.job_queue.run_once(DM_circular_permutation, due, chat_id=chat_id, name=str(chat_id), data=input_data)


async def DM_permutation(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    import DmCalc
    result = DmCalc.Permutation(job.data)
    await context.bot.send_message(job.chat_id, text=f"Result: {result}")


async def set_permutation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    # Get the raw input string from the user's message
    input_data = update.message.text
    if not input_data:
        await context.bot.send_message(chat_id, text="Please provide input data.")
        return

    due = 1.0
    context.job_queue.run_once(DM_permutation, due, chat_id=chat_id, name=str(chat_id), data=input_data)


async def DM_combinition(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    import DmCalc
    result = DmCalc.Combination(job.data)
    await context.bot.send_message(job.chat_id, text=f"Result: {result}")


async def set_combinition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    # Get the raw input string from the user's message
    input_data = update.message.text
    if not input_data:
        await context.bot.send_message(chat_id, text="Please provide input data.")
        return

    due = 1.0
    context.job_queue.run_once(DM_combinition, due, chat_id=chat_id, name=str(chat_id), data=input_data)


async def red_handed(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    import RedHanded
    result = RedHanded.set_combinations(job.data)
    await context.bot.send_message(job.chat_id, text=f"Result: {result}")


async def set_red_handed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    # Get the raw input string from the user's message
    input_data = update.message.text
    if not input_data:
        await context.bot.send_message(chat_id, text="Please provide input data.")
        return

    due = 1.0
    context.job_queue.run_once(red_handed, due, chat_id=chat_id, name=str(chat_id), data=input_data)

async def king(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    import KingPolynomial
    result = KingPolynomial.Kingpolynomial(job.data)
    await context.bot.send_message(job.chat_id, text=f"\t{result}")


async def set_king_polynomial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    # Get the raw input string from the user's message
    input_data = update.message.text
    if not input_data:
        await context.bot.send_message(chat_id, text="Please provide input data.")
        return

    due = 1.0
    context.job_queue.run_once(king, due, chat_id=chat_id, name=str(chat_id), data=input_data)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Request
    print(Request)
    # input_data = update.message.text
    # print(input_data)
    if Request == 1:
        await set_king_polynomial(update, context)
    elif Request == 2:
        await set_logicalCalculator(update, context)
    elif Request == 5:
        await set_factorial(update, context)
    elif Request == 6:
        await set_circular_permutation(update, context)
    elif Request == 7:
        await set_permutation(update, context)
    elif Request == 8:
        await set_combinition(update, context)
    elif Request == 4:
        await set_red_handed(update, context)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=update.message.text
        )


async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global Request
    if Request == 5 or Request == 6 or Request == 7 or Request == 8:
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
        Request = 3

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Hi again dear {update.effective_user.first_name}\nwhat DM operation can I do for you ?",
            reply_markup=reply_markup)

    else:

        keyboard = [
            [
                InlineKeyboardButton("King polynomial", callback_data="1"),
                InlineKeyboardButton("Logical calculator", callback_data="2"),
            ],
            [
                InlineKeyboardButton("DM calaculator", callback_data="3"),
                InlineKeyboardButton("caught the red-handed", callback_data="4"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Hi again dear {update.effective_user.first_name}\nHow can I help you with your Dm today",
            reply_markup=reply_markup)


if __name__ == "__main__":
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()
    # Command Handler
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("b", back_handler))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT, message_handler))
    # application.add_handler(MessageHandler(filters.FORWARDED & filters.PHOTO, callback))

    # Run the Bot

    application.run_polling()