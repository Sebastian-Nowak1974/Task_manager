# This is a program designed for a small business 
# to help it manage tasks assigned to each member of a team.
# Logged in user can register new users, add new tasks, 
# view and edit existing tasks and generate reports
# Use the following username and password to access the admin rights 
# username: admin
# password: password

import os
from datetime import datetime, date
import pandas as pd

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# This code reads in tasks data from text file
# If the file doesn't exists it's created 
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

tasks_data = {   'Asign to:': [],
                 'Task_title:': [],
                 'Description:': [],
                 'Due_date:': [],
                 'Assigned_date:': [],
                 'Completed:': []}
with open("tasks.txt", 'r') as task_file:        
    task_file_line = task_file.readline().strip('\n')            
    while task_file_line:
        task_data_list = task_file_line.split(';')                      
        for j, key in enumerate(tasks_data.keys()):
            tasks_data[key].append(task_data_list[j])                   
        task_file_line = task_file.readline().strip('\n')  


# This code reads usernames and password from the user.txt file to 
# allow a user to login.
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")        

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.readline().strip("\n")
    username_password = {}
    while user_data:
        username, password = user_data.split(';')
        username_password[username] = password
        user_data = user_file.readline().strip("\n")

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login successful!")
        logged_in = True


def reg_user():
    # reg_user() function adds new username and password
    new_user_registered = False
    while  not new_user_registered:                
        new_username = input("New Username: ")        
        if new_username not in username_password.keys():
            new_password = input("New Password: ")
            confirm_password = input("Confirm Password: ")   
            if new_password == confirm_password:
                username_password[new_username] = new_password
                with open("user.txt", 'a') as user_file:
                    user_file.write("\n" +new_username + ";" + new_password)                        
            else:
                print("Passwords do no match")
                continue  
            print("New user registered successfully")
            new_user_registered = True
        else:
            print("The username already exist. Try another username")
           
def view_all():  
    # Displays list of tasks. The user can view the task by 
    # selecting task number from the list
    tasks_list = '\nNo.\tTask title\n'      
    task_num = 0
    for task_title in tasks_data['Task_title:']:
        tasks_list += f'{task_num}\t{task_title}   <{tasks_data["Asign to:"][task_num]}>\n'
        task_num += 1 
    if task_num == 0:
        print('No tasks to display')         
    else: 
        print(tasks_list)        
    while task_num != 0:                
        try: 
            user_input = input('Select task number to view the task, r to refresh tasks list\
                             \nor b to go back to main menu: ')            
            if user_input == 'r':                
                print(tasks_list)
                continue
            elif user_input == 'b':
                break
            user_input = int(user_input)    
            if user_input >= 0:     
                display_task(user_input)    
            else:
                print('Incorrect entry') 
                continue                  
        except (ValueError, IndexError): 
            print('Incorrect entry')
            continue          

def display_task(num, line_lenght = 47):
    disp_task = ''    
    for key, value in tasks_data.items():
        if key == 'Description:':
            # Breaks long description into smaller lines of text
            if len(tasks_data[key][num]) > line_lenght:
                line_split = tasks_data[key][num].split()
                line_slice = ''
                line_to_print = ''
                for word in line_split:
                    if len(line_slice) < line_lenght:
                        line_slice += word + ' '
                    else:
                        line_to_print += line_slice + word +'\n\t\t\t'
                        line_slice = ''
                else:
                    line_to_print += line_slice
                disp_task += f'{key}\t\t{line_to_print}\n'
                continue
        disp_task += f'{key}\t\t{value[num]}\n'
    print('\n' + disp_task)

