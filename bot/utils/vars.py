from telegram import InlineKeyboardButton
import os 

main_keyboard = [[InlineKeyboardButton('پیشنهاد ویژه استاد الکس', callback_data='alex_recommendation')]]

BOT_TOKEN = os.getenv('BOT_TOKEN')

BACKEND_URL = os.getenv('BACKEND_URL')

START = '''
سلام و احترام❤️
وقت بخیر
 
✅خیلیییی ممنونم از اینکه مارو برای شروع یادگیری مکالمه زبان انگلیسی انتخاب کردید💚
با ما پرونده زبان انگلیسی تو برای همیشه ببند و بذار کنار 💪

✅بنده الکس، موسس و مدیر موسسه Englishdrop هستم.
مدرسِ مکالمه زبان انگلیسی و با روش ابداعی ( بدون کتاب و آزمون و دفتر و قلم) کاملا مکالمه محور

✅آدرس پیج اصلی اینستاگرام: 
Englishdrop.ir

✅برای ارتباط با ما و پشتیبانی فقط کافیست به این آیدی در تلگرام پیام بدید.
@englishdropbotsupport

✅با<b> ٣ تا کلیک ساده</b>، ثبت نام تون انجام میشه😍

برای شروع ثبت نام دوره، روی آیکون <b>پیشنهاد ویژه الکس</b>، کلیک کنید👇
'''

REGISTRATION_GUIDE_MESSAGE = '''
اطلاعات خود را مانند نمونه ارسال کنید.
نام و نام خانوادگی
شماره تماس 
آیدی اینستاگرام تون بدون (@)

توجه داشته باشید که اطلاعات خود را حتما در ٣ سطر مانند نمونه زیر ارسال کنید👇👇👇

مثال: 
علی رضوانی 
09121234567
Englishdrop
'''

REGISTRATION_INVALID_INPUT = '''
لطفا مشخصات خود را به فرمت درست وارد کنید ، مانند نمونه زیر :
الکس رضوانی
09121111111
nenglishdrop.ir
'''

INFORMATION_VERIFICATION = '''
آیا مشخصات خود را تایید می کنید ؟
نام و نام خانوادگی : {}
شماره همراه : {}
آدرس اینستاگرام : {}
'''

CREATE_USER_SUCCESSFULLY = 'ثبت نام با موفقیت انجام شد'

INTERNAL_ERROR = 'اختلالی بوجود آمده است ، لطفا جند لحظه دیگر تلاش کنید و در صورت مشاهده مجدد به پشتیبانی پیام دهید'

ALEX_RECOMANDATION = '<b>{}</b>\n{}'

TRANSACTION_DETAIL = '''
لطفا مبلغ <b>{}</b> را به شماره کارت زیر به نام <b> {} </b>واریز کنید و بعد فیش رو همینجا برامون ارسال کنید🙏

شمارت کارت : {}
'''