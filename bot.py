#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time

import lxml.html as lh
import requests

config_file = 'config.json'


def download(url: str) -> str:
    """ Download data with throttling """
    print('[download] Fetching', url)
    time.sleep(1)
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    content = requests.get(url, headers=custom_headers).text
    return content


def send_telegram(message: str, bot_token: str, bot_chatID: str) -> None:
    """ Send a message via Telegram bot """
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message + '&disable_web_page_preview=True'
    requests.get(url)


def check_sites() -> None:
    """ Check sites """
    print('[bot.py] Initializing, reading config')
    with open(config_file) as read_config_file:
        config = json.loads(read_config_file.read())
    bot_token = config['bot_token']
    bot_chatID = config['bot_chatID']

    for i in range(len(config['sites'])):
        site = config['sites'][i]
        name = site['name']
        url = site['url']
        term = site['term']
        notify_on = site['notify_on']
        selector = site['selector']
        enabled = site['enabled']
        if not enabled:
            print(f'Site {name} disabled, continuing')
            continue

        print(f'[bot.py] Checking site: {name} ({url})')

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
            print('Sending notification!')
            message = f'Term <{term}> {notify_on} on site [{name}]({url})'
            message = message.replace('&', '%26amp;')
            send_telegram(message, bot_token, bot_chatID)
            # Disable after the message was sent
            config['sites'][i]['enabled'] = False

    with open(config_file, 'w') as write_config_file:
        write_config_file.write(json.dumps(config, indent=2))

    print('[bot.py] Finish')


if __name__ == "__main__":
    check_sites()
