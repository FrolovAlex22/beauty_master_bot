# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# # Может пригодиться !!!!!
# # чтобы окно не закрывалось
# o = Options()
# o.add_experimental_option("detach", True)

# browser = webdriver.Chrome(options=o)
# browser.get('http://selenium.dev/')

# # метод закрытия окна
# time.sleep(10)
# browser.close()

# ------------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver.get('http://selenium.dev/')

# ------------------------------------------------------------------------------

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# # чтобы окно не закрывалось
# o = Options()
# o.add_experimental_option("detach", True)

# browser = webdriver.Chrome(options=o)
# browser.get('http://selenium.dev/')

# # пишем код на JS для выполнения в браузере
# js = 'window.scrollTo(0, document.body.scrollHeight);'
# # и запускаем его
# browser.execute_script(js)
# ------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS

# чтобы окно не закрывалось
o = Options()
o.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=o)
browser.get('http://selenium.dev/')

# пишем код на JS для выполнения в браузере
js = 'window.scrollTo(0, document.body.scrollHeight);'
# и запускаем его
browser.execute_script(js)

main_page = browser.page_source
soup = BS(main_page, 'html.parser')
# а дальше разбираем контент

print(soup.prettify())
# prettify(), который возвращает отформатированный HTML. Он добавляет в код переносы строк и отступы для удобства чтения.
