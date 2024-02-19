# -*- coding utf-8 -*-

import csv
import click
import os

# Файл для хранения данных
CSV_FILE: str = "contacts.csv"


def read_contacts() -> list:
    """
    Читает контакты из CSV файла.

    Returns:
        list: Список словарей, каждый словарь представляет контакт, содержащий информацию о фамилии, имени,
        отчестве, организации, рабочем и личном номерах телефонов.

    Notes:
        Если файл не существует или пустой, возвращает пустой список.
    """
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    return []


def save_contacts(contacts: list) -> None:
    """
    Сохраняет контакты в CSV файл.

    Args:
        contacts (list): Список словарей, представляющих контакты. Каждый словарь должен содержать информацию о фамилии,
        имени, отчестве, организации, рабочем и личном номерах телефонов.

    Returns:
        None

    Side Effects:
        Сохраняет контакты в CSV файл, если файл существует, перезаписывает его. Каждая строка в файле
        представляет один контакт.

    Raises:
        ValueError: Если переданный аргумент `contacts` не является списком.
    """
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Surname', 'Name', 'Patronymic', 'Organization', 'Work Phone', 'Personal Phone']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)
    click.secho("Изменения успешно сохранены в файл.", fg='green')


def edit_contact(contact: dict, contacts: list) -> None:
    """
    Редактирует существующий контакт.

    Args:
        contact (dict): Словарь, представляющий редактируемый контакт. Содержит информацию о фамилии, имени,
        отчестве, организации, рабочем и личном номерах телефонов.

        contacts (list): Список словарей, представляющих все контакты.

    Returns:
        None

    Side Effects:
        Редактирует переданный контакт в списке контактов и сохраняет изменения в CSV файле.

    Raises:
        ValueError: Если переданный аргумент `contact` не является словарем или `contacts` не является списком.
    """
    for field in contact.keys():
        new_value = click.prompt(f"Текущее значение {field} '{contact[field]}' - введите новое значение или нажмите Enter, чтобы оставить без изменений", default=contact[field], show_default=False)
        contact[field] = new_value
    save_contacts(contacts)
    click.secho(f"Контакт '{contact['Name']}' успешно отредактирован.", fg='green')


def delete_contact(contact: dict, contacts: list) -> None:
    """
    Удаляет указанный контакт из списка контактов.

    Args:
        contact (dict): Словарь, представляющий удаляемый контакт. Содержит информацию о фамилии, имени,
        отчестве, организации, рабочем и личном номерах телефонов.

        contacts (list): Список словарей, представляющих все контакты.

    Returns:
        None

    Side Effects:
        Удаляет переданный контакт из списка контактов и сохраняет изменения в CSV файле.

    Raises:
        ValueError: Если переданный аргумент `contact` не является словарем или `contacts` не является списком.
    """
    if click.confirm(f"Вы уверены, что хотите удалить контакт '{contact['Name']}'?", default=False):
        try:
            contacts.remove(contact)
            save_contacts(contacts)
            click.secho(f"Контакт '{contact['Name']}' успешно удален.", fg='red')
        except ValueError:
            click.secho("Ошибка при удалении контакта. Контакт не найден.", fg='red')
    else:
        click.secho("Удаление отменено.", fg='yellow')


@click.group()
def contacts():
    """Управление телефонным справочником"""
    pass


@click.command(help="Добавление нового контакта")
@click.option('--surname', prompt='Фамилия', help='Фамилия контакта')
@click.option('--name', prompt='Имя', help='Имя контакта')
@click.option('--patronymic', prompt='Отчество', help='Отчество контакта')
@click.option('--organization', prompt='Организация', help='Название организации')
@click.option('--work_phone', prompt='Рабочий', help='Рабочий номер')
@click.option('--personal_phone', prompt='Личный', help='Личный номер')
def add(surname: str, name: str, patronymic: str, organization: str,
        work_phone: str, personal_phone: str) -> None:
    """
    Добавляет новый контакт в справочник.

    Args:
        surname (str): Фамилия контакта.
        name (str): Имя контакта.
        patronymic (str): Отчество контакта.
        organization (str): Название организации контакта.
        work_phone (str): Рабочий номер телефона контакта.
        personal_phone (str): Личный номер телефона контакта.

    Returns:
        None

    Side Effects:
        Добавляет новый контакт в справочник и сохраняет изменения в файле CSV.

    """
    new_contact = {
        "Surname": surname,
        "Name": name,
        "Patronymic": patronymic,
        "Organization": organization,
        "Work Phone": work_phone,
        "Personal Phone": personal_phone
    }
    contacts = read_contacts()
    contacts.append(new_contact)
    save_contacts(contacts)
    click.secho(
        f"Контакт успешно добавлен: {surname} {name} {patronymic}, Организация: {organization}, Рабочий: {work_phone}, Личный: {personal_phone}",
        fg='green')


