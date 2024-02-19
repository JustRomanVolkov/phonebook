# Используем базовый образ Python
FROM python:slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы приложения в рабочую директорию
COPY requirements.txt .
COPY phonebook.py .
COPY contacts.csv .

RUN chmod +x phonebook.py

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Определение переменной среды для файла с данными
ENV CSV_FILE="contacts.csv"

# Команда для запуска приложения
CMD ["python", "phonebook.py"]
