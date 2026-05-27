print("Привет! Это CleykaCore v0.0.3.1!")
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
        print("CleykaCore v.0.0.3.1")
    elif user_input == "poweroff":
        break
    elif user_input == "root":
         root = root + 1
    else:
        print("Command", user_input, "not found")
      	