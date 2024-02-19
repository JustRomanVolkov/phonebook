# Телефонный справочник

Данный проект представляет собой простое приложение для управления телефонным справочником. 
Вы можете добавлять, редактировать, удалять и просматривать контакты в удобном интерфейсе командной строки.

## Установка

1. Склонируйте репозиторий на ваш компьютер:

```bash
git clone https://github.com/TheRomanVolkov/phonebook.git
```
2. Перейдите в каталог проекта:

```bash
cd phonebook
```
3. Запустите phonebook.py

## Список доступных команд:

- add: Добавление нового контакта.
- list-contacts: Отображение списка всех контактов(с возможностью редактирования и удаления).
- search: Поиск контактов (с возможностью редактирования и удаления).

### Примеры использования:

```bash
python phonebook.py add --surname "Иванов" --name "Иван" --work_phone "1234567890"
python phonebook.py list-contacts --page 2
python phonebook.py search --surname "Петров"
```

## Использование с Docker'ом

Соберите Docker:
```bash
docker build -t phonebook-app .
```
После успешной установки вы можете запустить приложение с помощью Docker. Вот примеры команд:

- Добавление нового контакта:
```bash
docker run -it --rm phonebook-app python phonebook.py add
```

- Просмотр списка всех контактов:
```bash
docker run -it --rm phonebook-app python phonebook.py list-contacts
 ```

- Поиск контактов с возможностью редактирования и удаления:
```bash
docker run -it --rm phonebook-app python phonebook.py search
```
