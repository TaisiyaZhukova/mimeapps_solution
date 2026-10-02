from mime_associations import (
    read_associations,
    merge_associations,
    write_associations
)


# Создаем пример словаря ассоциаций.
example = {

    # Приложение по умолчанию для открытия текстовых файлов.
    "Default Applications": {
        "text/plain": [
            "gedit.desktop"
        ]
    },

    # Дополнительные приложения для изображений.
    "Added Associations": {
        "image/png": [
            "firefox.desktop",
            "gimp.desktop"
        ]
    },

    # Удаленные ассоциации.
    "Removed Associations": {}
}


# Записываем словарь в файл.
write_associations(
    example,
    "example_mimeapps.list"
)


# Проверяем чтение файла.
result = read_associations(
    "example_mimeapps.list"
)

print("Прочитанные ассоциации:")
print(result)


# Создаем новые ассоциации,
# которые должны заменить старые.
new = {

    "Default Applications": {
        "text/plain": [
            "code.desktop"
        ]
    }
}


# Проверяем объединение словарей.
merged = merge_associations(
    example,
    new
)

print("\nПосле объединения:")
print(merged)
