print("Привет! Это CleykaCore v.0.0.3.2!")
print("")
print("Список команд:")
print("info - выводит информацию о версии ядра")
print("poweroff - выключает ядро")
print("root - получить рут (логично)")
root = 0
while True:
    if root == 0:
        print("$ ", end="")
    else:
        print("# ", end="")
    user_input = input()
    if user_input == "info":
        print("CleykaCore v.0.0.3.2")
    elif user_input == "poweroff":
        break
    elif user_input == "root":
        print("Enter password!")
        print("Password: ", end="")
        user_input_0 = input()
        if user_input_0 == "6205":
            root = root + 1
        else:
            print("Wrong password!")
    else:
        print("Command", user_input, "not found")
      	