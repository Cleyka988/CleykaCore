from pathlib import Path
import os

print("Привет! Это CleykaCore v.0.1.1!")
print("")
print("Список команд:")
print("info - выводит информацию о версии ядра")
print("poweroff - выключает ядро")
print("root - получить рут (логично)")
print("unroot - убрать рут")
print("lang - сменить язык")
print("go <папка> / go .. - переход в папку (.. - предыдущая папка)")
print("readdir - показывает файлы и папки в текущей директории")
print("path - показывает полный путь к текущей папке")
print("readfile <файл> - выводит содержимое файла")
print("newfile <название файла> - создает пустой файл")
print("write <файл> <содержимое> - перезаписать файл")
print("del <папка или файл> - удаляет папку")
print("newdir <название папки> - создает новую папку")
print("fork - запускает форк бомбу")
print("")

TRANSLATIONS_DB = {
    "root_enter_pass": {"rus": "Введите пароль", "eng": "Enter password"},
    "root_pass": {"rus": "Пароль: ", "eng": "Password: "},
    "root_success": {"rus": "Рутировано успешно!", "eng": "Rooted successfully!"},
    "wrong_pass": {"rus": "Неверный пароль!", "eng": "Wrong password!"},
    "unroot_success": {"rus": "Рут убран успешно", "eng": "Root removed successfully!"},
    "language": {"rus": "Setted English language!", "eng": "Поставлен русский язык!"},
    "cmnd_not_found_1": {"rus": "Команда", "eng": "Command"},
    "cmnd_not_found_2": {"rus": "не найдена", "eng": "not found"},
    "file_ls": {"rus": "Содержимое папки:", "eng": "Directory contents:"},
    "file_not_found": {"rus": "Файл или папка не найдены", "eng": "File or directory not found"},
    "file_created": {"rus": "Файл создан", "eng": "File created"},
    "file_deleted": {"rus": "Файл удалён", "eng": "File deleted"},
    "dir_changed": {"rus": " Переход в:", "eng": "Changed to:"},
    "pwd_msg": {"rus": "Текущий путь:", "eng": " Current path:"},
    "dir_created": {"rus": "Папка создана", "eng": "Directory created"},
    "usage_cat": {"rus": "Использование: readfile <имя_файла>", "eng": "Usage: readfile <filename>"},
    "usage_touch": {"rus": "Использование: newfile <имя_файла>", "eng": "Usage: newfile <filename>"},
    "usage_write": {"rus": "Использование: write <файл> <текст>", "eng": "Usage: write <file> <text>"},
    "file_error": {"rus": "Ошибка доступа к файлу", "eng": "File access error"},
    "fork_confirm": {"rus": "Вы уверены? [y/N]", "eng": "Are you sure? [y/N]"}
}
root = 0
STORAGE_DIR = Path("/sdcard/Coding IDE/python/core/storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
current_dir = STORAGE_DIR
lang = "rus"
while True:
    if root == 0:
        print("$ ", end="")
    else:
        print("# ", end="")
    cmd = input().strip()
    parts = cmd.split()
    if not parts:
        continue
    cmd = parts[0].lower()
    args = parts[1:]

    if cmd == "readdir":
        print(TRANSLATIONS_DB["file_ls"][lang])
        try:
            for item in sorted(current_dir.iterdir()):
                prefix = " " if item.is_dir() else " "
                print(f"  {prefix}{item.name}")
        except PermissionError:
            print(TRANSLATIONS_DB["file_error"][lang])

    elif cmd == "go":
        if not args:
            current_dir = STORAGE_DIR
            print(f"{TRANSLATIONS_DB['dir_changed'][lang]} {current_dir}")
        else:
            target = current_dir / args[0]
            if target.is_dir():
                current_dir = target.resolve()
                print(f"{TRANSLATIONS_DB['dir_changed'][lang]} {current_dir}")
            else:
                print(TRANSLATIONS_DB["file_not_found"][lang])

    elif cmd == "path":
        print(f"{TRANSLATIONS_DB['pwd_msg'][lang]} {current_dir}")

    elif cmd == "readfile":
        if not args:
            print(TRANSLATIONS_DB["usage_cat"][lang])
            continue
        target = current_dir / args[0]
        if target.is_file():
            try:
                print(target.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"{TRANSLATIONS_DB['file_error'][lang]}: {e}")
        else:
            print(TRANSLATIONS_DB["file_not_found"][lang])

    elif cmd == "newfile":
        if not args:
            print(TRANSLATIONS_DB["usage_touch"][lang])
            continue
        try:
            (current_dir / args[0]).touch()
            print(TRANSLATIONS_DB["file_created"][lang])
        except Exception as e:
            print(f"{TRANSLATIONS_DB['file_error'][lang]}: {e}")

    elif cmd == "write":
        if len(args) < 2:
            print(TRANSLATIONS_DB["usage_write"][lang])
            continue
        fname, *text_parts = args
        text = " ".join(text_parts)
        try:
            (current_dir / fname).write_text(text, encoding="utf-8")
            print("OK")
        except Exception as e:
            print(f"{TRANSLATIONS_DB['file_error'][lang]}: {e}")

    elif cmd == "del":
        if not args:
            print("Usage: del <file>")
            continue
        target = current_dir / args[0]
        if target.exists():
            try:
                if target.is_file():
                    target.unlink()
                else:
                    import shutil
                    shutil.rmtree(target)
                print(TRANSLATIONS_DB["file_deleted"][lang])
            except Exception as e:
                print(f"{TRANSLATIONS_DB['file_error'][lang]}: {e}")
        else:
            print(TRANSLATIONS_DB["file_not_found"][lang])

    elif cmd == "newdir":
        if not args:
            print("Usage: newdir <dirname>")
            continue
        try:
            (current_dir / args[0]).mkdir(exist_ok=True)
            print(TRANSLATIONS_DB["dir_created"][lang])
        except Exception as e:
            print(f"{TRANSLATIONS_DB['file_error'][lang]}: {e}")
    elif cmd == "info":
        print("CleykaCore v.0.1.1")
    elif cmd == "poweroff":
        break
    elif cmd == "root":
        print(TRANSLATIONS_DB["root_enter_pass"][lang])
        print(TRANSLATIONS_DB["root_pass"][lang], end="")
        user_input_0 = input().strip()
        if user_input_0 == "6205":
            root = 1
            print(TRANSLATIONS_DB["root_success"][lang])
        else:
            print(TRANSLATIONS_DB["wrong_pass"][lang])
    elif cmd == "unroot":
        root = 0
        print(TRANSLATIONS_DB["unroot_success"][lang])
    elif cmd == "lang":
        print(TRANSLATIONS_DB["language"][lang])
        if lang == "rus":
            lang = "eng"
        else:
            lang = "rus"
    elif cmd == "fork":
        print(TRANSLATIONS_DB["fork_confirm"][lang], end=" ")
        user_input_1 = input().strip()
        if user_input_1 == "y" or "Y":
            while True:
                os.fork()
    else:
        print(TRANSLATIONS_DB["cmnd_not_found_1"][lang], cmd, TRANSLATIONS_DB["cmnd_not_found_2"][lang])	