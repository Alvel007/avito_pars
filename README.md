# avito_pars - Простой парсер новых объявлений на avito.ru

## Описание
Этот скрипт парсит Avito.ru по заданным запросам, записывает полученные данные в JSON-файл и отправляет их в Telegram. При последующих проверках, если результаты поиска обновтлись, он также добавляет новые записи в JSON и отправляет их в мессейджер. Провека проходит только по первым страницам указанных запросов.

## Требования
* Python 3.x
* Selenium
* BeautifulSoup
* requests

## Начальные параметры
Перед запуском скрипта убедитесь, что вы установили все необходимые библиотеки и задали следующие начальные параметры:
- Токен Вашего бота Telegram
- Токен Вашенр Avito профиля
- Перечень запросов, которые необходимо проверять при каждом проходе цикла речека
- ID чата Telegram, куда бот будет направлять сообщения об обновлении результатов поиска
- Время между проверками

## Использование
1. Установите скрипт себе на ПК.  
`$ git clone git@github.com:<ВАШ_GITHUB>/avito_pars.git`
2. Установите зависимости.  
`$ pip install -r requirements.txt`
3. Пропишите токены профиля Avito, вашего бота Telegram, ID чата, куда бот должен направлять сообщение об обновления, а также интересующие Вас запросы к авито и время между речеками.
4. Запустите скрипт avito_parser.py.  
`$ python avito_parser.py`

## Автор:
Кирилишин Алексей  
(alexkak@inbox.ru)