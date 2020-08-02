'''
things to do:
-add warning popups for
    -empty responses - done
    -existing file w/ same name - done
'''

import string
import random
import os.path
from stat import S_IREAD, S_IRGRP, S_IROTH
from tkinter import Tk
import tkinter as tk_window
from tkinter import messagebox
from tkinter.font import Font
from tkinter import IntVar
import psycopg2

class RandomPassGen(tk_window.Frame): #using class 

    window = None #the window associated with the GUI when putting components on
    #initiates variables
    file_name = ''
    username = ''
    length = 0
    gen_pass = ''

    #self references to this instance of the class
    def __init__(self): 
        self.length = random.randint(12,16)
        self.file_name = ""
        self.username = ""
        self.window = tk_window.Tk()

    #function used to generate password
    def gen_pass_method(self, length, uppercase, special_char):
        gen_pass = ""
        char = string.ascii_letters + string.digits #characters to select from when creating random password
        for i in range(length):
            gen_pass += random.choice(char)

        # to guarantee #
        gen_pass += str(random.randint(0, 9))
        if (uppercase.get()):
            gen_pass += string.ascii_uppercase[random.randint(0,len(string.ascii_uppercase) - 1)] #adds a random uppercase letter to password
        if (special_char.get()):
            s_char = "!@#$%^&*()-+=_"
            gen_pass += s_char[random.randint(0,len(s_char) - 1)] #adds a random special character to password
        return gen_pass

    #function that specifies what happens after a button is clicked (the OK button)
    def button_click(self, username_entry, file_name_entry, generated_pass, uppercase, special_char):
        if (file_name_entry.get() == '' or username_entry.get() == ''):
            messagebox.showwarning(title="Warning", message="You have not entered a value for one of the fields.")
        else:
            try: #try to generate a txt file with the username and filename and the password 
                file_name = file_name_entry.get()
                username = username_entry.get()

                self.gen_pass = self.gen_pass_method(self.length, uppercase, special_char)
                self.create_file(file_name,username, self.gen_pass) #calls the create file function to actually create the file

                generated_pass.configure(state = 'normal')
                generated_pass.delete(1.0, 'end')
                generated_pass.insert('current', self.gen_pass)
                generated_pass.pack()
                generated_pass.configure(state = 'disabled')
            except PermissionError: #catches error of when creating a file with the same name
                messagebox.showinfo(title="Warning", message="There is already a file with the same name :c")

    def create_file(self, file_name, username, gen_pass):
        #print("asda")
        file_dir = os.path.expanduser('~/Desktop') + "\\" + file_name + ".txt"
        newFile = open(file_dir, 'w+')
        newFile.write(file_name + '\n')
        newFile.write("Username:" + username + '\n')
        newFile.write("Password:" + gen_pass)
        newFile.close()
        #changes file to read only
        os.chmod(file_dir, S_IREAD|S_IRGRP|S_IROTH)

        upload_db((file_name, username, gen_pass))

# uploads the data to my local db
def upload_db(data):
    # print(data)
    try:
        passw = open(r"D:\Coding (Old)\Python\Random Password Generator\pass.cfg").readline().rsplit('\n')[0]
        connection = psycopg2.connect(user = "postgres",
                                    password = passw,
                                    host = "127.0.0.1",
                                    port = "5432",
                                    database = "passwords")
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

        SQL = "INSERT INTO public.passwords (website, username, password) VALUES (%s, %s, %s)"
        cursor.execute(SQL, data)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into mobile table")

    except Exception as error:
        print(error)
        
#executes main part of program which uses the class above
if __name__ == "__main__":

    rand = RandomPassGen() #creates rand object from class
    rand.window.configure(background = 'black')

    #configure the GUI below
    rand.window.title("Random Password Generator")
    x = 500
    y = 460
    rand.window.geometry(str(x)+"x"+str(y))
    rand.window.resizable(False,False)

    font1 = Font(family = "Calibri",size = 30,weight = 'bold')

    title = tk_window.Label(rand.window,font=font1,text="RANDOM # GENERATOR", bg = 'black', fg = 'white')
    title.pack()

    #creating decription
    desc = tk_window.Text(rand.window, height = 4, width = 40, wrap = 'word', font = 'Calibri', fg = 'white', bg = 'black', bd = 0)
    desc.tag_configure("center",justify = 'center')
    desc.insert(tk_window.INSERT ,'This app generates a random password. ' \
        + 'The app will generate a file with your credentials on your desktop.')
    desc.tag_add("center","1.0","end")
    desc.pack()
    desc.configure(state = 'disabled')

    empty = tk_window.Label(rand.window, bg = 'black')
    empty.pack()

    #create label which allows user to enter file name and user name
    get_file_name_label = tk_window.Label(rand.window, text = "File Name: ", bg = 'black', fg = 'white')
    get_file_name_label.pack()
    get_file_name = tk_window.Entry(rand.window, bg = 'gray20', fg = 'white')
    get_file_name.pack()

    get_user_name_label = tk_window.Label(rand.window, text = "Username: ", bg = 'black', fg = 'white')
    get_user_name_label.pack()
    get_username = tk_window.Entry(rand.window, bg = 'gray20', fg = 'white')
    get_username.pack()

    uppercase_needed = IntVar()
    uppercase = tk_window.Checkbutton(rand.window, text = "Uppercase Needed", variable = uppercase_needed, bg = 'black', fg = 'white', activebackground = 'black', activeforeground = 'white', selectcolor = 'black')
    uppercase.pack()

    special_char_needed = IntVar()
    special_char = tk_window.Checkbutton(rand.window, text = "Special Char Needed", variable = special_char_needed, bg = 'black', fg = 'white', activebackground = 'black', activeforeground = 'white', selectcolor = 'black')
    special_char.pack()

    empty = tk_window.Label(rand.window, bg = 'black')
    empty.pack()
    ufprompt = tk_window.Label(rand.window, bg = 'black', fg = 'white', text = 'Your password: ')
    generated_pass = tk_window.Text(rand.window, bg = 'gray20', fg = 'gray93', height = 2, width = 25)
    generated_pass.configure(state = 'disabled')

    # gen_pass = rand.gen_pass_method(RandomPassGen.length, uppercase_needed, special_char_needed)

    #create ok button and attach enter key press to the button
    get_ok = tk_window.Button(rand.window, text = 'OK', font = 'bold', height = 2, width = 10 , bg = 'black', fg = 'white', \
        command = lambda : rand.button_click(get_username, get_file_name, generated_pass, uppercase_needed, special_char_needed)) #using lambda to pass function with parameters
    get_ok.pack()
    rand.window.bind('<Return>', lambda event :rand.button_click(get_username, get_file_name, generated_pass, uppercase_needed, special_char_needed))

    empty.pack()
    ufprompt.pack()
    generated_pass.pack()

    rand.window.mainloop() #lets the window stay up