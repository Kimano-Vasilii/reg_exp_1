from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

import re


def format_phone(phone):
    # Извлекаем только цифры из номера телефона
    digits = re.sub(r'\D', '', phone)
    # Проверяем длину номера телефона
    if len(digits) == 10:
        # Форматируем номер телефона в формат +7 (999) 999-99-99
        return f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"
    elif len(digits) == 11:
        # Форматируем номер телефона с добавочным номером в формат +7 (999) 999-99-99 доб. 9999
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]} доб. {digits[-4:]}"
    else:
        # Если номер телефона не соответствует ожидаемому формату, возвращаем его без изменений
        return phone

# Приведение ФИО в нужный формат и объединение дублирующихся записей о человеке
contacts_list['lastname'] = contacts_list.apply(lambda row: ' '.join(row['ФИО'].split()[:1]), axis=1)
contacts_list['firstname'] = contacts_list.apply(lambda row: ' '.join(row['ФИО'].split()[1:2]), axis=1)
contacts_list['surname'] = contacts_list.apply(lambda row: ' '.join(row['ФИО'].split()[2:]), axis=1)
contacts_list['phone'] = contacts_list['phone'].apply(format_phone)

# Удаление дублирующихся записей о человеке
data = contacts_list.drop_duplicates(subset=['lastname', 'firstname', 'surname'])

# Сохраняем обновленные данные в файл
data.to_csv('updated_address_book.csv', index=False)

