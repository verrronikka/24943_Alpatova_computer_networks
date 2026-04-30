## Задача 5

- Тип задачи: DOCKER

Краткое описание задачи
Создать два контейнера и настроить связь между ними


## Создание Dockerfile

```
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## Сборка моего кода

```
docker build -t pinterest-api .
```

## Запуск базы данных и создание сети

```
docker volume create pinterest-db-volume
docker network create pinterest-network

docker run -d \
--name pinterest-postgres \
-e POSTGRES_PASSWORD=12345 \
-e POSTGRES_DB=pinterest_db \
--mount type=volume,src=pinterest-db-volume,dst=/var/lib/postgresql/data \
--network=pinterest-network postgres:15
```

## Запуск моего кода с той же сетью

```
docker run -d \
--name pinterest-api \
-p 8001:8001 \
--network=pinterest-network \
--cap-add=SYS_ADMIN \
-e DATABASE_URL=postgresql://postgres:12345@pinterest-postgres:5432/pinterest_db pinterest-api
```

## Создание пустой таблицы

```
docker exec -it pinterest-postgres psql -U postgres -d pinterest_db -c "
CREATE TABLE IF NOT EXISTS pins (
    id SERIAL PRIMARY KEY,
    path VARCHAR(500),
    url VARCHAR(500) UNIQUE,
    style VARCHAR(100),
    tag VARCHAR(100),
    title TEXT,
    author VARCHAR(200),
    save_count VARCHAR(50),
    comment_count VARCHAR(50),
    downloaded BOOLEAN,
    error TEXT
);"
```

## Перезапуск контейнера с кодом

```
docker restart pinterest-api
```

## Проверка

```
curl "http://127.0.0.1:8001/parse?styles=y2k&tags=outfit&max_pins=2&scrolls=2"
```

```
curl http://127.0.0.1:8001/get_data
```
