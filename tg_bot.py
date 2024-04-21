from lib import *
TOKEN = 'YOUR_TOKEN'


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот. Как дела?')


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
