import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver



HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en;q=0.9",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36"
}

def get_href_data(url):

    r = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    print(r)
    if soup:
        print("Подключение прошло успешно")

    city_masters = soup.find(
        "div",
        class_="items-items-kAJAg",
        attrs={"data-marker": "catalog-serp"}
    )


    with open("index.html", "w", encoding="utf-8") as file:
            # json.dump(master.text, file, indent=4, ensure_ascii=False)
        file.write(soup.text)

    master_cards = city_masters.find_all(attrs={"data-marker": "item"})

    # masters_list = {}

    for master in master_cards:
        master_info = []
        try:
            href = master.find(attrs={"data-marker": "item-title"}).get("href")
            print("href done")

        except Exception as ex:
            None

        if href:
            master_info.append(href)


        time.sleep(1)
        try:
            name = master.find(class_="style-root-uufhX").get("p").text
            master_info.append(name)
        except Exception as ex:
            None
        # if name:
        #     master_info.append(name)
        #     name = None

        print(master_info)
    # except Exception as ex:
    #     print("Ошибка во время сбора ссылок")
    #     print(ex)


def main():
    get_href_data("https://www.avito.ru/birsk/uslugi?cd=1&q=реконструкция+волос")
    # get_data("https://www.tury.ru/hotel/most_luxe.php")
    # get_data_with_selenium("https://www.tury.ru/hotel/most_luxe.php")


if __name__ == '__main__':
    main()