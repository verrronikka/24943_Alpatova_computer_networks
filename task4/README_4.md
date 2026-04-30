## Задача 4

- Тип задачи: API + SQL

Краткое описание задачи
Поднять точку на API, где запуститься парсер и запишет данные в postgres, из которого мы будем извлекать данные и записывать в json.


## Стркутура директории task4

task4/

├── data/

│   └── /styles/tags

├── Dockerfile

├── main.py

├── parser.py

├── README.md

├── requirements.txt

└── state.json

## Development

- Создание и активация виртуального окружения:

```bash
python -m venv .venv
source .venv/bin/activate
```

- Зависимости
```bash
pip install -r requirements.txt
```

## Как воспроизвести

Команда запуска:
```
uvicorn main:app --reload
```

## Проверка

```
http://127.0.0.1:8000/parse?styles=y2k&tags=outfit&max_pins=2&scrolls=2
```

```

```
http://127.0.0.1:8000/get_data
```