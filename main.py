import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER AUTO_INCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()
def checksum(number):
    sum_ = 0
    number = "400000" + number
    for i in range(0, 15, 2):
        meta = int(number[i])      
        meta *= 2    
        if meta > 9:
            meta -= 9   
        sum_ += meta
    for i in range(1, 15, 2):
        meta = int(number[i])
        sum_ += meta
    return str(10 - (sum_ % 10))


def allkeyes():
    cur.execute('SELECT number FROM card')
    return cur.fetchall()

def addincome(number, balance):
    cur.execute('UPDATE card SET balance = balance + ? WHERE number = ? ', [balance, number])
    conn.commit()

def getpin(number):
    cur.execute('SELECT pin FROM card WHERE number = ?', [number])
    return cur.fetchall()


def getbalance(number):
    cur.execute('SELECT balance FROM card WHERE number = ?', [number])
    return useless(cur.fetchall())

def transfermoney(number1, number2, income):
    if getbalance(number2) < income:
        print("Not enough money!")
        return
    addincome(number1, income)
    income = -int(income)
    addincome(number2, income)
    print(getbalance(number2))
    return("Sucess")

def checktransfervalidity(number1, number2):
    if number1 == number2:
        return "You can't transfer money to the same account!"
    partnumber = number1[6:]
    partnumber = partnumber[:9]
    print (partnumber)
    if checksum(partnumber) != number1[15]:
        return "Probably you made a mistake in the card number. Please try again!"
    state = 0
    for iter in allkeyes():
            iter = ''.join(iter)
            if iter == number1:
                state = 1
    if state == 0:
        return "Such a card does not exist."
    return "How much money"

def closeacc(number):
    cur.execute("DELETE FROM card WHERE number = ?", [number])
    conn.commit()
def useless(mpin):
    mpin = str(mpin)
    mpin = mpin.replace("[", '')
    mpin = mpin.replace("]", '')
    mpin = mpin.replace("(", '')
    mpin = mpin.replace(")", '')
    mpin = mpin.replace("'", '')
    mpin = mpin.replace(",", '')
    return mpin


library = {}
command = "start"
state = False
while command != "0":  
    print("1. Create an account\n"
    "2. Log into account\n"
    "0. Exit")
    command = input()
    print("")
    if command == "1":
        number = str(random.randint(100000000, 999999999))
        pin = str(random.randint(1000, 9999))
        sum = checksum(number)
        if sum == "10":
            sum = "0"
        new_card = ("400000" + number + sum, pin)
        cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', new_card )
        conn.commit()
        library["400000" + number + sum] = pin
        print("Your card has been created")
        print("Your card number:")
        print("400000" + number + sum)
        print("Your card PIN:")
        print(pin)
        print("")
    elif command == "2":
        command = "1"
        print("Enter your card number:")
        number = input()
        print("Enter your pin:")
        pin = input()
        print("")
        for iter in allkeyes():
            iter = ''.join(iter)
            if iter == number:
                if useless(getpin(number)) == pin:
                    state = True
                    print("You have successfully logged in!\n")
                    while command != "0":
                        print("1. Balance\n"
                        "2. Add income\n"
                        "3. Do transfer\n"
                        "4. Close account\n"
                        "5. Log out\n"
                        "0. Exit")
                        command = input()
                        print("")
                        if command == "1":
                            print("Balance: {0}\n", getbalance(number))
                        elif command == "5":
                            print("You have successfully logged out!\n")
                            break
                        elif command == "2":
                            print("Enter income:\n")
                            income = input()
                            addincome(number, income)
                            print(getbalance(number))
                        elif command == "3":
                            print("Enter card number:\n")
                            number2 = input()
                            vozvrat = checktransfervalidity(number2,number)
                            print(vozvrat)
                            if vozvrat == "How much money":
                                money = input()
                                transfermoney(number2, number, money)
                        elif command == "4":
                            closeacc(number)
                            print("The account has been closed!")
                            break

        if state != True:
            print("Wrong card number or PIN!\n")
print("Bye!")
