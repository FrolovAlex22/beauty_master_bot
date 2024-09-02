# pip install fake_useragent

from bs4 import BeautifulSoup as BS
import requests
from fake_useragent import UserAgent

URL = "https://yandex.ru/search/?text=мастер+по+реконструкции+волос+бирск&lr=20689&clid=2270455&win=644"

# получаем сайт с передачей случайного user-agent
r = requests.get(URL)
# получаем весь текст-код сайта
text = r.text

# создаем парсера
soup = BS(text, "html.parser")
print(soup.title.text)
masters = []

master_data = soup.find_all("div", class_="bcard__address")
print(master_data)

# if master_data != []:
#     masters.extend(master_data)
#     print("YES")
# else:
#     print("empty")

with open("data3.csv", "w", encoding="utf-8") as f:
    f.write(master_data)
# ищем все элементы по исследованному тегу и классу
# news = soup.find_all("span", class_="main__feed__title")
# d = []
# for n in news:
#     # получаем ссылку на новость
#     link = n.parent.parent['href']
#     # получаем заголовок новости
#     header = n.text
#     d.append((header, link))
# я
# # делаем текст
# t = ''
# for i in d:
#     t += i[0] + ';' + i[1] + '\n'
# # заносим текст в файл
# with open("data1.csv", "w", encoding="utf-8") as f:
#     f.write(t)