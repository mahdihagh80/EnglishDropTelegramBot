from .types import Action, ResponseType, HttpMethod
from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .vars import main_keyboard, BACKEND_URL
import aiohttp
import logging


async def get_package_detail() -> dict:
    url = f'{BACKEND_URL}/telegram-bot/package/'
    package_detail, status_code = await async_request(url, HttpMethod.GET, ResponseType.JSON)
    if status_code != 200:
        logging.error(f"error while getting package_detail, status_code = {status_code}, response: {str(package_detail)}")    
        return None
    return package_detail
    
    
def register(*, must=False, must_not=False):
    def inner(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            if must:
                if not context.user_data.get('is_registered', False):
                    query = update.callback_query
                    if query:
                        await query.answer()
                        await query.delete_message()
                    msg = 'شما تا به حال ثبت نام نکرده اید ، لطفا در ابتدا ثبت نام کنید\nبرای ثبت نام کلیک کنید'
                    keyboard = [
                                [InlineKeyboardButton("ثبت نام", callback_data='registration')],
                                [InlineKeyboardButton("بازگشت به منوی اصلی", callback_data='start')]
                                ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await context.bot.send_message(text=msg, chat_id=update.effective_user.id, reply_markup=reply_markup)
                    return Action.MAIN
                
            elif must_not:
                if context.user_data.get('is_registered', False):
                    query = update.callback_query
                    if query:
                        await query.answer()
                        await query.delete_message()
                    msg = 'شما قبلا ثبت نام انجام داده اید'
                    reply_markup = InlineKeyboardMarkup(main_keyboard)
                    await context.bot.send_message(text=msg, chat_id=update.effective_user.id, reply_markup=reply_markup)
                    return Action.MAIN

            return await func(update, context)
        return wrapper
    return inner


async def async_request(
        url: str,
        httpMethod: HttpMethod,
        response_type: ResponseType=ResponseType.JSON,
        data: dict=None
        ):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(url=url, method=httpMethod.value, data=data) as response:
                    match response_type:
                        case ResponseType.JSON:
                            return await response.json(), response.status
                        
                        case ResponseType.TEXT:
                            return await response.text(), response.status
                        
                        case ResponseType.RAW:
                            return await response.read(), response.status
        except Exception as e:
            logging.error(e, exc_info=True)
            return None, 500