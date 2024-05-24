# Сбор и разметка данных (семинары)
# Урок 4. Парсинг HTML. XPath
# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
#
# Ваш код должен включать следующее:
#
# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.
#
# Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.
#
#
#
# С семинара, немного улучшить, и добавить в csv файл.
import csv
from lxml import html
import requests
from pprint import pprint

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15'}

url = "https://www.ebay.com"
link = "/b/Fishing-Equipment-Supplies/1492/bn_1851047"
session = requests.session()
response = session.get(url + link, headers=headers)
dom = html.fromstring(response.text)

items_list = []
items = dom.xpath("""//ul[@class="b-list__items_nofooter"]/li""")
for item in items:
    item_info = {}

    name = item.xpath(""".//h3[@class="s-item__title"]/text()""")
    link = item.xpath(""".//h3[@class="s-item__title"]/../@href""")
    price = item.xpath(""".//span[@class="s-item__price"]//text()""")
    add_info = item.xpath(""".//span[@class="NEGATIVE"]/text()""")

    item_info["name"] = name[0]
    item_info["link"] = link[0]
    item_info["price"] = price
    item_info["add_info"] = add_info
    items_list.append(item_info)


# У каждого, будет:
# Имя = name
# Ссылка = link
# Стоимость от = min price or price
# Стоимость до = max price or price_max
# Валюта = currency
# Продано = sales
# Осталось товаров = goods_remained
#
# После условий и действий над add_info, ключ удаляется.
# Добавляется currency, для обозначения какой валюты стоимость предмета/вещи
# Добавляется price_max, для обозначения максимальной стоимости предмета/вещи
# Добаляется sales и goods_remained, вместо add_info. Лучше добавить 2 ключа, чем помещать 2 разных ключа в один ключ.
for iteml in items_list:
    iteml["sales"] = None
    iteml["goods_remained"] = None
    iteml["price_max"] = None
    if "продано" in str(iteml["add_info"]):
        iteml["sales"] = iteml["add_info"][0].split(" ")[0].replace(u'\xa0', u'')
    elif "сталось" in str(iteml["add_info"]):
        iteml["goods_remained"] = iteml["add_info"][0].split(" ")[1].replace(u'\xa0', u'')

    del iteml["add_info"] # В любом случае удаляется, так как он нам не пригодится в будущем.

    if len(iteml["price"]) > 1:
        replace_split = (iteml["price"][0].replace(u'\xa0', u'').split(" "),
                         iteml["price"][-1].replace(u'\xa0', u'').split(" "))
        iteml["price"],iteml["price_max"] = (float(replace_split[0][0].replace(",",".")),float(replace_split[-1][0].replace(",",".")))
        iteml["currency"] = replace_split[0][-1].replace(".","")# if (replace_split[0][-1] == replace_split[-1][-1]) else (replace_split[0][-1], replace_split[-1][-1])
    else:
        replace_split = (iteml["price"][0].replace(u'\xa0', u'')).split(" ")
        iteml["price"] = float(replace_split[0].replace(",","."))
        iteml["currency"] = replace_split[1].replace(".","")


    print(iteml)

# https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
# https://ru.stackoverflow.com/questions/756119/чем-отличается-символ-xa0-от-простого-пробела
# Как удалить xa0 из строки.
# Проблема решена.
# Устранение лёгкое.
#
# https://stackoverflow.com/questions/18766955/how-to-write-utf-8-in-a-csv-file
# Как записать utf8 в csb файл.
# Проблема не решена.
# Устранение сложное.

# pprint(items_list)

# Имя = name
# Ссылка = link
# Стоимость от = min price or price
# Стоимость до = max price or price_max
# Валюта = currency
# Продано = sales
# Осталось товаров = goods_remained
with open('data_base.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'link', 'price', 'price_max', 'currency', 'sales', 'goods_remained']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()
    for i in items_list:
        sort_item = {n:str(i[n]).encode("utf-8").decode("utf-8") for n in fieldnames}
        print(sort_item)
        writer.writerow(sort_item)

    # writer.writerow({'name': 'Baked', 'link': 'Beans'})
    # writer.writerow({'name': 'Lovely', 'link': 'Spam'})
    # writer.writerow({'name': 'Wonderful', 'link': 'Spam'})

# При записи в data_base.csv, часть информации теряется.
# Символ ; не встречался в sort_item.
# Это довольно приоритетная проблема.