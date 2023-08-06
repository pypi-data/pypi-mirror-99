"""
HomeTask 1 func
"""
def svetofor():
    print("Какой горит цвет?")
    signal = input()
    print("Горит", signal)
    while signal != "выход":
        if signal == "Зелёный":
            print("Идите")
            print("Какой горит цвет?")
            signal= input()
        elif signal == "Красный":
            print("Стойте и ждите зелёный")
            print("Какой горит цвет?")
            signal= input()
        else:
            print("Не распознан сигнал,введите заного")
            signal= input()

"""
HomeTask 2 func
"""

def counter_num():
    print("Какой длины будет диапазон?")
    n = int(input())
    print("Какую цифру нужно считать?")
    d = int(input())
    print("Далее вводите цифры по очереди")
    count= 0
    for i in range(1, n + 1):
        m = int(input("Число"+ str(i)+ ": "))
        while m > 0:
            if m % 10 == d:
                count +=1
            m = m // 10
    print("Цифра-",d,"Встретилась ", count, "раз")


def fizzbuzz():
    for count in range(1,101):
        if count % 3 == 0 and count % 5 == 0:
            print("FizzBuzz")
        elif count % 3 == 0:
            print("Fizz")
        elif count % 5 == 0:
            print("Buzz")
        else:
            print(count)


def noknodsimple():
    from math import sqrt

    print("Можно найти НОД, НОК, или узнать простое ли это число")
    print("Далее запустится цикл из которого можно выйти только введя слово - выход или написать что-то кроме условия")
    print("Что ты хочешь узнать? Введи NOK, NOD  или SIMPLE")
    move= input()
    while move != "выход":
        if move == "NOD":
            print("Введите два числа :")
            a = int(input())
            b = int(input())
            while a != 0 and b != 0:
                if a > b:
                    a %= b
                else:
                    b %= a
            print("Нод =", a+b)
            print("Что ты хочешь узнать? Введи NOK, NOD  или SIMPLE")
            move= input()
        elif move == "NOK":
            print("Введите два числа :")
            a = int(input())
            b = int(input())
            cloud= a * b
            while a != 0 and b != 0:
                if a > b:
                    a %= b
                else:
                    b %= a
            print("Нок =", cloud //(a+b))
            print("Что ты хочешь узнать? Введи NOK, NOD  или SIMPLE")
            move= input()
        elif move =="SIMPLE":
            print("Введите число для проверки")
            n = int(input())
            if n < 2:
                print("False, Число должно быть больше 1")
                print("Что ты хочешь узнать? Введи NOK, NOD  или SIMPLE")
                move= input()
            elif n == 2 or n == 3:
                print("Это простое число")
                print("Что ты хочешь узнать? Введи NOK, NOD  или SIMPLE")
                move= input()
            d = 2
            while d <= sqrt(n):
                if n % d == 0:
                    print("Это сложное число")
                else:
                    print("Это простое число")
                d +=1
                print("Что ты хочешь узнать? Введи NOK, NOD  или SIMPLE")
                move= input()
        else:
            print("Не понятен ввод")
            quit()