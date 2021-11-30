Простой HTTP-прокси-сервер, запускаемый локально, который показывает содержимое
страниц [Hacker News](https://news.ycombinator.com). Прокси модицифирует текст
на страницах следующим образом: после каждого слова из шести букв добавляется
значок «™». При навигации по ссылкам, которые ведут на другие страницы HN,
браузер остается на адресе прокси. Используются библиотеки _aiohttp_
и _beautifulsoup4_.

Запускается командой `make setup && make start`.

Пример:

![screenshot](https://i.imgur.com/ilTnDM7.png)

### Prerequisites

* pipenv
* make

### Commands

* Setup a working environment using _Pipenv_

    `make setup`

* Start application server

    `make start`

* Run tests

    `make test`

* Run linter

    `make lint`

* List all available _Make_ commands

    `make help`
