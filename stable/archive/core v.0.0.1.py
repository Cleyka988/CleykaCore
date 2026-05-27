print("Привет! Это CleykaCore v.0.0.1!")
print("")
print("Список команд:")
print("info - выводит информацию о версии ядра")
while True:
    print("$ ", end="")
    user_input = input()
    if user_input == "info":
        print("CleykaCore v.0.0.1")
    else:
        print("Command not found")
      	