def add_task():
    new_task_data_list = []
    for key in tasks_data.keys():        
        if key == 'Asign to:':
            print('Enter username from the list below')
            for user in username_password.keys():
                print(user, end=', ')
            print()               
            user_input = input(key + '\t\t')
            while user_input not in username_password.keys():
                print("Username does not exist. Please enter a valid username")
                user_input = input(key + '\t\t')                
            tasks_data[key].append(user_input)
            new_task_data_list.append(user_input)
        elif key == 'Assigned_date:':
            today_date = date.today()            
            tasks_data[key].append(today_date.strftime(DATETIME_STRING_FORMAT))
            new_task_data_list.append(today_date.strftime(DATETIME_STRING_FORMAT))
        elif key == 'Due_date:':
            while True:
                try:
                    user_input = input("Due_date (YYYY-MM-DD): ")
                    due_date = datetime.strptime(user_input, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print("Invalid date format. Please use the format specified")
            tasks_data[key].append(due_date.strftime(DATETIME_STRING_FORMAT))
            new_task_data_list.append(due_date.strftime(DATETIME_STRING_FORMAT))   
        elif key ==  'Completed:':
            tasks_data[key].append('n')
            new_task_data_list.append('n')
        else:
            user_input = input(key + '\t\t')
            tasks_data[key].append(user_input)
            new_task_data_list.append(user_input)
    
    with open('tasks.txt', 'a') as task_file:
        task_file.write(';'.join(new_task_data_list) + '\n')   
    print('Task registered successfully')   

def edit_task(num):  
    # Allows the user to reassign task, change due date or mark task as complete
    # This function is called in view_mine()
    user_sel = input('Select w to edit task, c to mark as completed or b to go back: ').lower()
    if user_sel == 'c':
        tasks_data['Completed:'][num] = 'y'
        print('The task has been marked as completed. Select r to refresh tasks list or')
    elif user_sel == 'w':
        new_user_assigned = False
        new_date_assinged = False
        while True: 
            user_input = input('Select u to assign new user, d to change due date or b to go back: ')
            if user_input == 'u':    
                new_user_assigned = False                      
                while  not new_user_assigned:                
                    new_username = input("New username: ")
                    if new_username not in username_password.keys():
                        print("The username does not exist")
                        continue
                    else:
                        tasks_data['Asign to:'][num] = new_username
                        new_user_assigned = True
            elif user_input == 'd':     
                new_date_assinged = False          
                while not new_date_assinged:
                    try:
                        user_input = input("Due_date (YYYY-MM-DD): ")
                        due_date = datetime.strptime(user_input, DATETIME_STRING_FORMAT)
                        tasks_data['Assigned_date:'][num] = due_date.strftime(DATETIME_STRING_FORMAT)
                        new_date_assinged = True
                    except ValueError:
                        print("Invalid date format. Please use the format specified")
            elif user_input == 'b':
                print('All changes have been saved, select r to refresh tasks list or')
                break  
            else:
                print('Incorrect entry') 
        if new_user_assigned == True or new_date_assinged == True:
            line_to_write = ''
            for i in range(len(tasks_data['Asign to:'])):
                line = []
                for value in tasks_data.values():
                    line.append(value[i])
                line_to_write += ';'.join(line) + '\n'      
            with open('tasks.txt', 'w') as file_update:
                file_update.write(line_to_write)

    elif user_sel == 'b':
        pass
    else:
            print('Incorrect entry')  

def view_mine(): 
# j enumerates all tasks, while i enumerates current user's tasks  
# i_to_j list maps index value i to j
    i = 0
    i_to_j =[]
    tasks_list = '\nNo.\tTask title\n'
    for j, user in enumerate(tasks_data['Asign to:']):
        if user == curr_user:
            tasks_list += f'{i} \t {tasks_data["Task_title:"][j] }\n'
            i_to_j.append(j)
            i += 1  
    if i != 0:
        print(tasks_list) 
    else: 
        print('No tasks to display')                  
    while i != 0:                   
        try: 
            task_num = input('Select task number to view/edit the task or b to go back to main menu\
                             \n(Tasks marked as complete cannot be changed): ')                 
            if task_num == 'r':               
                view_mine()
                break
            elif task_num == 'b':
                break                             
            task_num = i_to_j[int(task_num)]
            display_task(task_num)
            if tasks_data['Completed:'][task_num] == 'n':
                edit_task(task_num)           
        except (ValueError, IndexError): 
            print('Incorrect entry')
            continue      

def gen_report():
    # The user can generate report using padnas data frame
    # It can be displayed by admin
    total = len(tasks_data['Asign to:'])
    def gen_data(username):        
        tasks = uncomp = overdue = 0
        if username not in tasks_data['Asign to:']:
            return [username, 0, 0, 0, 0, 0, 0, 0, 0]
        else:    # This loop counts number of tasks                        
            for i, user in enumerate(tasks_data['Asign to:']):
                if user == username:
                    tasks += 1
                    if tasks_data['Completed:'][i] == 'n':
                        uncomp += 1
                        due_date = datetime.strptime(tasks_data['Due_date:'][i],\
                            DATETIME_STRING_FORMAT).date()
                        today_date = date.today()
                        if due_date < today_date:
                            overdue += 1
            comp = tasks - uncomp            
            return [username, tasks, f'{tasks/total*100:.1f}' , comp, f'{comp/tasks*100:.1f}', uncomp, \
                   f'{uncomp/tasks*100:.1f}', overdue, f'{overdue/tasks*100:.1f}']
  
    my_data ={}
    keys = ['username', '    A', 'A/T[%]', '    C', 'C/A[%]', '    U', 'U/A[%]', '    O', 'O/A[%]']
    for i, key in enumerate(keys):
        my_data[key] = [gen_data(username)[i] for username in username_password.keys()]
    def _total(key):
        total = 0
        for num in my_data[key]:
            total += num
        return total
    c_total = _total('    C')
    u_total = _total('    U')
    o_total = _total('    O')
    last_row = ['users in total', total , '100.0' , c_total, f'{c_total/total*100:.1f}', u_total, \
            f'{u_total/total*100:.1f}', o_total, f'{o_total/total*100:.1f}']
    for i, key in enumerate(my_data.keys()):
        my_data[key].append(last_row[i])
    df = pd.DataFrame(my_data)
    df.to_csv('task_manager_overview.txt', sep = ' ', index = False)
       

while True:      
    print()
    menu = input('''Select one of the following Options below:
r   - Register a user
a   - Add a task
va  - View all tasks
vm  - View my tasks
gr  - Generate report
ds  - Display statistics
e   - Exit
: ''').lower()

    if menu == 'r':
        reg_user()    
    elif menu == 'a':
        add_task()       
    elif menu == 'va':
        view_all()          
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        gen_report()  
        print('The report has been generated')                
    elif menu == 'ds':
        # Allows admin user to display report
        if curr_user == 'admin':         
            print('\nT - total number of tasks assigned\
             \nA - number of tasks assigned to the user\
             \nC - number of completed tasks\
             \nU - number of uncompleted tasks\
             \nO - number of overdue tasks\n')
            if not os.path.exists("task_manager_overview.txt"):
                gen_report()
            df = pd.read_csv('task_manager_overview.txt', sep = ' ')                         
            print(df)
            print()
            input('Press enter to go back to main menu: ')
        else:
            print('You need admin rights to run this section')         
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, please try again")
