import pytest

from mime_associations import (
    read_associations,
    merge_associations,
    write_associations
)

"""
Тест-план

read_associations:
  1. Чтение корректного файла с несколькими секциями.
  2. Чтение пустого файла.
  3. Чтение файла только с одной секцией.
  4. Обработка отсутствующего файла.

merge_associations:
  1. Объединение двух словарей без пересечений.
  2. Перезапись существующего MIME-типа значением из второго словаря.
  3. Объединение нескольких секций.
  4. Работа с пустыми словарями.

write_associations:
  1. Запись структуры данных в файл.
  2. Возможность повторного чтения после записи.
  3. Запись пустой структуры.
  4. Корректное создание файла.
"""


# ==========================
# Тесты read_associations
# ==========================


def test_read_correct_file(tmp_path):
    """Проверяет чтение корректного файла с несколькими секциями."""

    file = tmp_path / "mimeapps.list"

    file.write_text(
        """
[Default Applications]
text/plain=gedit.desktop
image/png=eog.desktop

[Added Associations]
text/plain=vim.desktop;
""",
        encoding="utf-8"
    )

    result = read_associations(file)

    assert result == {
        "Default Applications": {
            "text/plain": "gedit.desktop",
            "image/png": "eog.desktop"
        },
        "Added Associations": {
            "text/plain": "vim.desktop;"
        }
    }


def test_read_empty_file(tmp_path):
    """Проверяет обработку пустого файла."""

    file = tmp_path / "empty.list"
    file.write_text("", encoding="utf-8")

    result = read_associations(file)

    assert result == {}


def test_read_single_section(tmp_path):
    """Проверяет чтение файла с одной секцией."""

    file = tmp_path / "mimeapps.list"

    file.write_text(
        """
[Default Applications]
application/pdf=firefox.desktop
""",
        encoding="utf-8"
    )

    result = read_associations(file)

    assert result["Default Applications"] == {
        "application/pdf": "firefox.desktop"
    }


def test_read_missing_file(tmp_path):
    """Проверяет ошибку при отсутствии файла."""

    file = tmp_path / "missing.list"

    with pytest.raises(FileNotFoundError):
        read_associations(file)


# ==========================
# Тесты merge_associations
# ==========================


def test_merge_without_conflicts():
    """Проверяет объединение данных без одинаковых MIME-типов."""

    first = {
        "Default Applications": {
            "text/plain": "gedit.desktop"
        }
    }

    second = {
        "Default Applications": {
            "image/png": "eog.desktop"
        }
    }

    result = merge_associations(first, second)

    assert result["Default Applications"] == {
        "text/plain": "gedit.desktop",
        "image/png": "eog.desktop"
    }


def test_merge_overwrites_values():
    """Проверяет замену старого значения новым."""

    first = {
        "Default Applications": {
            "image/png": "old.desktop"
        }
    }

    second = {
        "Default Applications": {
            "image/png": "new.desktop"
        }
    }

    result = merge_associations(first, second)

    assert result["Default Applications"]["image/png"] == "new.desktop"


def test_merge_multiple_sections():
    """Проверяет объединение нескольких секций."""

    first = {
        "Default Applications": {
            "text/plain": "gedit.desktop"
        }
    }

    second = {
        "Added Associations": {
            "image/jpeg": "gimp.desktop;"
        }
    }

    result = merge_associations(first, second)

    assert "Default Applications" in result
    assert "Added Associations" in result


@pytest.mark.parametrize(
    "first, second",
    [
        ({}, {}),
        ({"Default Applications": {}}, {}),
        ({}, {"Added Associations": {}})
    ]
)
def test_merge_empty_cases(first, second):
    """Проверяет объединение пустых структур."""

    result = merge_associations(first, second)

    assert isinstance(result, dict)


# ==========================
# Тесты write_associations
# ==========================


def test_write_creates_file(tmp_path):
    """Проверяет создание файла после записи."""

    file = tmp_path / "output.list"

    data = {
        "Default Applications": {
            "text/plain": "gedit.desktop"
        }
    }

    write_associations(file, data)

    assert file.exists()


def test_write_then_read(tmp_path):
    """Проверяет сохранение и повторное чтение данных."""

    file = tmp_path / "mimeapps.list"

    data = {
        "Default Applications": {
            "image/png": "eog.desktop"
        }
    }

    write_associations(file, data)

    result = read_associations(file)

    assert result == data


def test_write_empty_data(tmp_path):
    """Проверяет запись пустой структуры."""

    file = tmp_path / "empty.list"

    write_associations(file, {})

    assert file.exists()
    assert file.read_text(encoding="utf-8") == ""


def test_write_multiple_sections(tmp_path):
    """Проверяет запись нескольких секций."""

    file = tmp_path / "mimeapps.list"

    data = {
        "Default Applications": {
            "text/plain": "gedit.desktop"
        },
        "Added Associations": {
            "image/png": "gimp.desktop;"
        }
    }

    write_associations(file, data)

    text = file.read_text(encoding="utf-8")

    assert "[Default Applications]" in text
    assert "[Added Associations]" in text
