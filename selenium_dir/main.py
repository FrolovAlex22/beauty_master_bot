import json
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium import webdriver



HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en;q=0.9",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36"
}

URL_FOR_SEARCH_MASTERS = {
    "hair reconstruction": "https://www.avito.ru/birsk/uslugi?cd=1&q=реконструкция+волос",
}

ATTEMPTS_TO_FIND_THE_MASTERS = 5



def get_href_data(url):

    r = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    print(r)

    city_masters = soup.find(
        "div",
        class_="items-items-kAJAg",
        attrs={"data-marker": "catalog-serp"}
    )
    master_cards = city_masters.find_all(attrs={"data-marker": "item"})

    masters_list = []

    for master in master_cards:
        try:
            href = master.find(attrs={"data-marker": "item-title"}).get("href")
            masters_list.append(href)
        except Exception as ex:
            print(ex)

    return masters_list


def get_master_info(master_url: str):
    driver = uc.Chrome()
    driver.implicitly_wait(5)

    try:
        driver.get(f"https://www.avito.ru{master_url}")
        name = driver.find_element(By.CLASS_NAME, "style-titleWrapper-Hmr_5").text
        print(name)
        # driver.get("https://www.ozon.ru/")
        time.sleep(4)
    except Exception as ex:
        print(ex)

    finally:
        driver.quit()


def search_masters(type_master: str):

    url = URL_FOR_SEARCH_MASTERS[type_master]
    masters_dict = None
    for i in range(ATTEMPTS_TO_FIND_THE_MASTERS):
        try:
            masters_dict = get_href_data(url)
            break
        except Exception as ex:
            print(ex)
        finally:
            time.sleep(2)

    for master in masters_dict:
        info = get_master_info(master)
        # r = requests.get(url=f"https://www.avito.ru{master}", headers=HEADERS)
        # print(f"Status~~~~~~~~~~~~~~~~~~~{r}")

def main():
    # get_href_data(URL_FOR_SEARCH_MASTERS["hair reconstruction"])
    # get_href_data()
    search_masters("hair reconstruction")
    # get_data("https://www.tury.ru/hotel/most_luxe.php")
    # get_data_with_selenium("https://www.tury.ru/hotel/most_luxe.php")


if __name__ == '__main__':
    main()
