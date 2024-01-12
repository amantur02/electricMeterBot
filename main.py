import logging

from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from core.config import settings
from pydantic import BaseModel

from schemas import Resident

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! To add a user, enter /add_user.",
        reply_markup=ForceReply(selective=True),
    )


async def add_resident(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the process of adding a new resident."""
    chat_id = update.message.chat_id
    user_data[chat_id] = Resident()

    await update.message.reply_text("Enter the house number:")
    await get_house_number(update, context)


async def get_house_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the house number from the resident."""
    chat_id = update.message.chat_id
    user_data[chat_id].house_number = update.message.text

    await update.message.reply_text("Enter the resident name:")
    await get_resident_name(update, context)


async def get_resident_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the resident name from the user."""
    chat_id = update.message.chat_id
    user_data[chat_id].user_name = update.message.text

    await update.message.reply_text("Enter the phone number:")
    await get_phone_number(update, context)


async def get_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the phone number from the resident and create resident"""
    chat_id = update.message.chat_id
    user_data[chat_id].phone_number = update.message.text

    user_object = user_data[chat_id]
    await update.message.reply_text(f"User added:\n{user_object}")

    del user_data[chat_id]  # Clear temporary data after completion
    return None


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(settings.TOKEN).build()

    handlers = [
        CommandHandler("start", start),
        CommandHandler("add_user", add_resident),
        MessageHandler(filters.TEXT & ~filters.COMMAND, get_house_number),
        MessageHandler(filters.TEXT & ~filters.COMMAND, get_resident_name),
        MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_number),
    ]

    for handler in handlers:
        application.add_handler(handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
