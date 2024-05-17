import utils.vars as vars
from .types import Action, HttpMethod, ResponseType
from .util import async_request, register, get_package_detail
import logging 
import os
from .vars import main_keyboard
from telegram.constants import ParseMode

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardRemove,
    Video,
)

from telegram.ext import (
    ContextTypes,
    PersistenceInput,
    CallbackQueryHandler,
    MessageHandler,
    CommandHandler,
    filters
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    query = update.callback_query
    if query:
        await query.edit_message_text(text=vars.START, reply_markup=InlineKeyboardMarkup(main_keyboard), parse_mode=ParseMode.HTML)
        await query.answer()
        return Action.MAIN

    reply_markup = InlineKeyboardMarkup(main_keyboard)
    await context.bot.send_message(text=vars.START,chat_id=update.effective_user.id, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return Action.MAIN


# @register(must_not=True)
async def registration_entrypoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    query = update.callback_query
    keyboard = [[InlineKeyboardButton('بازگشت به منوی اصلی', callback_data='start')]]
    await query.answer()
    await query.edit_message_text(vars.REGISTRATION_GUIDE_MESSAGE, reply_markup=InlineKeyboardMarkup(keyboard))
    return Action.REGISTRATION


async def parse_user_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    text = update.message.text
    text = text.strip('\n').split('\n')
    text = [txt.strip() for txt in text if txt!='']

    if len(text) != 3:
        keyboard = [[InlineKeyboardButton('بازگشت به منوی اصلی', callback_data='start')]]
        await context.bot.send_message(
            text = vars.REGISTRATION_INVALID_INPUT,
            chat_id=update.effective_user.id,
            reply_markup=InlineKeyboardMarkup(keyboard))
        return Action.REGISTRATION

        

    user = {
        'chat_id' : update.effective_user.id,
        'full_name': text[0],
        'phone_number' : text[1],
        'instagram_id' : text[2].strip('@')
    }

    context.user_data['user_information'] = user

    keyboard = [
        [InlineKeyboardButton('تایید', callback_data='create_user')],
        [InlineKeyboardButton('اصلاح مشخصات', callback_data='registration_entrypoint')],
        [InlineKeyboardButton('بازگشت به منوی اصلی', callback_data='start')]
    ]

    await context.bot.send_message(
        text=vars.INFORMATION_VERIFICATION.format(user['full_name'], user['phone_number'], user['instagram_id']),
        chat_id=user['chat_id'],reply_markup=InlineKeyboardMarkup(keyboard)
        )
    return Action.MAIN


async def create_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    query = update.callback_query
    await query.answer()
    
    user = context.user_data['user_information']
    url = f'{vars.BACKEND_URL}/telegram-bot/telegram-user/'
    res, status_code = await async_request(url, HttpMethod.POST, ResponseType.JSON, data=user)
    if status_code != 201:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        logging.error(f"error while creating user, status_code = {status_code}, user : {str(user)}, response: {str(res)}")
        await query.edit_message_text(text=vars.INTERNAL_ERROR, reply_markup=reply_markup)
        return Action.MAIN
    
    context.user_data['is_registered'] = True
    next_stage = await buy_package(update, context)
    return next_stage



async def alex_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    query = update.callback_query
    await query.answer()
    await query.delete_message()

    package_detail = await get_package_detail()
    if not package_detail:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        await context.bot.send_message(text=vars.INTERNAL_ERROR,chat_id=update.effective_user.id, reply_markup=reply_markup)
        return Action.MAIN
    
    voice, status_code = await async_request(vars.BACKEND_URL+package_detail['voice'], HttpMethod.GET, ResponseType.RAW)
    if status_code != 200:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        logging.error(f"error while getting voice, status_code = {status_code}, response: {str(voice)}")
        await context.bot.send_message(text=vars.INTERNAL_ERROR,chat_id=update.effective_user.id, reply_markup=reply_markup)
        return Action.MAIN
    
    if context.user_data.get('is_registered', False):
        keyboard = [
            [InlineKeyboardButton('خرید', callback_data='buy_package')],
            [InlineKeyboardButton('بازگشت به منوی اصلی', callback_data='start')]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton('خرید', callback_data='registration_entrypoint')],
            [InlineKeyboardButton('بازگشت به منوی اصلی', callback_data='start')]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=vars.ALEX_RECOMANDATION.format(package_detail['title'], package_detail['description']),
        parse_mode=ParseMode.HTML
        )
    
    await context.bot.send_voice(chat_id=update.effective_user.id, voice=voice)

    file_id = 'BAACAgQAAxkBAAMDZkd8JkvuUtJMmeKGqH8uCV4ZxsUAAnwXAAICSjFS0IepUlNZNpQ1BA'
    file_unique_id = 'AgADfBcAAgJKMVI'
    video = Video(file_id=file_id, file_unique_id=file_unique_id, width=848, height=464, duration=80)
    await context.bot.send_video(chat_id=update.effective_user.id, video=video, caption='ویدیو نمونه دوره')
    await context.bot.send_message(chat_id=update.effective_user.id, text='گزینه موردنظر را انتخاب کنید', reply_markup=reply_markup)
    return Action.MAIN


async def buy_package(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    query = update.callback_query
    if query:
        await query.answer()    
        await query.delete_message()    

    url = f'{vars.BACKEND_URL}/telegram-bot/bank-accounts/'
    bank_account, status_code = await async_request(url, HttpMethod.GET, ResponseType.JSON)
    if status_code != 200:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        logging.error(f"error while getting bank_account, status_code = {status_code}, response: {str(bank_account)}")
        await context.bot.send_message(text=vars.INTERNAL_ERROR,chat_id=update.effective_user.id, reply_markup=reply_markup)
        return Action.MAIN
    
    package_detail = await get_package_detail()
    if not package_detail:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        await context.bot.send_message(text=vars.INTERNAL_ERROR,chat_id=update.effective_user.id, reply_markup=reply_markup)
        return Action.MAIN
    
    keyboard = [[InlineKeyboardButton('منصرف شدم', callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = vars.TRANSACTION_DETAIL.format(package_detail['price'], bank_account['owner_name'], bank_account['card_number'])
    await context.bot.send_message(text=msg, chat_id=update.effective_user.id, reply_markup=reply_markup, parse_mode=ParseMode.HTML)    
    context.user_data['pending_transaction'] = {
        "bank_account": bank_account['id'],
        "package": package_detail['id'],
        'package_price': package_detail['price'],
        
    }
    return Action.TRANSACTION



async def submit_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    photo_file = await update.message.photo[-1].get_file()
    img, status_code = await async_request(photo_file.file_path, HttpMethod.GET, ResponseType.RAW)
    
    if status_code != 200:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        logging.error(f"error while getting receipt from telegram, status_code = {status_code}, response: {str(img)}")
        await context.bot.send_message(text=vars.INTERNAL_ERROR,chat_id=update.effective_user.id, reply_markup=reply_markup)
        return Action.MAIN
    
    with open(f'{photo_file.file_unique_id}.jpg', 'wb') as f:
        f.write(img)

    transaction = context.user_data['pending_transaction']
    transaction['user'] = update.effective_user.id

    url = f'{vars.BACKEND_URL}/telegram-bot/transactions/'
    resp, status_code = await async_request(url, HttpMethod.POST, ResponseType.JSON, data=transaction)
    if status_code != 201:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        logging.error(f"error while getting creating transaction, status_code = {status_code}, response: {str(resp)}")
        await context.bot.send_message(text=vars.INTERNAL_ERROR,chat_id=update.effective_user.id, reply_markup=reply_markup)
        return Action.MAIN
    

    receipt = {"receipt": open(f'{photo_file.file_unique_id}.jpg', 'rb')}
    resp, status_code = await async_request(f"{url}{resp['id']}/", HttpMethod.PATCH, ResponseType.RAW, data=receipt)
    if status_code != 200:
        reply_markup = InlineKeyboardMarkup(main_keyboard)
        logging.error(f"error while sending receipt to backend, status_code = {status_code}, response: {str(resp)}")
        await context.bot.send_message(text=vars.INTERNAL_ERROR,chat_id=update.effective_user.id, reply_markup=reply_markup)
        return Action.MAIN
    
    context.user_data.pop('pending_transaction')
    os.remove(f'{photo_file.file_unique_id}.jpg')
    

    reply_markup = InlineKeyboardMarkup(main_keyboard)
    await context.bot.send_message(
        text="خرید شما با موفقیت ثبت شد و پس از تایید لینک های مرتبط با دوره برای شما ارسال خواهد شد",
        chat_id=update.effective_user.id,
        reply_markup=reply_markup,
    )

    return Action.MAIN


async def invalid_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Action:
    await context.bot.send_message(chat_id=update.effective_user.id, text='ارسالی شما معتبر نیست ، لطفا یک عکس رسید خود را ارسال کنید')
    return Action.TRANSACTION