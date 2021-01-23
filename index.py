from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import re


root = Tk()
root.title("Contact Book")
width = 700
height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#C4C4C4")

#VARIABLES
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
EMAIL = StringVar()
CONTACT = StringVar()



#METHODS

def Database():
    conn = sqlite3.connect("contactlist.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `Contacts` ([firstname] TEXT, [lastname] TEXT, [gender] TEXT, [email] TEXT NOT NULL  PRIMARY KEY, [contact] INTEGER)")
    cursor.execute("SELECT * FROM `Contacts` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    # c = conn.execute('select * from Contacts')
    # colnames = c.description
    # for row in colnames:
    #     print(row[0])

    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
        if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or EMAIL.get() == "" or CONTACT.get() == "":
            result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
        else:
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("contactlist.db")
            cursor = conn.cursor()
            emailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            phoneRegex = '^(\(\d{3}\)|\d{3})-?\d{3}-?\d{4}$'
            if (not re.search(emailRegex, str(EMAIL.get()))):
                result = tkMessageBox.showwarning('', 'Invalid Email!', icon="warning")
                cursor.execute("SELECT * FROM `Contacts` ORDER BY `firstname` ASC")
                fetch = cursor.fetchall()
                for data in fetch:
                    tree.insert('', 'end', values=(data))
                cursor.close()
                conn.close()
                return
            if (not re.search(phoneRegex, str(CONTACT.get()))):
                result = tkMessageBox.showwarning('', 'Invalid Phone Number!', icon="warning")
                cursor.execute("SELECT * FROM `Contacts` ORDER BY `firstname` ASC")
                fetch = cursor.fetchall()
                for data in fetch:
                    tree.insert('', 'end', values=(data))
                cursor.close()
                conn.close()
                return

            cursor.execute("INSERT INTO `Contacts` (firstname, lastname, gender, email, contact) VALUES(?, ?, ?, ?, ?)", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(EMAIL.get()), str(CONTACT.get())))
            conn.commit()
            cursor.execute("SELECT * FROM `Contacts` ORDER BY `firstname` ASC")
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
                print(data)
            cursor.close()
            conn.close()
            FIRSTNAME.set("")
            LASTNAME.set("")
            GENDER.set("")
            EMAIL.set("")
            CONTACT.set("")




def UpdateData():
    if GENDER.get() == "":
       result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contactlist.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `Contacts` SET `firstname` = ?, `lastname` = ?, `gender` = ?, `contact` = ? WHERE `email` = ? ", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(CONTACT.get()), str(EMAIL.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `Contacts` ORDER BY `firstname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        EMAIL.set("")
        CONTACT.set("")


def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("contactlist.db")
            cursor = conn.cursor()
            # print(selecteditem[3])
            cursor.execute("DELETE FROM `Contacts` WHERE `contact` = %d"% selecteditem[4])
            conn.commit()
            cursor.close()
            conn.close()


def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    EMAIL.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact Book")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    
    #FRAME
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male",  font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female",  font=('arial', 14)).pack(side=LEFT)
    
    #LABELS
    lbl_title = Label(FormTitle, text="Adding New Contact", font=('arial', 16), bg="#90EC69",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_email.grid(row=3, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=4, sticky=W)

    #ENTRY
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    email = Entry(ContactForm, textvariable=EMAIL,  font=('arial', 14))
    email.grid(row=3, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14))
    contact.grid(row=4, column=1)
    

    btn_addcon = Button(ContactForm, text="Save", width=40, command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)


def OnSelected():
    global email, UpdateWindow
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    email = selecteditem[3]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    # EMAIL.set("")
    CONTACT.set("")
    FIRSTNAME.set(selecteditem[0])
    LASTNAME.set(selecteditem[1])
    GENDER.set(selecteditem[2])
    EMAIL.set(selecteditem[3])
    CONTACT.set(selecteditem[4])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Contact Book")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width / 2) + 450) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    #FRAME
    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    #LABELS
    lbl_title = Label(FormTitle, text="Updating Contact", font=('arial', 16), bg="orange", width=300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_address = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_address.grid(row=3, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=4, sticky=W)

    #ENTRY
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    email = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
    email.grid(row=3, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
    contact.grid(row=4, column=1)

    btn_updatecon = Button(ContactForm, text="UPDATE", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)


#FRAMES
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500,  bg="#C4C4C4")
Mid.pack(side=TOP)
MidRight1 = Frame(Mid, width=100)
MidRight1.pack(side=LEFT, pady=20)
MidRight1Padding = Frame(Mid, width=10, bg="#C4C4C4")
MidRight1Padding.pack(side=RIGHT)
MidRight2 = Frame(Mid, width=100)
MidRight2.pack(side=RIGHT, pady=20)
MidRight3 = Frame(Mid, width=100)
MidRight3.pack(side=RIGHT, pady=20)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

#LABEL
lbl_title = Label(Top, text="CONTACT BOOK", font=('arial', 16), width=500)
lbl_title.pack(fill=X)


#BUTTONS
btn_add = Button(MidRight1, text="ADD NEW", bg="#90EC69", command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight2, text="DELETE", bg="#EC5050", command=DeleteData)
btn_delete.pack(side=RIGHT)
btn_update = Button(MidRight3, text="UPDATE", bg="orange", command=OnSelected)
btn_update.pack(side=RIGHT)

#TABLES
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Firstname", "Lastname", "Gender", "Email", "Contact"), height=300, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Email', text="Email", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=80)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=80)
tree.column('#4', stretch=NO, minwidth=0, width=150)
tree.pack()

#INITIALIZATION
if __name__ == '__main__':
    Database()
    root.mainloop()