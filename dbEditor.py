import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def enter_item(conn, item):
    cursor = conn.cursor()
    sql = ''' INSERT INTO item(name, category, basePrice)
                VALUES(?,?,?)'''
    cursor.execute(sql, item)
    conn.commit()
    return cursor.lastrowid

def enter_store(conn, store):
    cursor = conn.cursor()
    sql = ''' INSERT INTO store(name, tag, args, value)
                VALUES(?,?,?,?)'''
    cursor.execute(sql, store)
    conn.commit()
    return cursor.lastrowid

def enter_stock(conn, stock):
    cursor = conn.cursor()
    sql = ''' INSERT INTO stock(item, store, url)
                VALUES(?,?,?)'''
    cursor.execute(sql, stock)
    conn.commit()
    return cursor.lastrowid

conn = create_connection("onlineShopping.db")
while (True):
    userInput = input("Enter [I]tem, [S]tore or [St]ock\n")

    if (userInput.lower() == 'i' or userInput.lower() == "item"):
        name = input("Enter item name: ")
        category = input("Enter item category: ")
        basePrice = input("Enter item base price: ")
        print("Entering " + name + " | " + category + " | " + basePrice)
        if (input("If correct, enter to confirm or x to cancel: ").lower() == 'x'):
            print("Operation cancelled")
        else:
            item = (name, category, basePrice)
            enter_item(conn, item)
    elif (userInput.lower() == 's' or userInput.lower() == "store"):
        name = input("Enter store name: ")
        tag = input("Enter store tag: ")
        args = input("Enter tag arguments: ")
        value = input("Enter argument value: ")
        print("Entering " + name + " | " + tag + " | " + args + " | " + value)
        if (input("If correct, enter to confirm or x to cancel: ").lower() == 'x'):
            print("Operation cancelled")
        else:
            store = (name, tag, args, value)
            enter_store(conn, store)
    elif (userInput.lower() == 'st' or userInput.lower() == "stock"):
        item = input("Enter item name: ")
        store = input("Enter store name: ")
        url = input("Enter product's url for store: ")
        print("Entering " + item + " | " + store + " | " + url)
        if (input("If correct, enter to confirm or x to cancel: ").lower() == 'x'):
            print("Operation cancelled")
        else:
            stock = (item, store, url)
            enter_stock(conn, stock)
    else:
        print("Command not recognised")
    print()