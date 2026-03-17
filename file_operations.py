import os
import shutil
from pathlib import Path


class FileOperations:
    """Класс для безопасных операций с файловой системой."""

    def __init__(self, root_dir):
        """
        Инициализация менеджера.

        Args:
            root_dir (str): Путь к корневой (рабочей) директории.
        """
        self.root = Path(root_dir).resolve()
        if not self.root.exists():
            self.root.mkdir(parents=True)
            print(f"Создана рабочая директория: {self.root}")
        self.current_dir = self.root
        print(f"Корневая директория: {self.root}")

    def _resolve_path(self, path_str):
        """
        Преобразует относительный путь в абсолютный и проверяет,
        находится ли он внутри корневой директории.

        Args:
            path_str (str): Путь от текущей директории.

        Returns:
            Path: Абсолютный путь, если он безопасен.

        Raises:
            PermissionError: Если попытка выйти за пределы корневой папки.
        """
        if not path_str:
            target = self.current_dir
        else:
            target = (self.current_dir / path_str).resolve()

        try:
            target.relative_to(self.root)
        except ValueError:
            raise PermissionError(f"Ошибка безопасности: выход за пределы рабочей папки запрещен! ({target})")

        return target

    def list_dir(self, path=""):
        """Просмотр содержимого директории."""
        target_path = self._resolve_path(path)
        if not target_path.is_dir():
            print("Ошибка: Указанный путь не является директорией.")
            return
        print(f"\nСодержимое: {target_path}")
        for item in target_path.iterdir():
            suffix = "/" if item.is_dir() else ""
            print(f"  {item.name}{suffix}")

    def change_dir(self, path):
        """Смена текущей директории."""
        new_path = self._resolve_path(path)
        if new_path.is_dir():
            self.current_dir = new_path
            print(f"Текущая директория: {self.current_dir}")
        else:
            print("Ошибка: Директория не существует.")

    def make_dir(self, path):
        """Создание новой директории."""
        new_dir = self._resolve_path(path)
        new_dir.mkdir(parents=True, exist_ok=True)
        print(f"Директория создана: {new_dir}")

    def remove_dir(self, path):
        """Удаление пустой директории."""
        target_dir = self._resolve_path(path)
        if target_dir == self.root:
            print("Ошибка: Нельзя удалить корневую рабочую папку.")
            return
        try:
            target_dir.rmdir()  # rmdir удаляет только пустые папки
            print(f"Директория удалена: {target_dir}")
        except OSError as e:
            print(f"Ошибка удаления (возможно, папка не пуста): {e}")

    def create_file(self, path, content=""):
        """Создание нового файла (или перезапись существующего)."""
        file_path = self._resolve_path(path)
        file_path.write_text(content, encoding='utf-8')
        print(f"Файл создан: {file_path}")

    def read_file(self, path):
        """Чтение и вывод содержимого файла."""
        file_path = self._resolve_path(path)
        if not file_path.is_file():
            print("Ошибка: Файл не найден.")
            return
        try:
            content = file_path.read_text(encoding='utf-8')
            print(f"\n--- Содержимое {file_path.name} ---")
            print(content)
            print("--- Конец файла ---\n")
        except UnicodeDecodeError:
            print("Ошибка: Не удалось прочитать файл (возможно, бинарный).")

    def write_file(self, path, content):
        """Дозапись в конец файла."""
        file_path = self._resolve_path(path)
        if not file_path.is_file():
            print("Ошибка: Файл не найден.")
            return
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        print(f"Текст добавлен в файл: {file_path}")

    def delete_file(self, path):
        """Удаление файла."""
        file_path = self._resolve_path(path)
        if file_path.is_file():
            file_path.unlink()
            print(f"Файл удален: {file_path}")
        else:
            print("Ошибка: Файл не найден.")

    def copy_file(self, src, dst):
        """Копирование файла."""
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)
        if not src_path.is_file():
            print("Ошибка: Исходный файл не найден.")
            return
        shutil.copy2(src_path, dst_path)  # copy2 сохраняет метаданные
        print(f"Скопировано: {src_path} -> {dst_path}")

    def move_file(self, src, dst):
        """Перемещение файла."""
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)
        if not src_path.is_file():
            print("Ошибка: Исходный файл не найден.")
            return
        shutil.move(str(src_path), str(dst_path))
        print(f"Перемещено: {src_path} -> {dst_path}")

    def rename_file(self, old, new):
        """Переименование файла или папки."""
        old_path = self._resolve_path(old)
        new_path = self._resolve_path(new)
        if not old_path.exists():
            print("Ошибка: Исходный объект не найден.")
            return
        old_path.rename(new_path)
        print(f"Переименовано: {old_path} -> {new_path}")

    def pwd(self):
        """Показать текущий путь."""
        print(self.current_dir)