def edit_or_delete_contact(filtered_contacts, contacts):
    """
    Предлагает пользователю редактировать или удалить выбранный контакт.

    Args:
        filtered_contacts (list): Отфильтрованный список контактов.
        contacts (list): Список всех контактов.

    Returns:
        None

    """
    prompt_text_confirm = click.style("Хотите ли вы отредактировать или удалить один из этих контактов?", fg='blue')
    if filtered_contacts and click.confirm(prompt_text_confirm):
        prompt_text_action = click.style("Введите 'edit' для редактирования или 'del' для удаления контакта", fg='blue')
        action = click.prompt(prompt_text_action, type=str)

        prompt_text_choice = click.style("Введите номер контакта", fg='blue')
        choice = click.prompt(prompt_text_choice, type=int)

        if 0 < choice <= len(filtered_contacts):
            if action.lower() == 'edit':
                edit_contact(filtered_contacts[choice - 1], contacts)
            elif action.lower() == 'del':
                delete_contact(filtered_contacts[choice - 1], contacts)
            else:
                click.secho("Неверное действие.", fg='red')
        else:
            click.secho("Неверный выбор.", fg='red')
    else:
        click.secho("Поиск завершен без действий.", fg='yellow')


@click.command(help="Отображение списка всех контактов")
@click.option('--page', default=1, help='Номер страницы для отображения. По умолчанию: 1')
@click.option('--per_page', default=10, help='Количество контактов на страницу. По умолчанию: 10')
def list_contacts(page: int, per_page: int) -> None:
    """
    Отображает список всех контактов с возможностью редактирования и удаления.

    Args:
        page (int): Номер страницы для отображения. По умолчанию: 1.
        per_page (int): Количество контактов на страницу. По умолчанию: 10.

    Returns:
        None

    Side Effects:
        Отображает список всех контактов, разбитый на страницы. Каждая страница содержит указанное количество контактов.
        Если контактов нет на выбранной странице, выводится соответствующее сообщение.
        Предоставляет возможность редактирования и удаления контактов.

    """
    contacts = read_contacts()
    start = (page - 1) * per_page
    end = min(start + per_page, len(contacts))
    for i, contact in enumerate(contacts[start:end], start=start + 1):
        click.echo(f"{i}. {contact['Surname']} {contact['Name']} {contact['Patronymic']} - {contact['Organization']} - {contact['Work Phone']}, {contact['Personal Phone']}")
    if not contacts[start:end]:
        click.secho("На этой странице контактов нет.", fg='red')
    else:
        edit_or_delete_contact(contacts[start:end], contacts)


@click.command(help="Поиск контактов с возможностью редактирования и удаления")
@click.option('--surname', default=None, help='Фамилия контакта')
@click.option('--name', default=None, help='Имя контакта')
@click.option('--patronymic', default=None, help='Отчество контакта')
@click.option('--organization', default=None, help='Организация контакта')
@click.option('--work_phone', default=None, help='Рабочий телефон контакта')
@click.option('--personal_phone', default=None, help='Личный телефон контакта')
def search(surname, name, patronymic, organization, work_phone, personal_phone):
    """
    Поиск контактов с возможностью редактирования и удаления.

    Аргументы:
        surname (str): Фамилия контакта.
        name (str): Имя контакта.
        patronymic (str): Отчество контакта.
        organization (str): Организация контакта.
        work_phone (str): Рабочий телефон контакта.
        personal_phone (str): Личный телефон контакта.
    """
    contacts = read_contacts()
    filtered_contacts = [contact for contact in contacts if
                         (surname is None or contact['Surname'].lower() == surname.lower()) and
                         (name is None or contact['Name'].lower() == name.lower()) and
                         (patronymic is None or contact['Patronymic'].lower() == patronymic.lower()) and
                         (organization is None or contact['Organization'].lower() == organization.lower()) and
                         (work_phone is None or contact['Work Phone'] == work_phone) and
                         (personal_phone is None or contact['Personal Phone'] == personal_phone)]

    if not filtered_contacts:
        click.secho("Контакты не найдены.", fg='red')
    else:
        for i, contact in enumerate(filtered_contacts, 1):
            click.echo(f"{i}. {contact['Surname']} {contact['Name']} {contact['Patronymic']} - {contact['Organization']} - {contact['Work Phone']}, {contact['Personal Phone']}")
        edit_or_delete_contact(filtered_contacts, contacts)


# Добавление команд в группу
contacts.add_command(add)
contacts.add_command(list_contacts)
contacts.add_command(search)

if __name__ == '__main__':
    contacts()
