#Password Strength 
#Copyright 2015 Jago Strong-Wright
def checkPass(password, pre_pass,name_f, name_s):
    # length = int()
    # lower = int()
    # upper = int()
    # special = int()
    # number = int()
    # like_past = int()
    # f_name = int()
    # s_name = int()
    password_strength = 0
    if len(password)>=8 :
        length = 1
    for i in lower_alphabet:
        if i in password:
            lower = 1
    for i in upper_alphabet:
        if i in password:
            upper = 1
    for i in special_characters:
        if i in password:
            special = 1
    for i in numbers:
        if i in password:
            number = 1
    if name_f.lower() not in password.lower():
        f_name = 1
    if name_s.lower() not in password.lower():
        s_name = 1
    if pre_pass.lower() not in password.lower():
        like_past = 1
    
    if length == 1:
        password_strength += 1
    if lower == 1 :
        password_strength += 1
    if upper== 1 :
        password_strength += 1
    if special == 1:
        password_strength +=2
    if f_name != 1:
        password_strength -=2
    if s_name != 1:
        password_strength -=2
    if like_past != 1:
        password_strength -=1
    
    password_rank = str()
    
    if password_strength >= 5:
        password_rank = 'Very Strong'
    elif password_strength == 4:
        password_rank = 'Strong'
    elif password_strength == 3:
        password_rank = 'OK'
    elif password_strength == 2:
        password_rank = 'Not Good'
    elif password_strength ==1:
        password_rank = 'Bad'
    elif password_strength < 1:
        password_rank = 'Awfle'
    print('\nI think that your password is ',password_rank)
    issues = [length, lower, upper, special, number, like_past, f_name, s_name, password_rank]
    return issues

lower_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
upper_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
special_characters = [' ', '!', '#', '$', '%', '&', '"', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',"'"]

choice = None

print("""
Welcome to JagoS-W password strength tester
""")

while choice != '0':
    print("""
Menu options:
    1 - Check Password Strength
    0 - Exit
""")

    choice = str(input('Please type the number that is beside your choice and press enter: '))
    i   f choice == '1':
        password = input('\nPlease enter your password here: ')
        pre_pass = input('\nPlease enter your previose password here: ')
        name_f = input('\nPlease enter your first name: ')
        name_s = input('\nPlease enter your last name: ')
        issues = checkPass(password,pre_pass,name_f,name_s)
        why = input('\nIf you would like to find out why type why? and press enter: ')
        if why.lower() == 'why?':
            if issues[0] != 1:
                print("It's too short")
            if issues[1] != 1:
                print("It doesn't have a lower case character in it")
            if issues[2] != 1:
                print("It doesn't have an upper case character in it")
            if issues[3] != 1:
                print("It doesn't have a special character in it")
            if issues[4] != 1:
                print("It doesn't have a number in it")
            if issues[5] != 1:
                print("It's like your old password")
            if issues[6] != 1:
                print("It's got your first name in it")
            if issues[7] != 1:
                print("It's got your last name in it")
            if issues[8] == 'Very Strong':
                print('There is nothing wrong with it!')
    elif choice == '0':
        print('Goodbye')
    else:
        print('Choice is invalid, please try again')
        
