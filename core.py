import html
import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#  ----------------------------------
#  Основные настроки скрипта
#  Токен вашего тг-бота
bot_token = ''
#  Токен avito
avito_token = ''
#  ID вашего чата с тг-ботом
chat_id = ''
#  Список интересных запросов (список любой длины)
key_phrase = ['ЗАПРОС1', 'ЗАПРОС2',] #  и т.д.
#  Время между обновлениями линка чекером (в мин.)
check_time = 5
#  ----------------------------------


def tg_alert(alarm):
    """Функция отправки сообщения в чат через бота telegram"""
    return requests.get(f'https://api.telegram.org/bot{bot_token}'
                        f'/sendMessage?chat_id={chat_id}'
                        f'&parse_mode=html&text={alarm}')


def create_empty_json_file(file_name):
    """Функция проверки наличия файла json в директории скрипта"""
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    if not os.path.isfile(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('{}')
        print(f'Файл {file_name} был создан.')
    else:
        print(f'Файл {file_name} уже существует.')


def extract_data_from_blocks(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    data_dict = {}
    blocks = soup.find_all('div', attrs={'data-marker': 'item'})
    for block in blocks:
        item_id = block.get('data-item-id')
        title = html.unescape(
            block.find('a', class_='iva-item-sliderLink-uLz1v')['title'])
        link = (f'https://www.avito.ru/'
                f'{block.find("a",
                              class_="iva-item-sliderLink-uLz1v")["href"]}')
        title_cleaned = re.sub(r'[^\w\s]', '', title)[11:45] + '...' \
            if len(re.sub(r'[^\w\s]', '', title)) > 35 \
            else re.sub(r'[^\w\s]', '', title)
        price_element = block.find(class_='iva-item-priceStep-uq2CQ')
        price = html.unescape(price_element.get_text())
        price_cleaned = re.sub(r"\D", "", price)
        data_dict[item_id] = [title_cleaned, price_cleaned, link]
    return data_dict


def collecting_dict_links(my_list):
    result_data = {}
    for item in my_list:
        driver.get(
            f'https://www.avito.ru/samara?cd=1&q={item.replace(" ", "+")}'
            )
        WebDriverWait(
            driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "iva-item-sliderLink-uLz1v")))
        page_content = driver.page_source
        data = extract_data_from_blocks(page_content)
        result_data.update(data)
        time.sleep(4)
    return result_data


driver = webdriver.Chrome()
driver.get('https://www.avito.ru/')
create_empty_json_file('avito.json')
cookie_au = {'name': 'auth', 'value': '1'}
cookie_session = {'name': 'sessid', 'value': avito_token}
driver.add_cookie(cookie_au)
driver.add_cookie(cookie_session)
driver.maximize_window()
driver.refresh()
time.sleep(1)

count = 0
while True:
    data = collecting_dict_links(key_phrase)
    with open('avito.json', 'r', encoding='utf-8') as file:
        existing_data = json.load(file)
    missing_keys = {}
    for key in data.keys():
        if key not in existing_data:
            missing_keys[key] = data[key]
    if len(missing_keys) > 0:
        missing_keys_str = '\n'.join([
            f'{value[0]}, цена {value[1]} ₽: {value[2]}'
            for value in missing_keys.values()
        ])
        tg_alert(missing_keys_str)
        with open('avito.json', 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
        existing_data.update(missing_keys)
        with open('avito.json', 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
        print('Сообщение отправлено в чат')
    count += 1
    print(f'Проведена проверка №{count}')
    time.sleep(check_time*60)
