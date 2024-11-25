from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = '7625417352:AAF4rYYRMUhQihSoNIwFOAd1_IYenehAbNk'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a file, and I'll give you a direct download link.")

def handle_file(update: Update, context: CallbackContext):
    file = update.message.document or update.message.video or update.message.audio
    if file:
        file_id = file.file_id
        file_info = context.bot.get_file(file_id)
        file_path = file_info.file_path

        # Generate the direct download URL
        direct_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        update.message.reply_text(f"Here is your direct download link:\n{direct_url}\n\nYou can download it without any speed limits!")
    else:
        update.message.reply_text("Please send a valid file.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.audio, handle_file))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
