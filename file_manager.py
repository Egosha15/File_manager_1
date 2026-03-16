import configparser
import os
import sys
from file_operations import FileOperations

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        print("Ошибка: Файл конфигурации не найден.")
        sys.exit(1)
    config.read(config_file)
    try:
        return config['Settings']['work_directory']
    except KeyError:
        print("Ошибка: Неверный формат config.ini")
        sys.exit(1)

def print_help():
    help_text = """
Доступные команды:
ls [path]          - просмотр содержимого
cd <path>          - сменить директорию
pwd                - текущий путь
mkdir <path>       - создать директорию
rmdir <path>       - удалить директорию
touch <file>       - создать файл
cat <file>         - прочитать файл
echo <file> <text> - добавить текст в файл
rm <file>          - удалить файл
cp <src> <dst>     - скопировать файл
mv <src> <dst>     - переместить файл
rename <old> <new> - переименовать
help               - справка
exit/quit          - выход
    """
    print(help_text)

def main():
    work_dir_path = load_config()
    if not os.path.isabs(work_dir_path):
        work_dir_path = os.path.join(os.path.dirname(__file__), work_dir_path)
    try:
        fm = FileOperations(work_dir_path)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    print_help()
    while True:
        try:
            command_line = input(f"\n{fm.current_dir.name} $ ").strip()
            if not command_line:
                continue
            parts = command_line.split()
            cmd = parts[0].lower()
            args = parts[1:]
            if cmd in ('exit', 'quit'):
                break
            elif cmd == 'help':
                print_help()
            elif cmd == 'ls':
                fm.list_dir(args[0] if args else "")
            elif cmd == 'cd':
                fm.change_dir(args[0] if args else ".")
            elif cmd == 'pwd':
                fm.pwd()
            elif cmd == 'mkdir' and args:
                fm.make_dir(args[0])
            elif cmd == 'rmdir' and args:
                fm.remove_dir(args[0])
            elif cmd == 'touch' and args:
                fm.create_file(args[0], "")
            elif cmd == 'cat' and args:
                fm.read_file(args[0])
            elif cmd == 'echo' and len(args) >= 2:
                fm.write_file(args[0], ' '.join(args[1:]).strip('\'"') + '\n')
            elif cmd == 'rm' and args:
                fm.delete_file(args[0])
            elif cmd == 'cp' and len(args) >= 2:
                fm.copy_file(args[0], args[1])
            elif cmd == 'mv' and len(args) >= 2:
                fm.move_file(args[0], args[1])
            elif cmd == 'rename' and len(args) >= 2:
                fm.rename_file(args[0], args[1])
            else:
                print("Неизвестная команда. Введите help.")
        except PermissionError as e:
            print(e)
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()