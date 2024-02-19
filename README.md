# ���������� ����������

������ ������ ������������ ����� ������� ���������� ��� ���������� ���������� ������������. 
�� ������ ���������, �������������, ������� � ������������� �������� � ������� ���������� ��������� ������.

## ���������

1. ����������� ����������� �� ��� ���������:

```bash
git clone https://github.com/TheRomanVolkov/phonebook.git
```
2. ��������� � ������� �������:

```bash
cd phonebook
```
3. ��������� phonebook.py

## ������ ��������� ������:

- add: ���������� ������ ��������.
- list-contacts: ����������� ������ ���� ���������(� ������������ �������������� � ��������).
- search: ����� ��������� (� ������������ �������������� � ��������).

### ������� �������������:

```bash
python phonebook.py add --surname "������" --name "����" --work_phone "1234567890"
python phonebook.py list-contacts --page 2
python phonebook.py search --surname "������"
```

## ������������� � Docker'��

�������� Docker:
```bash
docker build -t phonebook-app .
```
����� �������� ��������� �� ������ ��������� ���������� � ������� Docker. ��� ������� ������:

- ���������� ������ ��������:
```bash
docker run -it --rm phonebook-app python phonebook.py add
```

- �������� ������ ���� ���������:
```bash
docker run -it --rm phonebook-app python phonebook.py list-contacts
 ```

- ����� ��������� � ������������ �������������� � ��������:
```bash
docker run -it --rm phonebook-app python phonebook.py search
```
