print("Привет! Это CleykaCore v.0.0.4 beta 1!")
print("")
print("Список команд:")
print("info - выводит информацию о версии ядра")
print("poweroff - выключает ядро")
print("root - получить рут (логично)")
print("unroot - убрать рут")
print("lang - сменить язык")
root = 0
lang =  "rus"
while True:
    if root == 0:
	    print("$ ", end="")
    else:
	    print("# ", end="")
    user_input = input()
    if user_input == "info":
    	print("CleykaCore v.0.0.4b1")
    elif user_input == "poweroff":
        break
    elif user_input == "root":
        if lang == "rus":
            print("Введите пароль")
        else:
            print("Enter password")
        if lang == "rus":
        	print( "Пароль: ", end="")
        else:
        	print( "Password: ", end="")
        user_input_0 = input()
        if user_input_0 == "6205":
	        root = 1
	        if lang ==  "rus":
	        	print( "Рутировано успешно!")
	        else:
	        	print( "Rooted successfully!")
        else:
	        if lang ==  "rus":
	    	    print( "Неверный пароль!")
	        else:
	    	    print( "Wrong password!")
    elif user_input == "unroot":
	    root = 0
	    if lang ==  "rus":
		    print( "Успешно убран рут!")
	    else:
		    print( "Root removed successfully!")
    elif user_input ==  "lang":
        if lang ==  "rus":
        	print( "Setted English language!")
        	lang =  "eng"
        else:
        	print( "Поставлен русский язык!")
        	lang =  "rus"
    else:
    	if lang ==  "rus":
    		print( "Команда", user_input, "не найдена")
    	else:
    		print( "Command", user_input, "not found")