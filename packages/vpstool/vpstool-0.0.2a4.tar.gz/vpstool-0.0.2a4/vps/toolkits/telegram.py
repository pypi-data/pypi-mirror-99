"""Telegram bot"""
import json
import requests
import dofast.utils as du

from vps.config import HEMA_BOT, AUTH, HTTP_PROXY, TELEGRAM_KEY, MESSALERT
from .endecode import short_decode, decode_with_keyfile as dkey

proxies = {'http': dkey(AUTH, HTTP_PROXY)}


def bot_say(api_token: str, text: str, bot_name: str = 'PlutoShare'):
    url = f"http://api.telegram.org/bot{api_token}/sendMessage?chat_id=@{bot_name}&text={text}"
    requests.get(url, proxies=proxies)


def bot_messalert(msg:str)->None:
    bot_say(dkey(TELEGRAM_KEY, MESSALERT), msg, bot_name='messalert')

def read_hema_bot():
    bot_updates = dkey(TELEGRAM_KEY, HEMA_BOT)
    resp = du.client.get(bot_updates, proxies=proxies)
    print(json.loads(resp.text))


def download_file_by_id(file_id: str) -> None:
    bot_updates = dkey(TELEGRAM_KEY, HEMA_BOT)
    file_url = bot_updates.replace('getUpdates', f'getFile?file_id={file_id}')
    json_res = du.client.get(file_url, proxies=proxies).text
    file_name = json.loads(json_res)['result']['file_path']

    file_url = bot_updates.replace('getUpdates',
                                   file_name).replace('/bot', '/file/bot')
    du.download(file_url, proxy=dkey(AUTH, HTTP_PROXY))


