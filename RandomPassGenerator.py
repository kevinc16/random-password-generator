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

class RandomPassGen(tk_window.Frame):

    char = string.ascii_letters + string.punctuation + string.digits

    window = None
    file_name = ''
    username = ''
    length = 0
    gen_pass = ''

    #self references to this instance of the class
    def __init__(self):
        self.length = random.randint(14,18)
        self.file_name = ""
        self.username = ""
        self.window = tk_window.Tk()

    def gen_pass_method(self, length):
        gen_pass = ""
        for i in range(length):
            gen_pass += random.choice(self.char)
        return gen_pass

    def button_click(self, username_entry, file_name_entry, generated_pass):
        if (file_name_entry.get() == '' or username_entry.get() == ''):
            messagebox.showwarning(title="Warning", message="You have not entered a value for one of the fields.")
        else:
            try:
                file_name = file_name_entry.get()
                username = username_entry.get()

                self.gen_pass = self.gen_pass_method(self.length)
                self.create_file(file_name,username, self.gen_pass)

                generated_pass.configure(state = 'normal')
                generated_pass.delete(1.0, 'end')
                generated_pass.insert('current', self.gen_pass)
                generated_pass.pack()
                generated_pass.configure(state = 'disabled')
            except:
                messagebox.showinfo(title="Warning", message="There is already a file with the same name :c")

    def create_file(self, file_name, username, gen_pass):
        #print("asda")
        file_dir = os.path.expanduser('~/Desktop') + "\\" + file_name + ".txt"
        newFile = open(file_dir, 'w+')
        newFile.write(file_name + '\n')
        newFile.write("Username:" + username + '\n')
        newFile.write("gen_passord:" + gen_pass)
        newFile.close()
        #changes file to read only
        os.chmod(file_dir, S_IREAD|S_IRGRP|S_IROTH)
        

if __name__ == "__main__":

    rand = RandomPassGen()
    rand.window.configure(background = 'black')

    rand.window.title("Random Password Generator")
    x = 500
    y = 460
    rand.window.geometry(str(x)+"x"+str(y))
    rand.window.resizable(False,False)

    font1 = Font(family = "Calibri",size = 30,weight = 'bold')

    title = tk_window.Label(rand.window,font=font1,text="RANDOM # GENERATOR", bg = 'black', fg = 'white')
    title.pack()

    desc = tk_window.Text(rand.window, height = 5, width = 40, wrap = 'word', font = 'Calibri', fg = 'white', bg = 'black', bd = 0)
    desc.tag_configure("center",justify = 'center')
    #desc.tag_configure()
    desc.insert(tk_window.INSERT ,'This app generates a random password between the length of 14 to 18 characters. The app will generate a file with your credentials on your desktop.')
    desc.tag_add("center","1.0","end")
    desc.pack()
    desc.configure(state = 'disabled')

    empty = tk_window.Label(rand.window, bg = 'black')
    empty.pack()

    get_file_name_label = tk_window.Label(rand.window, text = "File Name: ", bg = 'black', fg = 'white')
    get_file_name_label.pack()
    get_file_name = tk_window.Entry(rand.window, bg = 'gray20', fg = 'white')
    get_file_name.pack()

    get_user_name_label = tk_window.Label(rand.window, text = "Username: ", bg = 'black', fg = 'white')
    get_user_name_label.pack()
    get_username = tk_window.Entry(rand.window, bg = 'gray20', fg = 'white')
    get_username.pack()

    empty = tk_window.Label(rand.window, bg = 'black')
    empty.pack()

    empty = tk_window.Label(rand.window, bg = 'black')
    ufprompt = tk_window.Label(rand.window, bg = 'black', fg = 'white', text = 'Your password: ')
    generated_pass = tk_window.Text(rand.window, bg = 'gray20', fg = 'gray93', height = 2, width = 25)
    generated_pass.configure(state = 'disabled')

    gen_pass = rand.gen_pass_method(RandomPassGen.length)

    #create ok button and attach enter key press to the button
    get_ok = tk_window.Button(rand.window, text = 'OK', font = 'bold', height = 2, width = 10 , bg = 'black', fg = 'white', command = lambda : rand.button_click(get_username, get_file_name, generated_pass))
    get_ok.pack()
    rand.window.bind('<Return>', lambda event :rand.button_click(get_username, get_file_name, generated_pass))

    empty.pack()
    ufprompt.pack()
    generated_pass.pack()

    rand.window.mainloop()

#doesnt work
'''
r = Tk()
r.withdraw()
r.clipboard_clear()
r.clipboard_append(gen_pass)
r.update()
r.destroy()
'''