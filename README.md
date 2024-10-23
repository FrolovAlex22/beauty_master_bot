# Проект beauty_master_bot

## Описание

### Телеграм-Бот ассистент для мастеров в бьюти сфере ###

Бот имеет 2 основных меню:

1. Меню администратора
Через меню администратора можно добавлять записи клиентов в выбранные даты. Для отображения календаря сделана inline клавиатура с возможностью выбора даты и месяца для записи. Есть возможность вести учет материала добавляя и изменяя количество на складе, так же можно распечатать список материалов для покупки, остаток на складе которых равен или менее одного. Реализованная возможность вести заметки для постов в соц.сетях, посты можно помечать как "опубликованные" в таком случае они будут отображаться у обычных пользователей, "не опубликованные посты" доступны только администратору.
Так же администратор может менять баннеры для некоторых меню.

2. Меню пользователя
Обычнй пользователь может просматривать список записей по датам, оставлять заявку мастеру для обратной связи, через inline клавиатуру - календарь. Пользователь может ознакомиться с продукцией для домашнего ухода, оставить заявку на покупку. Информация о продукции поступает через пагинатор. Пользователь может прочитать опубликованные мастером посты.

## Технологии
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4-blue)](https://docs.aiogram.dev/en/latest/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?logo=PostgreSQL&logoColor=white/)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue)](https://docs.sqlalchemy.org/en/20/)
[![pydentic](https://img.shields.io/badge/pydentic-blue)](https://pydantic-docs.helpmanual.io/)


## Запуск проекта локально

Клонируйте репозиторий и перейдите в него:

```
git clone git@github.com:Studio-Yandex-Practicum/random_coffee_bot_anna.git
cd random_coffee_bot_anna
```

Создайте виртуальное окружение:
```
py -3.11 -m venv venv
```
Активируйте виртуальное окружение:
```
Windows: source venv/Scripts/activate
Linux/macOS: source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
В корне проекта создайте файл .env и поместите в него:
```
BOT_TOKEN='<токен вашего бота>'
ADMIN_IDS='<id администратора>'
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/beauty_bot
```
Запустите бота (из корня проекта):
```
main.py
<!-- ```
## Запуск проекта на сервере
Клонируйте репозиторий и перейдите в него:
```
git clone git@github.com:Studio-Yandex-Practicum/random_coffee_bot_anna.git
cd random_coffee_bot_anna
```
Создайте виртуальное окружение:
```
python3.11 -m venv venv
```
Активируйте виртуальное окружение:
```
source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
В корне проекта создайте файл .env и поместите в него:
```
BOT_TOKEN='<токен вашего бота>'
DATABASE_URL='sqlite+aiosqlite:///./random_coffe_bot.db'
GEN_ADMIN_ID=<телеграмм id главного администратора>
```
Создайте базу данных, применив миграции (из корня проекта):
```
alembic upgrade head
```
Создайте юнита для автоматического перезапуска бота при перезагрузке сервера:
```
nano file_name.service
```
Поместите в файл следующее:
```
[Unit]
Description=<описание вашего бота>
After=multy-user.target

[Service]
Type=simple
ExecStart=/<путь до репозитория проекта>/random_coffee_bot_anna/venv/bin/python3.11 /<путь до репозитория проекта>/random_coffee_bot_anna/bot.py
WorkingDirectory=/<путь до репозитория проекта>/random_coffee_bot_anna
Restart=always

[Install]
WantedBy=multi-user.target
```
Последовательно выполните следующие команды:
```
sudo cp file_name.service /etc/systemd/system
sudo systemctl enable file_name.service
sudo systemctl restart file_name.service
```
Для перезапуска бота на сервере используйте команду:
```
sudo systemctl restart file_name.service
```
Поменять дни и время рассылки можно в bot_app/core/constants.py
```
class MailingInt(IntEnum):
    MAIL_TO_COUPLES_HOUR = 10  - время рассылки для пар (часы)
    MAIL_TO_COUPLES_MIN = 00 - время рассылки для пар (минуты)
    REMIND_MAIL_HOUR = 10  - время рассылки напоминания (часы)
    REMIND_MAIL_MIN = 00  - время рассылки напоминания (минуты)


class MailingStr(str, Enum):
    TRIGGER = 'cron'
    MAIL_TO_COUPLES_DAY = 'mon' - день расслыки для пар (принимает значения от 0 до 6, или mon, tue, wed, thu, fri, sat, sun, можно задать сразу несколько дней)
    REMIND_MAIL_DAY = 'thu' - день расслыки с напоминанием (принимает значения от 0 до 6, или mon, tue, wed, thu, fri, sat, sun,  можно задать сразу несколько дней)
``` -->


## Для связи:
mail: frolov.bsk@yandex.ru
Для связи tg: @frolov_bsk