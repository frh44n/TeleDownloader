from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = 'YOUR_BOT_TOKEN'

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Forward me a message containing a file, and I'll generate a direct download link for it."
    )

def handle_forwarded_message(update: Update, context: CallbackContext):
    # Check if the forwarded message contains a file
    file = update.message.document or update.message.video or update.message.audio
    if file:
        try:
            # Get file ID and fetch file information
            file_id = file.file_id
            file_info = context.bot.get_file(file_id)
            file_path = file_info.file_path

            # Generate the direct download URL
            direct_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

            update.message.reply_text(
                f"Here is your direct download link:\n{direct_url}\n\nYou can download it without any speed limits!"
            )
        except Exception as e:
            update.message.reply_text(f"An error occurred: {str(e)}")
    else:
        update.message.reply_text("The forwarded message doesn't seem to contain a valid file.")

def main():
    # Set up the bot
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Add command and message handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.forwarded & (Filters.document | Filters.video | Filters.audio), handle_forwarded_message))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
