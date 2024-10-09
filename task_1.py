import shutil
from pathlib import Path
from random import randint, choice, choices
import numpy
from PIL import Image

MESSAGE = "Hello, Привіт"


def get_random_filename():
    random_value = (
        "()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz"
        "{}~абвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    )
    return "".join(choices(random_value, k=8))


def generate_text_files(path):
    documents = ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX")
    with open(path / f"{get_random_filename()}.{choice(documents).lower()}", "wb") as f:
        f.write(MESSAGE.encode())


def generate_archive_files(path):
    archive = ("ZIP", "GZTAR", "TAR")
    shutil.make_archive(
        f"{path}/{get_random_filename()}", f"{choice(archive).lower()}", path
    )


def generate_image(path):
    images = ("JPEG", "PNG", "JPG")
    image_array = numpy.random.rand(100, 100, 3) * 255
    image = Image.fromarray(image_array.astype("uint8"))
    image.save(f"{path}/{get_random_filename()}.{choice(images).lower()}")


def generate_folders(path):
    folder_name = [
        "temp",
        "folder",
        "dir",
        "tmp",
        "OMG",
        "is_it_true",
        "no_way",
        "find_it",
    ]
    folder_path = Path(
        f"{path}/"
        + "/".join(
            choices(
                folder_name,
                weights=[10, 10, 1, 1, 1, 1, 1, 1],
                k=randint(5, len(folder_name)),
            )
        )
    )
    folder_path.mkdir(parents=True, exist_ok=True)


def generate_folder_forest(path):
    for i in range(0, randint(2, 5)):
        generate_folders(path)


def generate_random_files(path):
    for i in range(3, randint(5, 7)):
        function_list = [generate_text_files, generate_archive_files, generate_image]
        choice(function_list)(path)


def parse_folder_recursion(path):
    for elements in path.iterdir():
        if elements.is_dir():
            generate_random_files(elements)
            parse_folder_recursion(elements)


def exist_parent_folder(path):
    path.mkdir(parents=True, exist_ok=True)


def file_generator(path):
    exist_parent_folder(path)
    generate_folder_forest(path)
    parse_folder_recursion(path)


# Додавання функції для копіювання файлів з сортуванням за розширенням
def copy_and_sort_files(src_dir, dest_dir):
    dest_dir.mkdir(parents=True, exist_ok=True)

    for item in src_dir.rglob("*"):  # Рекурсивно проходить по всіх файлах і директоріях
        if item.is_file():
            file_extension = item.suffix[1:]  # Отримуємо розширення файлу
            target_folder = (
                dest_dir / file_extension
            )  # Цільова папка для цього розширення
            target_folder.mkdir(
                parents=True, exist_ok=True
            )  # Створюємо папку, якщо її немає
            shutil.copy(item, target_folder / item.name)  # Копіюємо файл до нової папки
            print(f"Копіюю {item} до {target_folder}")


if __name__ == "__main__":
    # Генерація тестових файлів
    parent_folder_path = Path("Temp")
    file_generator(parent_folder_path)

    # Копіювання та сортування файлів
    destination_folder_path = Path("Sorted_Files")
    copy_and_sort_files(parent_folder_path, destination_folder_path)
