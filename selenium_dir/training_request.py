# import requests
# from bs4 import BeautifulSoup as bs

# r = requests.get('https://pythonworld.ru/samouchitel-python')
# text = r.text

# soup = bs(text, "html.parser")

# # получить первый элемент, то можно получить так
# print(soup.title.text)
# # можно получить так
# print(soup.select("head > title")[0].text)
# # получить родителя
# print(soup.title.parent.name)
# # получить тег
# print(soup.title.name)

# print("---------------------------------------------------------")
# # список мета-тегов
# meta = soup.select("head > meta")
# for m in meta:
#     print(m)
#     # attrs - выдает словарь всех аттрибутов тега: {"attr": "value", ...}
#     for att, val in m.attrs.items():
#         print("....", att, val)
#     # можно удалить аттрибут
#     # del m['id']

# print("---------------------------------------------------------")
# # поиск по классу
# a1 = soup.select("p.strikeout.body")

# ==============================================================================

# import requests
# from bs4 import BeautifulSoup as bs

# r = requests.get('https://pythonworld.ru/samouchitel-python')
# text = r.text

# soup = bs(text, "html.parser")

# # вложенный поиск
# print(soup.find("head").find("title"))

# # поиск первого элемента
# print(soup.find(id="link3"))

# ==============================================================================

# import requests
# from bs4 import BeautifulSoup as bs

# r = requests.get('https://pythonworld.ru/samouchitel-python')
# text = r.text

# soup = bs(text, "html.parser")

# print("---------------------------------------------------------")
# # все дети
# for child in soup.head.children:
#     print(child)
# # все родители у первой ссылки
# for parent in soup.find_all('a')[0].parents:
#     print(parent.name)
# # предыдущий тег на уровне
# print(soup.find_all('meta')[0].previous_sibling)
# # следующий тег на уровне
# print(soup.find_all('meta')[0].next_sibling)

# # сразу все по тегам в виде списка
# print(soup.find_all(["a", "b"]))

# # если нужны все элементы по атрибуту
# news_list1 = soup.find_all('h2', id='post_title')
# # если нужны все элементы по классу
# news_list2 = soup.find_all('h2', class_='post__title')

# # все по идентификатору
# ids = soup.find_all(id="link2")

# # все элементы с href через регулярку
# import re
# a1 = soup.find_all(href=re.compile("elsie"))

# # все у кого есть атрибут id
# a2 = soup.find_all(id=True)

# # все ссылки
# for link in soup.find_all('a'):
#     print(link.get('href'))

# # поиск по нескольким аттрибутам в виде словаря
# a3 = soup.find_all(attrs={"data-foo": "value"})


# # функция-фильтр поиска элементов
# def has_six_characters(css_class):
#     return css_class is not None and len(css_class) == 3


# soup.find_all(class_=has_six_characters)

# # установить ограничение на количество элементов
# a4 = soup.find_all("a", limit=2)

# =============================================================================
