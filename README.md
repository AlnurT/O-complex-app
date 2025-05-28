## Веб-приложение для получения погоды для определённого города

В данной работе использовалось:
- веб фреймворк FastAPI
- база данных PostgreSQL
- реализована работа со статическими файлами и шаблонами
- сделано автодополнение при вводе города
- предложен просмотр погоды для города, который пользователь просматривал при последнем посещении сайта
- сохранена история поиска городов, для показа количества запросов по городу или городам (без JWT и сохранения ID пользователей)
- написаны автотесты
- всё помещено в докер контейнер

## Клонирование репозитория
```
git clone https://github.com/AlnurT/O-complex-app.git
cd O-complex-app
```
Создание файла .env.docker по примеру .env-example
```
cp .env-example .env.docker
```
Если нужно, редактируем параметры для базы данных в файле .env.docker

## Подготовка сервера
### git
```
sudo apt-get update
sudo apt-get install git
```

### docker
Можно воспользоваться инструкцией: https://docs.docker.com/engine/install/ubuntu/
или скопировать код ниже
```
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Запуск приложения
Сборка и запуск контейнера с приложением и базой данных PostgreSQL
```
docker-compose up -d --build
```
### Доступ к приложению
Откройте браузер и переходим по адресу:
http://localhost:8000
