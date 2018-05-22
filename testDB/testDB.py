#!/usr/bin/python
# coding: UTF-8

import sqlite3, os

# установка соединения с БД
def connect(fileName, tableNames):
    isDbNotExists = not os.path.exists(fileName)
    # создание/открытие базы
    db = sqlite3.connect(fileName)
    if isDbNotExists:
        for tableName in tableNames:
            createTable(db, tableName)
    return db

# создание таблицы c названием `tableName`
def createTable(db, tableName):
    # exceptions: базы не существует
    try:    
        db.execute('CREATE TABLE ' + tableName +
             ''' (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             NAME           TEXT    NOT NULL,
             AGE            INT     NOT NULL,
             ADDRESS        CHAR(50),
             SALARY         REAL);''')
    except sqlite3.OperationalError as err:
        print('Warning: ' + err.message)
    else:
        db.commit()    

def addEmployee(db, tableName, emp):
    try:
        db.execute("INSERT INTO " + tableName + " (NAME,AGE,ADDRESS,SALARY) VALUES (?, ?, ?, ?)",
                    (emp.name, emp.age, emp.address, emp.salary));    
    except sqlite3.IntegrityError as err:
        print('Error: ' + err.message)
    else:
        db.commit()

def compareTables(db, tableName1, tableName2):
    cursor = db.cursor() 
    try:
        # запрос к бд
        for emp in cursor.execute("SELECT NAME,AGE,ADDRESS,SALARY FROM " + tableName1 + \
                                 " EXCEPT SELECT NAME,AGE,ADDRESS,SALARY FROM " + tableName2):
            print(emp)
            # из tuple в Employee
            # добавить emp в tableName2
            addEmployee(db, tableName2, Employee(emp[0], emp[1], emp[2], emp[3]))
    except sqlite3.DatabaseError as err:
        print("Error: " + err)
    else:
        db.commit()   

class Employee:
    def __init__(self, name, age, address, salary):
        self.name = name
        self.age = age
        self.address = address
        self.salary = salary

tableNames = ['horn', 'hoot']

db = connect('test.db', tableNames)

#createTable(db, '); drop tables --')# evil

paul = Employee('Paul', 32, 'California', 20000.00)
allen = Employee('Allen', 25, 'Texas', 15000.00)
teddy = Employee('Teddy', 23, 'Norway', 20000.00)
mark = Employee('Mark', 25, 'Rich-Mond ', 65000.00)

#addEmployee(db, tableNames[0], paul)
#addEmployee(db, tableNames[0], allen)
#addEmployee(db, tableNames[0], mark)
#addEmployee(db, tableNames[1], paul)
#addEmployee(db, tableNames[1], teddy)

compareTables(db, tableNames[0], tableNames[1])

db.close()
