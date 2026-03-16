import os
import shutil
from pathlib import Path

class FileOperations:
    def __init__(self, root_dir):
        self.root = Path(root_dir).resolve()
        if not self.root.exists():
            self.root.mkdir(parents=True)
        self.current_dir = self.root

    def _resolve_path(self, path_str):
        if not path_str:
            target = self.current_dir
        else:
            target = (self.current_dir / path_str).resolve()
        try:
            target.relative_to(self.root)
        except ValueError:
            raise PermissionError("Ошибка безопасности: выход за пределы рабочей папки запрещен!")
        return target

    def list_dir(self, path=""):
        target_path = self._resolve_path(path)
        if not target_path.is_dir():
            print("Ошибка: Указанный путь не является директорией.")
            return
        for item in target_path.iterdir():
            suffix = "/" if item.is_dir() else ""
            print(f"  {item.name}{suffix}")

    def change_dir(self, path):
        new_path = self._resolve_path(path)
        if new_path.is_dir():
            self.current_dir = new_path

    def make_dir(self, path):
        new_dir = self._resolve_path(path)
        new_dir.mkdir(parents=True, exist_ok=True)

    def remove_dir(self, path):
        target_dir = self._resolve_path(path)
        if target_dir == self.root:
            print("Ошибка: Нельзя удалить корневую рабочую папку.")
            return
        try:
            target_dir.rmdir()
        except OSError as e:
            print(f"Ошибка удаления: {e}")

    def create_file(self, path, content=""):
        file_path = self._resolve_path(path)
        file_path.write_text(content, encoding='utf-8')

    def read_file(self, path):
        file_path = self._resolve_path(path)
        if not file_path.is_file():
            print("Ошибка: Файл не найден.")
            return
        try:
            content = file_path.read_text(encoding='utf-8')
            print(content)
        except UnicodeDecodeError:
            print("Ошибка: Не удалось прочитать файл.")

    def write_file(self, path, content):
        file_path = self._resolve_path(path)
        if not file_path.is_file():
            print("Ошибка: Файл не найден.")
            return
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)

    def delete_file(self, path):
        file_path = self._resolve_path(path)
        if file_path.is_file():
            file_path.unlink()
        else:
            print("Ошибка: Файл не найден.")

    def copy_file(self, src, dst):
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)
        if not src_path.is_file():
            print("Ошибка: Исходный файл не найден.")
            return
        shutil.copy2(src_path, dst_path)

    def move_file(self, src, dst):
        src_path = self._resolve_path(src)
        dst_path = self._resolve_path(dst)
        if not src_path.is_file():
            print("Ошибка: Исходный файл не найден.")
            return
        shutil.move(str(src_path), str(dst_path))

    def rename_file(self, old, new):
        old_path = self._resolve_path(old)
        new_path = self._resolve_path(new)
        if not old_path.exists():
            print("Ошибка: Исходный объект не найден.")
            return
        old_path.rename(new_path)

    def pwd(self):
        print(self.current_dir)