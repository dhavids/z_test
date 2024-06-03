import os
import csv

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

# Replace with your actual Telegram bot token
BOT_TOKEN = "7266174170:AAHuhL5p2tGBBHTwIhhON51rhPSXFbrWghM"

# Download directory for CSV files
DOWNLOAD_DIR = "downloads"


# Download directory for CSV files
DOWNLOAD_DIR = "downloads"


def download_csv(update, context):
    """
    Handles incoming messages, checks for documents, and downloads CSV files.
    """
    if update.message.document:
        document = update.message.document
        file_name = document.file_name

        # Check if file extension is CSV
        if file_name.endswith(".csv"):
            # Create download directory if it doesn't exist
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)

            # Download the file with a unique name
            file_path = os.path.join(DOWNLOAD_DIR, f"{file_name[:-4]}_{document.file_unique_id}.csv")
            with open(file_path, "wb") as f:
                file_content = update.message.document.get_file().download(file_path)
                f.write(file_content)

            # Send confirmation message with download path
            update.message.reply_text(f"CSV file downloaded to: {file_path}")
            print(f"CSV file downloaded to: {file_path}")
        else:
            update.message.reply_text("Not a CSV file. Please upload a CSV file.")
    else:
        update.message.reply_text("Please send a document to download.")


def main():
    """
    Initializes the Telegram bot and starts polling for updates.
    """
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handle document messages
    dispatcher.add_handler(MessageHandler(Filters.document, download_csv))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()