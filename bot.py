#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time

import lxml.html as lh
import requests


def download(url: str) -> str:
    """ Download data with throttling """
    print('[tools.py::download] Fetching', url)
    time.sleep(1)
    content = requests.get(url).text
    return content


def send_telegram(message: str, bot_token: str, bot_chatID: str) -> None:
    """ Send a message via Telegram bot """
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message + '&disable_web_page_preview=True'
    requests.get(url)


def check_sites() -> None:
    """ Check sites """
    print('[bot.py] Initializing, reading config')
    with open('config.json') as config_file:
        config = json.loads(config_file.read())
    bot_token = config['bot_token']
    bot_chatID = config['bot_chatID']

    for site in config['sites']:
        url = site['url']
        term = site['term']
        notify_on = site['notify_on']
        selector = site['selector']
        print('[bot.py] Checking site:', url)

        try:
            content = download(url)
        except:
            print('[bot.py] Error while fetching site, skipping for now')
            continue

        content_part = content
        if selector != '':
            tree = lh.fromstring(content)
            elements = tree.cssselect(selector)
            if len(elements) == 0:
                print('[bot.py] Element not found on site, skipping.')
                continue
            content_part = elements[0].text_content()

        if (term in content_part and notify_on == 'present') or (
            term not in content_part and notify_on == 'absent'):
            message = 'Term <' + term + '> ' + notify_on + ' on site ' + url
            send_telegram(message, bot_token, bot_chatID)

    print('[bot.py] Finish')


if __name__ == "__main__":
    check_sites()
