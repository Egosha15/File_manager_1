import configparser
import os
import sys
from file_operations import FileOperations


def load_config(config_file='config.ini'):
    """Загружает конфигурацию из файла."""
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        print(f"Ошибка: Файл конфигурации '{config_file}' не найден.")
        print("Создайте файл config.ini с секцией [Settings] и параметром work_directory.")
        sys.exit(1)

    config.read(config_file)
    try:
        work_dir = config['Settings']['work_directory']
        return work_dir
    except KeyError:
        print("Ошибка: В файле config.ini отсутствует секция [Settings] или параметр work_directory.")
        sys.exit(1)


def print_help():
    """Выводит список доступных команд."""
    help_text = """
    ДОСТУПНЫЕ КОМАНДЫ:
    ===================
    ls [path]          - Просмотр содержимого директории
    cd <path>          - Перейти в директорию
    pwd                - Показать текущую директорию
    mkdir <path>       - Создать директорию
    rmdir <path>       - Удалить ПУСТУЮ директорию
    touch <file>       - Создать пустой файл
    cat <file>         - Прочитать файл
    echo <file> <text> - Добавить текст в конец файла (в кавычках)
    rm <file>          - Удалить файл
    cp <src> <dst>     - Скопировать файл
    mv <src> <dst>     - Переместить файл
    rename <old> <new> - Переименовать файл/папку
    help               - Показать эту справку
    exit / quit        - Выход из программы
    """
    print(help_text)


def main():
    """Главная функция программы."""
    work_dir_path = load_config()
    if not os.path.isabs(work_dir_path):
        work_dir_path = os.path.join(os.path.dirname(__file__), work_dir_path)

    try:
        fm = FileOperations(work_dir_path)
    except Exception as e:
        print(f"Ошибка инициализации рабочей директории: {e}")
        sys.exit(1)

    print("=" * 50)
    print("Добро пожаловать в файловый менеджер!")
    print("=" * 50)
    print_help()

    while True:
        try:
            # Простой ввод команд
            command_line = input(f"\n{fm.current_dir.name if fm.current_dir.name else 'root'} $ ").strip()
            if not command_line:
                continue

            parts = command_line.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in ('exit', 'quit'):
                print("Выход из программы.")
                break
            elif cmd == 'help':
                print_help()
            elif cmd == 'ls':
                fm.list_dir(args[0] if args else "")
            elif cmd == 'cd':
                if args:
                    fm.change_dir(args[0])
                else:
                    fm.change_dir(".")
            elif cmd == 'pwd':
                fm.pwd()
            elif cmd == 'mkdir':
                if args:
                    fm.make_dir(args[0])
                else:
                    print("Использование: mkdir <dirname>")
            elif cmd == 'rmdir':
                if args:
                    fm.remove_dir(args[0])
                else:
                    print("Использование: rmdir <dirname>")
            elif cmd == 'touch':
                if args:
                    fm.create_file(args[0], "")
                else:
                    print("Использование: touch <filename>")
            elif cmd == 'cat':
                if args:
                    fm.read_file(args[0])
                else:
                    print("Использование: cat <filename>")
            elif cmd == 'echo':
                # Простейший парсер для поддержки текста с пробелами
                if len(args) >= 2:
                    file_name = args[0]
                    # Склеиваем остальные аргументы как текст
                    text = ' '.join(args[1:]).strip('\'"')
                    fm.write_file(file_name, text + '\n')
                else:
                    print("Использование: echo <filename> <text>")
            elif cmd == 'rm':
                if args:
                    fm.delete_file(args[0])
                else:
                    print("Использование: rm <filename>")
            elif cmd == 'cp':
                if len(args) >= 2:
                    fm.copy_file(args[0], args[1])
                else:
                    print("Использование: cp <source> <destination>")
            elif cmd == 'mv':
                if len(args) >= 2:
                    fm.move_file(args[0], args[1])
                else:
                    print("Использование: mv <source> <destination>")
            elif cmd == 'rename':
                if len(args) >= 2:
                    fm.rename_file(args[0], args[1])
                else:
                    print("Использование: rename <old_name> <new_name>")
            else:
                print(f"Неизвестная команда: {cmd}. Введите 'help' для списка команд.")

        except PermissionError as e:
            print(e)
        except Exception as e:
            print(f"Произошла ошибка: {e}. Попробуйте снова.")


if __name__ == "__main__":
    main()
