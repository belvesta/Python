from os.path import exists
from csv import DictReader, DictWriter


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Не валидное имя")
            else:
                is_valid_first_name = True
        except NameError as err:
            print(err)
            continue

    last_name = "Иванов"

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


def create_file(file_name):
    try:
        with open(file_name, "x", encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
            f_writer.writeheader()
    except FileExistsError:
        pass  # Файл уже существует


def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def copy_row(src_file_name, dest_file_name, row_number):
    src_data = read_file(src_file_name)

    try:
        row_number = int(row_number)
        if 1 <= row_number <= len(src_data):
            row_to_copy = src_data[row_number - 1]
            dest_data = read_file(dest_file_name)
            dest_data.append(row_to_copy)
            with open(dest_file_name, "w", encoding='utf-8', newline='') as dest_data_file:
                dest_writer = DictWriter(dest_data_file, fieldnames=['Имя', 'Фамилия', 'Телефон'])
                dest_writer.writeheader()
                dest_writer.writerows(dest_data)
            print(f"Строка {row_number} успешно скопирована.")
        else:
            print("Введен неверный номер строки.")
    except ValueError:
        print("Номер строки должен быть целым числом.")


file_name = 'phone.csv'


def main():
    while True:
        command = input("Введите команду (w - записать, r - прочитать, c - скопировать, q - выход): ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*read_file(file_name))
        elif command == 'c':
            dest_file_name = input("Введите имя файла, в который нужно скопировать данные: ")
            row_number = input("Введите номер строки для копирования: ")
            copy_row(file_name, dest_file_name, row_number)


if __name__ == "__main__":
    main()