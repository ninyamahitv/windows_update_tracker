# ------------------ Database Initialisation ------------------ #

import sqlite3

def db_connection():
    conn = sqlite3.connect('windows_uptracker.db')
    cursor = conn.cursor()
    return conn, cursor

db_connect,db_cursor = db_connection()

db_cursor.execute("""CREATE TABLE IF NOT EXISTS server_status (
                server_hostname text,
                operating_system text,
                installed_update text
                  )           
                """)

db_connect.close()

def db_variables():

    global server_list
    global server_names

    db_connect,db_cursor = db_connection()
    db_cursor.execute("SELECT * FROM server_status")
    server_list = db_cursor.fetchall()
    db_connect.close()

    server_names = [x[0] for x in server_list]

def server_table():

    db_variables()

    print("\n-***-  Server Status -***-\n")
    print(f"{'Server Hostname':<25} {'Operating System':<25} {'Installed Update':<25}")
    print("-" * 70)

    for server in server_list:
        print(f"{server[0]:<25} {server[1]:<25} {server[2]:<25}")

# ------------------ CRUD Functions ------------------ #

#---READ---#

def server_status():

    server_table()

    func_menu()

#---CREATE---#

def add_new_server():

    server_table()

    new_server = str(input("\nWhat is the hostname of the new server? Type quit to exit.\n\n"))

    if new_server == "quit":
        func_menu()
    elif new_server in server_names:
        print(f"\n{new_server} already exists, please enter a new server hostname")
        add_new_server()
    else:
        new_server_os = str(input("\nWhat OS is it running? Type quit to exit.\n\n"))

        if new_server_os == "quit":
            func_menu()
        else:
            new_server_patch = str(input("\nWhat is its most recent security patch (KB number)? Type quit to exit.\n\n"))

            if new_server_patch == "quit":
                func_menu()
            else:
                db_connect,db_cursor = db_connection()
                db_cursor.execute("INSERT INTO server_status VALUES (?, ?, ?)",(new_server,new_server_os,new_server_patch))
                db_connect.commit()
                db_connect.close()
                print(f"\n{new_server} has been added with {new_server_os} OS and {new_server_patch} security patch\n")
                func_menu()

#---UPDATE---#

def update_server():

    server_table()

    updated_server = str(input("\nWhat is the name of the server to be updated? Type quit to exit.\n\n"))

    if updated_server == "quit":
        func_menu()
    elif updated_server not in server_names:
        print(f"\n{updated_server} is not a recorded server\n")
        update_server()
    else:
        updated_server_os = str(input("\nWhat OS is it now running? Type quit to exit\n\n"))

        if updated_server_os == "quit":
            func_menu()
        else:
            updated_server_patch = str(input("\nWhat security patch does it now have (KB number)? Type quit to exit\n\n"))

            if updated_server_patch == "quit":
                func_menu()
            else:
                db_connect,db_cursor = db_connection()
                db_cursor.execute("UPDATE server_status SET operating_system = ?, installed_update = ? WHERE server_hostname  = ?",(updated_server_os,updated_server_patch,updated_server))
                db_connect.commit()
                db_connect.close()
                print(f"{updated_server} has been updated with {updated_server_os} OS and {updated_server_patch} security patch")
                func_menu()

#---DELETE---#

def delete_server():

    server_table()

    deleted_server = str(input("\nServer: "))

    if deleted_server == "quit":
        func_menu()
    elif deleted_server in server_names:
        db_connect,db_cursor = db_connection()
        db_cursor.execute("DELETE FROM server_status WHERE server_hostname = ?",(deleted_server,))
        db_connect.commit()
        db_connect.close()
        print(f"\n{deleted_server} has been removed\n")
        func_menu()
    else:
        print(f"\n{deleted_server} does not exist in the table\n")
        delete_server()

# ------------------ User Menu ------------------ #

print("\nWelcome to the Windows Update Tracker v1.1\n")

def func_menu():
    try:
        user_choice = int(input("\nPress 1 to see the status of all servers\nPress 2 to add a new server\nPress 3 to update an existing server\nPress 4 to delete a server\nPress 0 to quit\n\n"))

        if user_choice == 1:
            print("\n Here is the current patch status of all servers\n")
            server_status()
        elif user_choice == 2:
            print("\nAdding a new server and it's associated patch\n")
            add_new_server()
        elif user_choice == 3:
            print("\nUpdating an exisiting server OS and security patch\n")
            update_server()
        elif user_choice == 4:
            print("\nWhich server do you need to delete? Type quit to exit.\n")
            delete_server()
        elif user_choice == 0:
            print("\nGoodbye!\n")
            quit()
        else:
            print("\nYour choice is not valid\n")
            func_menu()

    except ValueError:
        print("\nYour input is not a valid character\n")
        func_menu()

func_menu()
