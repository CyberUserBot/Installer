# Copyright (C) 2021 CyberUserBot
# This file is a part of < https://github.com/CyberUserBot/Installer/ >
# Please read the MIT license in
# <https://www.github.com/CyberUserBot/Installer/blob/master/LICENSE/>.

# Təkrar istifadəyə icazə verilmir.
# Yeniden kullanıma izin verilmiyor.
# Reuse is not allowed.

import asyncio
import os
import sys
import subprocess
from cyber_installer import hata, bilgi, onemli, soru
from asyncio import get_event_loop

from telethon import TelegramClient, events, version
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError, FloodWaitError, PhoneCodeExpiredError
from telethon.network import ConnectionTcpAbridged
from telethon.utils import get_display_name
from telethon.sessions import StringSession
from rich.prompt import Prompt
from .language import LANG
from random import choice, randint

import requests
import bs4

os.system("clear")
loop = asyncio.get_event_loop()
LANG  = LANG['ASTRING']

class InteractiveTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash,
                 telefon=None, proxy=None):
        super().__init__(
            session_user_id, api_id, api_hash,
            connection=ConnectionTcpAbridged,
            proxy=proxy
        )
        self.found_media = {}
        bilgi(LANG['CONNECTING'])
        try:
            loop.run_until_complete(self.connect())
        except IOError:
            hata(LANG['RETRYING'])
            loop.run_until_complete(self.connect())

        if not loop.run_until_complete(self.is_user_authorized()):
            if telefon == None:
               user_phone = soru(LANG['PHONE_NUMBER'])
            else:
               user_phone = telefon
            try:
                loop.run_until_complete(self.sign_in(user_phone))
                self_user = None
            except (PhoneNumberInvalidError, ValueError):
                hata(LANG['INVALID_NUMBER'])
                sys.exit(1)
            except FloodWaitError as e:
                hata(
                    f"💤 {LANG['FLOODWAIT_ERROR'].format(e.seconds)}.\n\n\n\n🔁 {LANG['TRY_AGAIN_FW'].format(e.seconds)}!"
                )      
                sys.exit(1)
            except PhoneCodeExpiredError as e:
                hata(LANG['CODE_EXPIRED_ERROR'])
                sys.exit(1)
            while self_user is None:
               code = soru(LANG['CODE'])
               try:
                  self_user =\
                     loop.run_until_complete(self.sign_in(code=code))
               except (PhoneNumberInvalidError, ValueError):
                  hata(LANG['INVALID_NUMBER'])
                  sys.exit(1)
               except FloodWaitError as e:
                  hata(
                      f"💤 {LANG['FLOODWAIT_ERROR'].format(e.seconds)}.\n\n\n\n🔁 {LANG['TRY_AGAIN_FW'].format(e.seconds)}!"
                  )
                  sys.exit(1)
               except PhoneCodeExpiredError as e:
                  hata(LANG['CODE_EXPIRED_ERROR'])
                  sys.exit(1)
               except SessionPasswordNeededError:
                  bilgi(LANG['2FA'])
                  pw = soru(LANG['PASS'])
                  try:
                     self_user =\
                        loop.run_until_complete(self.sign_in(password=pw))
                  except PasswordHashInvalidError:
                     hata(LANG['INVALID_2FA'])

def main():
    bilgi(f"[1] {LANG['NEW']}\n[2] {LANG['OLD']}")
            
    Sonuc = Prompt.ask(f"[bold yellow]{LANG['WHICH']}[/]", choices=["1", "2"], default="1")

    if Sonuc == "1":
        API_ID = 6
        API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
        client = InteractiveTelegramClient(StringSession(), API_ID, API_HASH)
        return client.session.save(), API_ID, API_HASH
    elif Sonuc == "2":
        numara = soru(LANG['PHONE_NUMBER_NEW'])
        try:
            rastgele = requests.post("https://my.telegram.org/auth/send_password", data={"phone": numara}).json()["random_hash"]
        except:
            hata(LANG['CANT_SEND_CODE'])
            sys.exit(1)
      
        sifre = soru(LANG['WRITE_CODE_FROM_TG'])
        try:
            cookie = requests.post("https://my.telegram.org/auth/login", data={"phone": numara, "random_hash": rastgele, "password": sifre}).cookies.get_dict()
        except:
            hata(LANG['INVALID_CODE_MY'])
            sys.exit(1)
        app = requests.post("https://my.telegram.org/apps", cookies=cookie).text
        soup = bs4.BeautifulSoup(app, features="html.parser")

        if soup.title.string == "Create new application":
            bilgi(LANG['NEW_APP'])
            hashh = soup.find("input", {"name": "hash"}).get("value")
            app_title = soru("Proqramın adı nə olsun: ")
            if app_title == '':
                app_title = choice(["cyber", "cyb", "cybe", "madelineproto", "telethon", "pyrogram"]) + choice(["", "-", "+", " "]) + choice(["user", "bot", "vue", "jsx", "python", "php"]) + choice([str(randint(10000, 99999)), ""])
            
            app_shortname = soru("Proqramın qısa adı nə olsun: ")
            if app_shortname == '':
                app_shortname = choice(["cyber", "cyb", "cybe", "madelineproto", "telethon", "pyrogram"]) + choice(["", "-", "+", " "]) + choice(["user", "bot", "vue", "jsx", "python", "php"]) + choice([str(randint(10000, 99999)), ""])
            
            AppInfo = {
                "hash": hashh,
                "app_title": app_title,
                "app_shortname": app_shortname,
                "app_url": "",
                "app_platform": choice(["android", "ios", "web", "desktop"]),
                "app_desc": choice(["madelineproto", "pyrogram", "telethon", "", "web", "cli"])
            }
            app = requests.post("https://my.telegram.org/apps/create", data=AppInfo, cookies=cookie).text

            if app == "ERROR":
                hata("(!) Telegram avtomatik proqram açma prosesi bloklandı. Xahiş edirəm 1-2 saatdan sonra yenidən başladın.")
                sys.exit(1)

            bilgi(LANG['CREATED'])
            bilgi(LANG['GETTING_API'])
            newapp = requests.get("https://my.telegram.org/apps", cookies=cookie).text
            newsoup = bs4.BeautifulSoup(newapp, features="html.parser")

            g_inputs = newsoup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})

            app_id = g_inputs[0].string
            api_hash = g_inputs[1].string
            onemli(f"{LANG['APIID']} {app_id}")
            onemli(f"{LANG['APIHASH']} {api_hash}")
            bilgi(LANG['STRING_GET'])
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
        
            return client.session.save(), app_id, api_hash
        elif soup.title.string == "App configuration":
            bilgi(LANG['SCRAPING'])
            g_inputs = soup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
            app_id = g_inputs[0].string
            api_hash = g_inputs[1].string
            bilgi(LANG['STRING_GET'])

            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            return client.session.save(), app_id, api_hash
        else:
            hata(LANG['ERROR'])
            sys.exit(1)
    else:
        hata("(!) Bilinməyən seçim.")
        sys.exit(1)
