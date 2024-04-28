from .models import Transaction
from django.conf import settings
import requests
import logging
from urllib.parse import quote
import os
from django.conf import settings
from functools import partial


logging.basicConfig(filename=settings.BASE_DIR/'telegram_bot/cron.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
TOKEN = os.getenv('BOT_TOKEN')

ACCEPT_MSG = '''
✅ پرداخت شما مورد تأیید قرار گرفت

برای دسترسی ویدیوهای دوره ، از طریق لینک یکبار مصرفِ زیر،عضو کانال ما شوید.

{telegram_link}

و همچنین برای شرکت در لایوهای هفتگی ، با آیدی‌ پیجی که بالا برای ما ارسال کردید، به پیج زیر ریکوئست دهید و تا زمان قبول شدن ریکوئست منتظر بمانید.
از صبر و بردباری شما متشکریم❤️🙏

آیدی اینستاگرام:
 {instagram_link}
'''

REJECT_MSG = '''
❌واریزی شما مورد تایید نبود❌
در صورت هرگونه مشکل با پشتیبانی در تلگرام ارتباط برقرار کنید
آیدی پشتیبانی: 
@englishdropbotsupport'
'''

def send_links():
    queryset = Transaction.objects.filter(state=Transaction.TransactionState.ACCEPTED)
    queryset = queryset.filter(links_sent=False)

    for transaction in queryset:
        error_inner_loop = False
        
        instagram_pages = transaction.package.instagram_pages.values('instagram_id')
        for page in instagram_pages:
            partial_msg = partial(ACCEPT_MSG.format, instagram_link='www.instagram.com/' + page['instagram_id'])
        
    
        telegram_channels = transaction.package.telegram_channels.values()
        for channel in telegram_channels:
            url = f"https://api.telegram.org/bot{TOKEN}/createChatInviteLink?chat_id={channel['chat_id']}&member_limit=1"
            resp = requests.get(url).json()
            if not resp['ok']:
                logging.error(f"error while getting invite link for channel {channel['id']} and transaction {transaction.id}, response : " + str(resp))
                error_inner_loop = True
                break
            msg = partial_msg(telegram_link=quote(resp['result']['invite_link']))
            
        if error_inner_loop:
            continue

        chat_id = transaction.user.chat_id
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML"
        res = requests.get(url).json()
        if not resp['ok']:
            logging.error(f'error while sending links to telegram, msg = {msg}, response : ' + str(resp))
            continue
        transaction.links_sent = True
        transaction.save()


def send_reject_message():
    queryset = Transaction.objects.filter(state=Transaction.TransactionState.REJECTED)
    queryset = queryset.filter(links_sent=False)
    
    for transaction in queryset:
        chat_id = transaction.user.chat_id
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={REJECT_MSG}"
        resp = requests.get(url).json()
        if not resp['ok']:
            logging.error(f'error while sending reject msg to telegram, msg = {msg}, response : ' + str(resp))
            continue
        transaction.links_sent = True
        transaction.save()


