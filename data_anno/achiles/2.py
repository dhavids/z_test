import os
import telegram

# Replace with your actual Telegram bot token
BOT_TOKEN = '7266174170:AAHuhL5p2tGBBHTwIhhON51rhPSXFbrWghM'

class CSVBot:
    def __init__(self, bot_token):
        self.bot = telegram.Bot(token=bot_token)
        self.dispatcher = self.bot.dispatcher

    def handle_message(self, update, context):
        message = update.message.text
        document = update.message.document

        if document:
            file_name = document.file_name
            file_path = os.path.join(os.getcwd(), file_name)

            if file_name.lower().endswith('.csv'):
                try:
                    document.download(file_path)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"CSV file '{file_name}' downloaded successfully!")
                except Exception as e:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error downloading CSV: {e}")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a CSV file.")

    def start_polling(self):
        self.dispatcher.add_handler(telegram.MessageHandler(filters=[telegram.Filters.all], callback=self.handle_message))
        self.dispatcher.start_polling()
        self.dispatcher.idle()

if __name__ == '__main__':
    bot = CSVBot(BOT_TOKEN)
    bot.start_polling()