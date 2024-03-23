# PizzaMeow

## Запуск сервера
Для удобства создайте виртуальное окружение (если у вас его нет) `python -m venv venv`
Активируйте виртуальное окружение `./venv/bin/activate`
Установите зависимости `pip install -r requirements.txt`
Запустите сервер (надо находится в папке с проектом) `uvicorn server.app.__init__:app --reload`

Откройте в браузере ваш локальный сервер, документация будет находиться в относительном пути `/api/ui`
