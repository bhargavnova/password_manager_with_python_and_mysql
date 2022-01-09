import string
import subprocess
import random
import sqlite3
import mysql.connector
from tabulate import tabulate
import sys

uppercase_letters = string.ascii_uppercase
lowercase_letters = string.ascii_lowercase
digits = string.digits
special_symbols = '@#%&!$'


# You can add more names here
names_list = ['Zackery Orn','Dayton Powlowski','Brant Muller']

def create_table():
    sql_string = """CREATE TABLE IF NOT EXISTS passdata (passid INTEGER PRIMARY KEY, username VARCHAR(40), password VARCHAR(40), appname VARCHAR(40), email VARCHAR(60));"""
    fake_sql_string = """CREATE TABLE IF NOT EXISTS fakeaccountdata (passid INTEGER PRIMARY KEY, username VARCHAR(40), password VARCHAR(40), firstname VARCHAR(40), lastname VARCHAR(40), appname VARCHAR(40), email VARCHAR(60));"""
    print("[+] Creating SQL Table .....")
    cur = conection.cursor()
    cur.execute(sql_string)
    cur.execute(fake_sql_string)

conection = sqlite3.connect('db.sqlite3')
create_table()

def generate_random_password(length,up=True,low=True,digit=True,symbols=True):
    random_password_string = ""
    if up:
        random_password_string += uppercase_letters
    if low:
        random_password_string += lowercase_letters
    if digit:
        random_password_string += digits
    if symbols:
        random_password_string += special_symbols
    generated_password = ''.join(random.sample(random_password_string,k=length))
    return generated_password


def store_password(username,appname,email,password):
    cur = conection.cursor()
    sql_insert_query = """ INSERT INTO passdata (username, password, appname, email) VALUES ('"""+username+"""','"""+password+"""','"""+appname+"""','"""+email+"""')"""
    cur.execute(sql_insert_query)
    conection.commit()

def store_fake_data_password(username,password,firstname,lastname,appname,email):
    cur = conection.cursor()
    sql_insert_query = """ INSERT INTO fakeaccountdata (username, password, firstname, lastname, appname, email) VALUES ('"""+username+"""','"""+password+"""','"""+firstname+"""','"""+lastname+"""','"""+appname+"""','"""+email+"""')"""
    cur.execute(sql_insert_query)
    conection.commit()

def find_users(user_email):
    cursor = conection.cursor()
    sql_select_query = """ SELECT * FROM passdata WHERE email = '"""+user_email+"""'"""
    cursor.execute(sql_select_query)
    conection.commit()
    result = cursor.fetchall()
    table = tabulate(result,headers=["Username","Password","App/Site Name", "Email"],tablefmt='orgtbl')
    print(table)

def find_password(table_name,app_name):
    cursor = conection.cursor()
    sql_select_query = """ SELECT password FROM """+ table_name +""" WHERE appname = '"""+app_name+"""'"""
    cursor.execute(sql_select_query)
    conection.commit()
    result = cursor.fetchone()
    if result:
        print('\n')
        print("[+] Account Found ")
        print("-"*30)
        print('Password For: ',app_name)
        print("\n")
        print(result[0])
        print("\n")
        print("-"*30)
    else:
        print("[-] No Accout Found ")

def show_all_passwords(table_name):
    cursor = conection.cursor()
    sql_select_query = """ SELECT * FROM """+table_name+""" """
    cursor.execute(sql_select_query)
    conection.commit()
    result = cursor.fetchall()
    if table_name == 'passdata':
        table = tabulate(result,headers=["Record ID","Username","Password","App/Site Name", "Email"],tablefmt='orgtbl')
    elif table_name == 'fakeaccountdata':
        table = tabulate(result,headers=["Record ID","Username","Password","FirstName","LastName","App/Site Name", "Email"],tablefmt='orgtbl')
    else:
        table = None
    print(table)

def generate_password():
    username = input("Enter Username : ")
    appname = input("Enter Appname : ")
    email = input("Enter Email : ")
    password = generate_random_password(10)
    store_password(username,appname,email,password)
    print("Your has been stored Here it is ..... \n\n")
    print("-"*30)
    print(password)
    print("-"*30)
    print("\n\n")

