from pprint import pprint
import csv
import re

# Чтение CSV
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Сохраняем заголовки и данные отдельно
if contacts_list:
    headers = contacts_list[0]
    data_rows = contacts_list[1:]
else:
    headers = []
    data_rows = []

# ---------------------------------------------------------
# 1. Разбор ФИО (без регулярных выражений)
# ---------------------------------------------------------
def parse_fio(raw_parts):
    # Берём первые 3 элемента, убираем лишние пробелы
    parts = [p.strip() for p in raw_parts[:3]]
    # Убираем пустые строки
    parts = [p for p in parts if p]

    lastname = ""
    firstname = ""
    surname = ""

    if len(parts) == 3:
        lastname, firstname, surname = parts
    elif len(parts) == 2:
        lastname = parts[0]
        io_parts = parts[1].split(" ", 1)  # разбиваем только по первому пробелу
        if len(io_parts) == 2:
            firstname, surname = io_parts
        else:
            firstname = io_parts[0]  # если слитно или только имя
    elif len(parts) == 1:
        lastname = parts[0]

    return lastname, firstname, surname

# ---------------------------------------------------------
# 2. Нормализация телефона (с регулярными выражениями)
# Формат: +7(999)999-99-99 или +7(999)999-99-99 доб.9999
# ---------------------------------------------------------
def normalize_phone(phone):
    if not phone:
        return ""

    # Оставляем цифры, +, и буквы для "доб."
    cleaned = re.sub(r"[^\d\+\доб.]", "", phone.lower())

    # Ищем добавочный номер: доб.123 или доб 123
    ext_match = re.search(r"доб\.?\s*(\d+)", cleaned)
    extension = ext_match.group(1) if ext_match else None

    # Оставляем только цифры
    digits_only = re.sub(r"\D", "", cleaned)

    # Если начинается с 8, заменяем на 7
    if digits_only.startswith("8"):
        digits_only = "7" + digits_only[1:]

    # Проверяем, что получилось 11 цифр и начинается с 7
    if len(digits_only) == 11 and digits_only.startswith("7"):
        base = digits_only
    else:
        # Если формат не похож на российский номер, возвращаем как есть
        return phone

    # Форматируем: +7(XXX)XXX-XX-XX
    formatted = f"+7({base[1:4]}){base[4:7]}-{base[7:9]}-{base[9:11]}"

    if extension:
        formatted += f" доб.{extension}"

    return formatted

# ---------------------------------------------------------
# Обработка строк
# ---------------------------------------------------------
processed_rows = []
for row in data_rows:
    # Гарантируем, что в строке минимум 7 колонок
    while len(row) < 7:
        row.append("")

    raw_lastname, raw_firstname, raw_surname = row[0], row[1], row[2]
    organization = row[3]
    position = row[4]
    phone = row[5]
    email = row[6]

    lastname, firstname, surname = parse_fio([raw_lastname, raw_firstname, raw_surname])
    normalized_phone = normalize_phone(phone)

    processed_rows.append([lastname, firstname, surname, organization, position, normalized_phone, email])

# ---------------------------------------------------------
# 3. Объединение дублей по ФИО (Фамилия + Имя)
# ---------------------------------------------------------
merged_contacts = {}

for row in processed_rows:
    lastname, firstname, surname, org, pos, phone, email = row
    # Ключ для поиска дублей: (фамилия, имя) в нижнем регистре, без лишних пробелов
    key = (lastname.strip().lower(), firstname.strip().lower())

    if key not in merged_contacts:
        merged_contacts[key] = {
            "lastname": lastname,
            "firstname": firstname,
            "surname": surname,
            "organization": org,
            "position": pos,
            "phone": phone,
            "email": email,
        }
    else:
        existing = merged_contacts[key]
        # Заполняем пустые поля из новой строки
        if not existing["surname"] and surname:
            existing["surname"] = surname
        if not existing["organization"] and org:
            existing["organization"] = org
        if not existing["position"] and pos:
            existing["position"] = pos
        if not existing["phone"] and phone:
            existing["phone"] = phone
        if not existing["email"] and email:
            existing["email"] = email

# Преобразуем обратно в список списков для CSV
final_contacts_list = [headers]
for key, data in merged_contacts.items():
    final_contacts_list.append([
        data["lastname"],
        data["firstname"],
        data["surname"],
        data["organization"],
        data["position"],
        data["phone"],
        data["email"],
    ])

# Для проверки раскомментировать
# pprint(final_contacts_list)

# ---------------------------------------------------------
# TODO 2: запись результата в phonebook.csv
# ---------------------------------------------------------
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)
