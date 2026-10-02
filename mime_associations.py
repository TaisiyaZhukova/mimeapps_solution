from typing import Dict, List


# Список допустимых секций файла mimeapps.list.
# Он также используется для правильного порядка записи в файл.
SECTIONS = [
    "Default Applications",
    "Added Associations",
    "Removed Associations",
]


def read_associations(path: str) -> dict:
    """
    Читает файл mimeapps.list и преобразует его
    в структуру данных Python:

    {
        "Default Applications": {
            "text/plain": ["gedit.desktop"]
        },
        "Added Associations": {},
        "Removed Associations": {}
    }

    :param path: путь к файлу mimeapps.list
    :return: словарь ассоциаций
    """

    # Создаем пустую структуру с тремя секциями.
    # Если в файле какая-то секция отсутствует,
    # она всё равно будет существовать как пустой словарь.
    associations = {
        section: {}
        for section in SECTIONS
    }

    # Переменная для хранения текущей читаемой секции.
    # Она нужна, чтобы понимать, куда добавлять MIME-типы.
    current_section = None

    # Открываем файл для чтения.
    with open(path, "r", encoding="utf-8") as file:

        # Читаем файл построчно.
        for line in file:

            # Убираем пробелы и перенос строки.
            line = line.strip()

            # Пропускаем пустые строки и комментарии.
            if not line or line.startswith("#"):
                continue

            # Проверяем, является ли строка названием секции.
            # Например: [Default Applications]
            if line.startswith("[") and line.endswith("]"):

                # Извлекаем название секции без квадратных скобок.
                section_name = line[1:-1]

                # Запоминаем секцию только если она нам известна.
                if section_name in SECTIONS:
                    current_section = section_name
                else:
                    # Неизвестные секции игнорируем.
                    current_section = None

                continue

            # Если мы внутри нужной секции и строка содержит "=",
            # значит это описание MIME-типа.
            if current_section and "=" in line:

                # Делим строку на MIME-тип и список приложений.
                # Например: text/plain=gedit.desktop;code.desktop
                mime_type, applications = line.split("=", 1)

                # Разделяем приложения по символу ";" и удаляем пустые значения.
                apps = [
                    app.strip()
                    for app in applications.split(";")
                    if app.strip()
                ]

                # Сохраняем результат в словарь.
                associations[current_section][mime_type] = apps

    return associations


def merge_associations(old: dict, new: dict) -> dict:
    """
    Объединяет два словаря ассоциаций.

    Если один MIME-тип есть в обоих словарях,
    используется значение из new.

    Исходные словари old и new не изменяются.

    :param old: старые ассоциации
    :param new: новые ассоциации
    :return: объединенный словарь
    """

    # Создаем новый словарь результата.
    result = {}

    # Получаем все секции, которые есть хотя бы в одном словаре.
    all_sections = set(old.keys()) | set(new.keys())

    # Обрабатываем каждую секцию отдельно.
    for section in all_sections:

        # Создаем пустую секцию результата.
        result[section] = {}

        # Сначала копируем старые данные.
        if section in old:
            for mime_type, apps in old[section].items():

                # Используем copy(), чтобы не менять
                # исходные списки.
                result[section][mime_type] = apps.copy()

        # Затем добавляем новые данные.
        # Если MIME-тип уже существует,
        # новое значение заменит старое.
        if section in new:
            for mime_type, apps in new[section].items():
                result[section][mime_type] = apps.copy()

    return result


def write_associations(associations: dict, path: str) -> None:
    """
    Записывает словарь ассоциаций обратно в файл mimeapps.list.

    Секции записываются строго в порядке:
    Default Applications
    Added Associations
    Removed Associations

    :param associations: словарь ассоциаций
    :param path: путь для сохранения файла
    """

    # Открываем файл для записи.
    with open(path, "w", encoding="utf-8") as file:

        # Проходим по секциям в требуемом порядке.
        for section in SECTIONS:

            # Если секции нет или она пустая,
            # её заголовок не выводим.
            if section not in associations or not associations[section]:
                continue

            # Записываем название секции.
            file.write(f"[{section}]\n")

            # Записываем все MIME-типы внутри секции.
            for mime_type, applications in associations[section].items():

                # Объединяем список приложений через ";"
                # без дополнительного символа в конце.
                apps = ";".join(applications)

                file.write(f"{mime_type}={apps}\n")

            # Добавляем пустую строку между секциями.
            file.write("\n")
