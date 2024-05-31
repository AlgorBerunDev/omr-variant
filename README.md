### Установка и запуск проекта

#### 1. Установка зависимостей с помощью `requirements.txt`

Если у вас уже установлен Python и pip, вы можете установить все зависимости из файла `requirements.txt`.

1. Откройте терминал и перейдите в директорию вашего проекта:

   ```bash
   cd ~/www/work/omr-variant
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

#### 2. Запуск проекта

Предположим, что основной файл для запуска вашего проекта - `main.py`.

1. В терминале, находясь в корневом каталоге проекта, выполните:
   ```bash
   python main.py
   ```

### Использование Docker

#### 1. Создание Docker образа

Если у вас есть Dockerfile, вы можете создать Docker образ и запустить контейнер.

1. Перейдите в директорию вашего проекта:

   ```bash
   cd ~/www/work/omr-variant
   ```

2. Постройте Docker образ:
   ```bash
   docker build -t omr-variant .
   ```

#### 2. Запуск Docker контейнера

После создания образа вы можете запустить контейнер.

1. Запустите контейнер:
   ```bash
   docker run -it --name omr-variant-container omr-variant
   ```

### Пример Dockerfile

Если у вас нет Dockerfile или вы хотите проверить его корректность, вот пример Dockerfile для Python проекта:

```Dockerfile
# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "main.py"]
```

### Пример `requirements.txt`

Убедитесь, что ваш файл `requirements.txt` содержит все необходимые зависимости. Пример:

```
numpy==1.21.0
pandas==1.3.0
opencv-python==4.5.3.56
```

### Запуск Jupyter Notebook

Если вы хотите запустить Jupyter Notebook, например, `omr.ipynb`:

1. Установите Jupyter Notebook, если он еще не установлен:

   ```bash
   pip install notebook
   ```

2. Запустите Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

3. Откройте `omr.ipynb` в веб-интерфейсе Jupyter.
