## REST-сервис (FastAPI)

REST-сервис просмотра текущей зарплаты и даты следующего
повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности, реализован метод где по логину и паролю
сотрудника будет выдан секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате выдается только при предъявлении валидного токена.

## Запуск сервиса
#### Склонируйте репозиторий с проектом
```
git clone https://github.com/DVSAWR/SHIFT.git
```
#### Установите зависимости (Poetry)
[Официальная документация Poetry](https://python-poetry.org/docs/#installing-with-pipx)
```
poetry install
```

#### Запустите тестирование (Pytest)
```
pytest
```

#### Запустите приложение (Uvicorn)
```
uvicorn main:app --reload
```
