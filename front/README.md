# Дебош продакшн React App


## Запуск через Docker

В директории нужно вызвать

### `docker build --file Dockerfile --tag docker-react-image:1.0 .`

и затем

### `docker run -d -p 3000:80 --name docker-react-container docker-react-image:1.0`