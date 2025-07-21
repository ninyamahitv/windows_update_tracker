 # ------------------ Database Initialisation ------------------ #

import sqlite3

conn = sqlite3.connect('windows_uptracker.db')    #connection object for database. File saved as windows_uptracker.db

cursor = conn.cursor()                                                              #variable called cursor allows for sql commands

cursor.execute("""CREATE TABLE IF NOT EXISTS server_status (          
                server_hostname text,
                operating_system text,
                installed_update text
                  )           
                """)

# ------------------ CRUD Functions ------------------ #

#---READ---#

def server_status():
    cursor.execute("SELECT * FROM server_status")
    print(cursor.fetchall())

    func_menu()

#---CREATE---#

def add_new_server():
    global new_server
    global new_server_OS
    global new_server_patch
                                                              
    new_server = str(input("\nWhat is the name of the new server? Type quit to exit.\n\n"))

    if new_server == "quit":
        func_menu()
    else:    
        new_server_OS = str(input("\nWhat OS is it running? Type quit to exit.\n\n"))
        
        if new_server_OS == "quit":
            func_menu()
        else:
            new_server_patch = str(input("\nWhat is its most recent security patch (KB number)? Type quit to exit.\n\n"))

            if new_server_patch == "quit":
                func_menu()
            else:
                cursor.execute("INSERT INTO server_status VALUES (?, ?, ?)",(new_server,new_server_OS,new_server_patch))
                conn.commit()
                print(f"\n{new_server} has been added with {new_server_OS} OS and {new_server_patch} security patch\n")
                func_menu()

#---UPDATE---#

def update_server():

    global updated_server
    global updated_server_OS
    global updated_server_patch

    cursor.execute("SELECT * FROM server_status")

    update_list = cursor.fetchall() # saves the query for the server hostname as a variable, that we can check agaist

    print(update_list)
                                                              
    updated_server = str(input("\nWhat is the name of the server to be updated? Type quit to exit.\n\n"))
   
    server_names = [x[0] for x in update_list]

    if updated_server == "quit":
        func_menu()

    elif updated_server not in server_names:
        print(f"{updated_server} is not a recorded server\n")
        update_server()  
    
    else:
        updated_server_OS = str(input("\nWhat OS is it now running? Type quit to exit\n\n"))
        
        if updated_server_OS == "quit":
                func_menu()
        else:
            updated_server_patch = str(input("\nWhat security patch doess it now have (KB number)? Type quit to exit\n\n"))

            if updated_server_patch == "quit":
                func_menu()
            else:
                cursor.execute("UPDATE server_status SET operating_system = ?, installed_update = ? WHERE server_hostname  = ?",(updated_server_OS,updated_server_patch,updated_server))
                conn.commit()
                print(f"{updated_server} has been updated with {updated_server_OS} OS and {updated_server_patch} security patch")
                func_menu()
    
#---DELETE---#

def delete_server():

    global deleted_server
    
    cursor.execute("SELECT server_hostname FROM server_status")     # Selects all the server hostnames in the database
    
    server_list = cursor.fetchall() # saves the query for the server hostname as a variable, that we can check agaist

    print(server_list)        # Prints all the server hostnames in the database

    deleted_server = str(input("\nServer: "))

    if (deleted_server,) in server_list:
        cursor.execute("DELETE FROM server_status WHERE server_hostname = ?",(deleted_server,))
        conn.commit()
        print(f"{deleted_server} has been removed")
        func_menu()
    
    elif deleted_server == "quit":
        func_menu()

    else:
        print(f"{deleted_server} does not exist in the table")
        delete_server()

# ------------------ User Menu ------------------ #

print("\nWelcome to the Windows Update Tracker v1.1\n")

def func_menu():
    try:
        user_choice = int(input("\nPress 1 to see the status of all servers\nPress 2 to add a new server\nPress 3 to update an existing server\nPress 4 to delete a server\nPress 0 to quit\n\n")) 
        
        if user_choice == 1:
            print(f"\n Here is the current patch status of all servers\n")
            #server_status()
        elif user_choice == 2:
            print("\nAdding a new server and it's associated patch\n")
            #add_new_server()
        elif user_choice== 3:
            print("\nUpdating an exisiting server OS and security patch\n")
            #update_server()
        elif user_choice== 4:
            print("\nWhich server do you need to delete? Type quit to exit.\n")
            #delete_server()
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