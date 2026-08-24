import csv
import re
from pprint import pprint

# Чтение исходной адресной книги
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0] if contacts_list else []
data = contacts_list[1:] if contacts_list else []

def parse_fio(raw_fio_parts):
    """
    Принимает список из первых 3 полей строки (могут быть пустыми).
    Возвращает (lastname, firstname, surname).
    
    Обрабатывает случаи:
      - «Усольцев Олег Валентинович» (всё в первом поле)
      - «Мартиняхин,Виталий,Геннадьевич» (через запятые)
      - «Лукина Ольга» (без отчества)
      - смешанные варианты
    """
    # Сначала объединим все непустые части и почистим от лишних пробелов
    raw = " ".join(p.strip() for p in raw_fio_parts if p.strip())
    if not raw:
        return "", "", ""

    # Если есть запятые — пробуем разбить по ним (случай «Фамилия,Имя,Отчество»)
    if "," in raw:
        parts = [p.strip() for p in raw.split(",")]
        # Оставляем только непустые
        parts = [p for p in parts if p]
        if len(parts) == 1:
            # Если после split осталась одна часть — обрабатываем как единый блок
            return parse_single_fio_block(parts[0])
        elif len(parts) == 2:
            return parts[0], parts[1], ""
        else:
            # 3 и более частей: считаем, что это Фамилия, Имя, Отчество (и дальше игнорируем)
            return parts[0], parts[1], parts[2]

    # Если запятых нет — считаем, что это «Фамилия Имя Отчество» или «Фамилия Имя»
    return parse_single_fio_block(raw)


def parse_single_fio_block(block):
    """
    Разбивает строку вида «Фамилия Имя [Отчество]» на три поля.
    """
    parts = block.strip().split()
    if len(parts) == 0:
        return "", "", ""
    if len(parts) == 1:
        # Только фамилия
        return parts[0], "", ""
    if len(parts) == 2:
        # Фамилия + Имя
        return parts[0], parts[1], ""
    # 3+ частей: Фамилия + Имя + Отчество (+возможные лишние слова)
    lastname = parts[0]
    firstname = parts[1]
    surname = " ".join(parts[2:])
    return lastname, firstname, surname


def normalize_phone(phone):
    """
    Приводит телефон к формату:
      +7(999)999-99-99
      или
      +7(999)999-99-99 доб.9999
    
    Важно: цифры добавочного номера НЕ должны попадать в основной номер.
    """
    if not phone:
        return ""

    # Ищем добавочный номер ДО очистки: ищем паттерны «доб», «ext», «x», «#» и т.п.
    ext_match = re.search(r"(?:доб|ext|x|#)\s*(\d+)", phone, re.IGNORECASE)
    extension = ext_match.group(1) if ext_match else None

    # Очищаем строку от всего, кроме цифр и плюса
    digits_only = re.sub(r"\D", "", phone)

    # Если нашли добавочный — нужно убрать его цифры из digits_only.
    # Самый простой способ: удалить из исходной строки фрагмент с добавочным,
    # затем снова оставить только цифры.
    if extension:
        # Удаляем из phone фрагмент, который совпал с ext_match
        phone_without_ext = phone[:ext_match.start()] + phone[ext_match.end():]
        digits_only = re.sub(r"\D", "", phone_without_ext)

    # Нормализуем к +7, если начинается с 8 и длина 11
    if digits_only.startswith("8") and len(digits_only) == 11:
        digits_only = "7" + digits_only[1:]
    elif digits_only.startswith("7") and len(digits_only) == 11:
        pass  # уже ок
    else:
        # Если длина не 11 — возвращаем пустую строку или можно оставить как есть
        # Для задания лучше вернуть пустую, чтобы не сохранять мусор
        return ""

    # Формируем +7(XXX)XXX-XX-XX
    main_number = f"+7({digits_only[1:4]}){digits_only[4:7]}-{digits_only[7:9]}-{digits_only[9:]}"

    if extension:
        return f"{main_number} доб.{extension}"
    return main_number


# Обработка контактов
processed = []
for row in data:
    # Берём первые 3 поля как потенциальное ФИО
    raw_fio_parts = row[:3]
    lastname, firstname, surname = parse_fio(raw_fio_parts)

    organization = row[3] if len(row) > 3 else ""
    position = row[4] if len(row) > 4 else ""
    phone = normalize_phone(row[5] if len(row) > 5 else "")
    email = row[6] if len(row) > 6 else ""

    processed.append([lastname, firstname, surname, organization, position, phone, email])

# Дедупликация: объединяем дубли по lastname + firstname (нормализованные)
merged = {}
for contact in processed:
    key = (contact[0], contact[1])  # lastname, firstname
    if key not in merged:
        merged[key] = contact
    else:
        existing = merged[key]
        # Заполняем пустые поля из новой записи
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

final_contacts = [header] + list(merged.values())

pprint(final_contacts)

# Сохранение в новый файл
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts)
