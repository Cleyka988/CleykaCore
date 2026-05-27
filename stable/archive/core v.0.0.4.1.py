print("Привет! Это CleykaCore v.0.0.4.1!")
print("")
print("Список команд:")
print("info - выводит информацию о версии ядра")
print("poweroff - выключает ядро")
print("root - получить рут (логично)")
print("unroot - убрать рут")
print("lang - сменить язык")

TRANSLATIONS_DB = {
    "root_enter_pass": {"rus": "Введите пароль", "eng": "Enter password"},
    "root_pass": {"rus": "Пароль: ", "eng": "Password: "},
    "root_success": {"rus": "Рутировано успешно!", "eng": "Rooted successfully!"},
    "wrong_pass": {"rus": "Неверный пароль!", "eng": "Wrong password!"},
    "unroot_success": {"rus": "Рут убран успешно", "eng": "Root removed successfully!"},
    "language": {"rus": "Setted English language!", "eng": "Поставлен русский язык!"},
    "cmnd_not_found_1": {"rus": "Команда", "eng": "Command"},
    "cmnd_not_found_2": {"rus": "не найдена", "eng": "not found"}
}
root = 0
lang = "rus"
while True:
    if root == 0:
        print("$ ", end="")
    else:
        print("# ", end="")
    user_input = input().strip()
    if user_input == "info":
        print("CleykaCore v.0.0.4.1")
    elif user_input == "poweroff":
        break
    elif user_input == "root":
        print(TRANSLATIONS_DB["root_enter_pass"][lang])
        print(TRANSLATIONS_DB["root_pass"][lang], end="")
        user_input_0 = input().strip()
        if user_input_0 == "6205":
            root = 1
            print(TRANSLATIONS_DB["root_success"][lang])
        else:
            print(TRANSLATIONS_DB["wrong_pass"][lang])
    elif user_input == "unroot":
        root = 0
        print(TRANSLATIONS_DB["unroot_success"][lang])
    elif user_input == "lang":
        print(TRANSLATIONS_DB["language"][lang])
        if lang == "rus":
            lang = "eng"
        else:
            lang = "rus"
    else:
        print(TRANSLATIONS_DB["cmnd_not_found_1"][lang], user_input, TRANSLATIONS_DB["cmnd_not_found_2"][lang])	