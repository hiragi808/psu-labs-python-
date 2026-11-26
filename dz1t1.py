import string
import random
import math
from string import ascii_letters, ascii_lowercase, ascii_uppercase
def ocenka(password,used):
    alphabet_size = (
            used[0] * len(string.digits)
            + used[1] * 8
            + used[2] * len(ascii_lowercase)
            + used[3] * len(ascii_uppercase)
    )
    print(f"Сгенерированный пароль: {password}")
    print("="*10)
    print("Длинна:",len(password))
    print(f"Категории: {sum(used)} из {len(used)}")
    q = math.log2( (alphabet_size ) ** len(password))
    q=round(q,2)
    print("Энтропия:", q)
    if 0 <= q < 30:
        print("Надежность: Очень слабый")
    elif 30 <= q < 50:
        print("Надежность: Слабый")
    elif 50 <= q < 70:
        print("Надежность: Средний")
    elif 70 <= q < 90:
        print("Надежность: Хороший")
    else:  # q >= 90
        print("Надежность: Отличный")
    print("="*10)
def gen():
    special = "!@#$%^&*"
    used = [0] * 4
    pool = ""
    password = ""
    while True:
        try:
            n = int(input("Введите длину паролья от 6 до 20 "))
            if (n in range(6, 21)):
                break
            else:
                print("Неправильный ввод, длинна от 6 до 20")
        except Exception:
            print("Неправильный ввод, введите целое число длинны")
    choice = input("Добавить цифры?(Y/N)")[0]
    if choice == "Y":
        password = password + random.choice(string.digits)
        n=n-1
        pool=pool+string.digits
        used[0] = 1
    choice = input("Добавить специальные символы(Y/N)")[0]
    if choice == "Y":
        password = password + random.choice(special)
        n = n - 1
        used[1] = 1
        pool = pool + special
    choice = input("Добавить сторочные буквы(Y/N)")
    if choice == "Y":
        password = password + random.choice(ascii_lowercase)
        n = n - 1
        used[2] = 1
        pool = pool + ascii_lowercase
    choice = input("Добавить заглавные буквы(Y/N)")
    if choice == "Y":
        password = password + random.choice(ascii_uppercase)
        n = n - 1
        used[3] = 1
        pool = pool + ascii_uppercase
    listp = list(password)
    if pool != "":
        for i in range(n):
            listp.append(random.choice(pool))
        random.shuffle(listp)
        password = "".join(listp)
        ocenka(password,used)
    else:
        print("Вы не добавили ни одну из групп символов")
while True:
    gen()
    s = input("Сгенирировать еще?(Y/N)")[0]
    if s == "N":
        break