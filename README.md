### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```

git clone https://github.com/borzeman/api_yamdb

```

cd api_yamdb

```

Cоздать и активировать виртуальное окружение:

```

python3 -m venv env

```

```

source env/bin/activate

```

Установить зависимости из файла requirements.txt:

```

pip install -r requirements.txt

```

Создать файл ".env" и записать в нём SECRET_KEY

```

Выполнить миграции:

```

python3 manage.py migrate

```

Запустить проект:

```

python3 yatube_api/manage.py runserver

```