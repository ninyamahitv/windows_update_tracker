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

# ------------------ User Interactions ------------------ #

print("\nWelcome to the Windows Update Tracker v1.1\n")

def func_welcome():
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
            func_welcome()
  
    except ValueError:
        print("\nYour input is not a valid character\n")
        func_welcome()

func_welcome()