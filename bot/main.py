from utils import handlers
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot, ReplyKeyboardRemove
from telegram.ext import PicklePersistence,Application, PersistenceInput, CallbackQueryHandler, MessageHandler, CommandHandler, ContextTypes, ConversationHandler, filters
from utils import vars
from utils.types import Action
import logging



logging.basicConfig(filename='bot.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)



def main():
    inp = PersistenceInput()
    my_persistence = PicklePersistence(filepath='./bot_data/bot_states.persistence', update_interval=5, store_data=inp)
    application = Application.builder().token(vars.BOT_TOKEN).persistence(persistence=my_persistence).build()
    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', handlers.start)],

        states={

            Action.MAIN: [
                        CallbackQueryHandler(handlers.start, pattern='start'),
                        CallbackQueryHandler(handlers.alex_recommendation, pattern='alex_recommendation'),
                        CallbackQueryHandler(handlers.registration_entrypoint, pattern='registration_entrypoint'),
                        CallbackQueryHandler(handlers.buy_package, pattern='buy_package'),
                        CallbackQueryHandler(handlers.create_user, pattern='create_user'),
            ],

            Action.REGISTRATION: [
                                    MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.parse_user_information),
                                    CallbackQueryHandler(handlers.start, 'start'),
            ],

            Action.TRANSACTION: [
                                CallbackQueryHandler(handlers.start, 'start'),
                                MessageHandler(filters.PHOTO, handlers.submit_transaction),
                                MessageHandler(~filters.PHOTO & ~filters.COMMAND, handlers.invalid_image)
            ]
        },

        fallbacks=[CommandHandler("start", handlers.start)],
        name = 'conversation',
        persistent=True

    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()


    