def generate_fake_account():
    name = random.choice(names_list)
    firstname = name.split(' ')[0]
    lastname = name.split(' ')[1]
    username = input("Enter Username : ")
    appname = input("Enter Appname : ")
    email = input("Enter Email : ")
    password = generate_random_password(10)
    store_fake_data_password(username,password,firstname,lastname,appname,email)
    print("Your has been stored Here it is ..... \n\n")
    print("-"*30)
    print("FirstName : ",firstname)
    print("LastName : ", lastname)
    print("UserName : ", username)
    print("AppName : ",appname)
    print("Email : ",  email)
    print("Password : ",password)
    print("-"*30)
    print("\n\n")

def update_password_data(table_name,passid):
    what_to_do = input(" Do You wish to update with custom Password ? Y/N : ")
    if what_to_do.lower() == 'y':
        updated_password = input("Enter Your Password : ")
    else:
        length = input("Enter length of password : ")
        updated_password = generate_random_password(int(length))
    cursor = conection.cursor()
    sql_update_query = """ UPDATE """+ table_name +""" SET password = '"""+ updated_password +"""' WHERE passid = """+ passid +""" """
    cursor.execute(sql_update_query)
    conection.commit()
    print("[+] Password Updated Successfully")

def update_other_data(table_name,passid,field_name):
    updated_value = input("Enter Value For New {} : ".format(field_name))
    cursor = conection.cursor()
    sql_update_query = """ UPDATE """+ table_name +""" SET """+ field_name +""" = '"""+ updated_value +"""' WHERE passid = """+ passid +""" """
    cursor.execute(sql_update_query)
    conection.commit()
    print("[+] {} Updated Successfully".format(field_name))

def delete_password_data(table_name,passid):
    cursor = conection.cursor()
    cursor.execute("""DELETE FROM """+ table_name +""" WHERE passid = %s""" % passid )
    conection.commit()
    print("[+] Delete Password Data Successfully")

if __name__ == "__main__":
    while True:
        print('-'*30)
        print(('-'*13) + 'Password Manager @techdobz'+ ('-' *13))
        print('1. Create New Password')
        print('2. Create New Fake Account')
        print('3. Search By Email')
        print('4. Search By App Name')
        print('5. Update Data & Delete Data For Personal Passwords')
        print('6. Update Data & Delete Data For Fake Passwords')
        print('7. Show all Passwords')
        print('Q. Exit')
        print('-'*30)
        choice = input(": ")
        if choice.lower() == 'q':
            sys.exit()
        elif choice == '7':
            print('1. Personal Passwords')
            print('2. Fake Account Passwords')
            second_choice = input(": ")
            if second_choice == '1':
                show_all_passwords("passdata")
            elif second_choice == '2':
                show_all_passwords("fakeaccountdata")
            else:
                print("Please enter valid choise")
        elif choice == '6':
            print('1. Update Password')
            print('2. Update Other Details')
            print('3. Delete Password')
            second_choice = input(": ")
            if second_choice == '1':
                id = input("Enter Id of password : ")
                update_password_data("fakeaccountdata",id)
            elif second_choice == '2':
                fields = {'1': 'username', '2' : 'firstname', '3' : 'lastname', '4' : 'appname', '5' : 'email'}
                id = input("Enter Id of password : ")
                f_id=input("1 : username, 2 : firstname, 3 : lastname, 4 : appname, 5 : email")
                field_name = fields[f_id]
                update_other_data("fakeaccountdata",id,field_name)
            elif second_choice == '3':
                id = input("Enter Id of password : ")
                delete_password_data("fakeaccountdata",id)
            else:
                print("Please enter valid choise")
        elif choice == '5':
            print('1. Update Password')
            print('2. Update Other Details')
            print('3. Delete Password')
            second_choice = input(": ")
            if second_choice == '1':
                id = input("Enter Id of password : ")
                update_password_data("passdata",id)
            elif second_choice == '2':
                fields = {'1': 'username', '2' : 'appname', '3' : 'email'}
                id = input("Enter Id of password : ")
                f_id=input("1 : username, 2 : appname, 3 : email")
                field_name = fields[f_id]
                update_other_data("passdata",id,field_name)
            elif second_choice == '3':
                id = input("Enter Id of password : ")
                delete_password_data("passdata",id)
            else:
                print("Please enter valid choise")
        elif choice == '4':
            app_name = input("Enter App Name : ")
            find_password("passdata",app_name)
            find_password("fakeaccountdata",app_name)
        elif choice == '3':
            email = input("Enter Email Address : ")
            find_users(email)
        elif choice == '2':
            generate_fake_account()
        elif choice == '1':
            generate_password()
