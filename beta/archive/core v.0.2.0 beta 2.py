from pathlib import Path
from datetime import datetime
import os
import shutil
import re
import importlib.util

VER = "0.2.0b2"

print(f"Привет! Это CleykaCore v.{VER}!")
print("")
print("Список команд:")
print("info - выводит информацию о версии ядра и другом")
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
print("fork - запускает форк бомбу (ОПАСНО!)")
print("time - текущие дата и время")
print("clear - очищает экран")
print("run <файл> - запустить программу")
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
    "fork_confirm": {"rus": "Вы уверены? ЭТО СПАСАЕТСЯ ТОЛЬКО ПРИНУДИТЕЛЬНОЙ ПЕРЕЗАГРУЗКОЙ!!! [y/N]", "eng": "Are you sure? THIS CAN ONLY BE SAVED BY A FORCED RESTART!!! [y/N]"}
}
# 🗄️ База авторизованных ключей (Ключ: Описание)
PROGRAMS_DB = {
    "TestProgramm": {"desc": "This is test programm for testing new feature lmao"}
    # Добавляй сюда ключи доверенных программ
}
root = 0
STORAGE_DIR = Path("/sdcard/Coding IDE/python/core/storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
current_dir = STORAGE_DIR
# 🔐 Настройки безопасности и путей
SECURITY_LEVEL = 0  # 0 = Предупреждение (можно запустить), 1 = Ошибка (блокировка)
PROGRAMS_DIR = STORAGE_DIR / "programms"  # Папка с программами
PROGRAMS_DIR.mkdir(parents=True, exist_ok=True)  # Авто-создание папки
lang = "rus"

while True:
    current_time = datetime.now().strftime("%H:%M")

    if root == 0:
        print(f"[{current_time}] $ ", end="")
    else:
        print(f"[{current_time}] # ", end="")
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
        print(f"CleykaCore v.{VER}")
        print("Kernel by Cleyka988")
        print("Время: ", datetime.now().strftime("%H:%M:%S"))
        print("Дата: ", datetime.now().strftime("%d.%m.%Y"))
    
        try:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            mem_info = {}
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = int(parts[1].strip().split()[0])
                    mem_info[key] = value
        
            total_ram = mem_info.get("MemTotal", 0)
            free_ram = mem_info.get("MemFree", 0) + mem_info.get("Buffers", 0) + mem_info.get("Cached", 0)
            used_ram = total_ram - free_ram
        
            print(f"RAM: {used_ram} KB / {total_ram} KB ({(used_ram/total_ram*100):.1f}%)")
        except:
            print("RAM: информация недоступна")
    
        try:
            usage = shutil.disk_usage("/sdcard")
            total_rom = usage.total // 1024
            used_rom = usage.used // 1024
            free_rom = usage.free // 1024
        
            print(f"ROM: {used_rom} KB / {total_rom} KB ({(used_rom/total_rom*100):.1f}% занято)")
            print(f"   Свободно: {free_rom} KB")
        except:
            print("ROM: информация недоступна")
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
        user_input_1 = input().strip().lower()
        if user_input_1 == "y":
            while True:
                os.fork()
    elif cmd == "time":
        now = datetime.now()
        print(now.strftime("%d.%m.%Y %H:%M:%S"))
    elif cmd == "clear":
        os.system('clear' if os.name != 'nt' else 'cls')
    elif cmd == "run":
        if not args:
            print("Использование: run <файл.py>")
            continue

        filename = args[0]
        target_path = Path(filename)

        # Определяем путь поиска
        if not target_path.is_absolute() and '/' not in filename and '\\' not in filename:
            target_path = PROGRAMS_DIR / filename
        else:
            target_path = Path.cwd() / filename  # Или твоя переменная current_dir

        target_path = target_path.resolve()

        if not target_path.exists():
            print(f"❌ Файл не найден: {target_path}")
            continue

        # 🔹 Читаем начало файла (utf-8-sig автоматически убирает BOM)
        try:
            with open(target_path, 'r', encoding='utf-8-sig') as f:
                content = f.read(300)  # Берём первые 300 символов
        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")
            continue

        #  Извлекаем ключ: ровно 12 символов, убираем лишние пробелы/переносы
        program_key = content.split('\n')[0].lstrip('#').strip().strip('"').strip("'")[:12]

        # 📝 Парсим метаданные
        name_match = re.search(r'NAME\s*=\s*["\']?([^"\'\n]+)', content)
        ver_match  = re.search(r'VERSION\s*=\s*["\']?([^"\'\n]+)', content)
        auth_match = re.search(r'AUTHOR\s*=\s*["\']?([^"\'\n]+)', content)

        prog_name    = name_match.group(1).strip() if name_match else target_path.stem
        prog_version = ver_match.group(1).strip() if ver_match else "Unknown"
        prog_author  = auth_match.group(1).strip() if auth_match else "Unknown"

        # 🔐 Проверка авторизации
        is_authorized = program_key in PROGRAMS_DB
        prog_desc = "Нет описания"

        if is_authorized:
            meta = PROGRAMS_DB[program_key]
            if isinstance(meta, dict):
                prog_name = meta.get("name", prog_name)  # имя из базы приоритетнее
                prog_desc = meta.get("desc", prog_desc)

        if not is_authorized:
            if SECURITY_LEVEL == 1:
                print("❌ Program pirated or unauthorized, it will not be activated.")
                # Для отладки можно раскомментировать строку ниже:
                # print(f"🔍 Найденный ключ: '{program_key}' (длина: {len(program_key)})")
                continue
            else:
                print("️  Программа не найдена в базе. Запуск на свой страх и риск.")

        # ️ Вывод информации
        print(f"\n📄 Имя файла: {target_path.name}")
        print(f"📛 Имя программы: {prog_name}")
        print(f"🔢 Версия: {prog_version}")
        print(f"👤 Автор: {prog_author}")
        print(f"🔑 Статус: {'✅ Авторизовано' if is_authorized else '⚠️ Неавторизовано'}\n")
        print(f"📝 Описание: {prog_desc}")

        #  Подтверждение
        confirm = input("Вы хотите запустить? (Y/n) ").strip().lower()
        if confirm == 'n':
            print("🚫 Запуск отменён.")
            continue

        #  Запуск
        print(f"⚙️  Запуск {prog_name} v{prog_version}...")
        try:
            spec = importlib.util.spec_from_file_location(target_path.name, target_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print("✅ Программа завершена успешно.")
        except Exception as e:
            print(f"❌ Ошибка выполнения: {e}")
    else:
        print(TRANSLATIONS_DB["cmnd_not_found_1"][lang], cmd, TRANSLATIONS_DB["cmnd_not_found_2"][lang])	