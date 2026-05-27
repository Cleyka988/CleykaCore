print("Привет! Это CleykaCore v.0.0.2!")
print("")
print("Список команд:")
print("info - выводит информацию о версии ядра")
print("poweroff - выключает ядро")
while True:
    print("$ ", end="")
    user_input = input()
    if user_input == "info":
        print("CleykaCore v.0.0.2")
    elif user_input == "poweroff":
  	break
    else
        print("Command not found")
      	