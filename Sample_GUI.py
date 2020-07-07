import tkinter as tk
import sqlite3
from functools import partial


usernameEntry = ""
passwordEntry = ""
PatientNameEntry = ""
ContactNumberEntry = ""
AgeEntry = ""
AddressEntry = ""
loginWindow = ""
receptionWindow = ""
doctorWindow = ""
genderEntry = ""


PD = open('Patient_Details_File','w')
PD.close()


def LoginWindow(parameter):
    global usernameEntry, passwordEntry, loginWindow

    if parameter == 1:
        mainWindow.withdraw()
    elif parameter == 2:
        receptionWindow.destroy()
    else:
        doctorWindow.destroy()
        
    loginWindow = tk.Toplevel()
    #loginWindow.geometry('200x70')       
    tk.Label(loginWindow, text="User Name").grid(row=2)
    tk.Label(loginWindow, text="Password").grid(row=3)

    userName = tk.StringVar()
    password = tk.StringVar()

    usernameEntry = tk.Entry(loginWindow, textvariable=userName)
    usernameEntry.grid(row=2,column=1)
    passwordEntry = tk.Entry(loginWindow, textvariable=password, show='*')
    passwordEntry.grid(row=3,column=1)

    loginButton = tk.Button(loginWindow, text="Login", command=Check_Credentials)
    loginButton.grid(row=4,columnspan=2)

    '''img = tk.PhotoImage(file="D:\\Personnel_Documents\\Passport_Photo.png")
    imgLabel = tk.Label(loginWindow, image=img)
    imgLabel.place(x=0, y=0, height=200, width=70)'''
    
    loginWindow.protocol("WM_DELETE_WINDOW", mainWindow.destroy)    
    loginWindow.mainloop()


def Check_Credentials():
    global loginWindow
    if usernameEntry.get() == "reception" and passwordEntry.get() == "reception@123":
        loginWindow.destroy()
        ReceptionWindow()
    elif usernameEntry.get() == "doctor" and passwordEntry.get() == "doctor@123":
        loginWindow.destroy()
        DoctorWindow()
    else:
        text = tk.Text(loginWindow, height=1, width=30)
        text.grid(row=1, columnspan=2, sticky=tk.E+tk.W)
        text.insert(tk.END,'Invalid User Name or Password')
        

def ReceptionWindow():
    global receptionWindow, PatientNameEntry, ContactNumberEntry, AgeEntry, AddressEntry, genderEntry
    
    receptionWindow = tk.Toplevel()
    LoginWindow_2 = partial(LoginWindow, 2)
    LogoutButton = tk.Button(receptionWindow, text='Logout', command=LoginWindow_2)
    LogoutButton.grid(row=2, column=5)

    ExitButton = tk.Button(receptionWindow, text='Exit', command=ExitApplication)
    ExitButton.grid(row=2, column=7)
    
    tk.Label(receptionWindow, text='Patient Name').grid(row=3)
    PatientName = tk.StringVar()
    PatientNameEntry = tk.Entry(receptionWindow, textvariable=PatientName)
    PatientNameEntry.grid(row=3,column=1, columnspan=6, sticky=tk.E+tk.W)

    tk.Label(receptionWindow, text='Gender').grid(row=4)
    genderEntry = tk.StringVar()
    genderEntry.set('1')
    tk.Radiobutton(receptionWindow, text='Male', variable=genderEntry, value='1').grid(row=4, column=1, sticky=tk.W)
    tk.Radiobutton(receptionWindow, text='Female', variable=genderEntry, value='2').grid(row=4, column=3, sticky=tk.W)
    tk.Radiobutton(receptionWindow, text='Other', variable=genderEntry, value='3').grid(row=4, column=5, sticky=tk.W)

    tk.Label(receptionWindow, text='Contact Number').grid(row=5)
    ContactNumber = tk.StringVar()
    ContactNumberEntry = tk.Entry(receptionWindow, textvariable=ContactNumber)
    ContactNumberEntry.grid(row=5, column=1, columnspan=6, sticky=tk.E+tk.W)

    tk.Label(receptionWindow, text='Age').grid(row=6)
    Age = tk.StringVar()
    AgeEntry = tk.Entry(receptionWindow, textvariable=Age)
    AgeEntry.grid(row=6, column=1)

    tk.Label(receptionWindow, text='Address').grid(row=7)
    Address = tk.StringVar()
    AddressEntry = tk.Entry(receptionWindow, textvariable=Address)
    AddressEntry.grid(row=7, column=1, columnspan=6, sticky=tk.E+tk.W)

    clearButton = tk.Button(receptionWindow, text='Cancel', command=clearScreen)
    clearButton.grid(row=8, column=3)

    SaveButton = tk.Button(receptionWindow, text='Save and Next', command=PatientDetail)
    SaveButton.grid(row=8, column=5)
    
    receptionWindow.protocol("WM_DELETE_WINDOW", mainWindow.destroy)
    receptionWindow.mainloop()


def DoctorWindow():
    global doctorWindow

    doctorWindow = tk.Toplevel()
    LoginWindow_3 = partial(LoginWindow, 3)
    LogoutButton = tk.Button(doctorWindow, text='Logout', command=LoginWindow_3)
    LogoutButton.grid(row=2, column=5)

    ExitButton = tk.Button(doctorWindow, text='Exit', command=ExitApplication)
    ExitButton.grid(row=2, column=7)
    doctorWindow.protocol("WM_DELETE_WINDOW", mainWindow.destroy)

    doctorWindow.mainloop()
    

def ExitApplication():
    PD = open('Patient_Details_File','r')
    Details = PD.readlines()
    PD.close()
    
    connection = sqlite3.connect("Patient_Details_DataBase.db") 
      # cursor  
    crsr = connection.cursor() 
    # SQL command to create a table in the database 
    sql_command = """CREATE TABLE IF NOT EXISTS Patient_Detail (    
    Patient_Name VARCHAR(20),
    gender CHAR(1),
    Age VARCHAR(3), 
    Contact_number INTEGER PRIMARY KEY,
    Address VARCHAR(100));"""
  
    # execute the statement 
    crsr.execute(sql_command)
    #put data in data base
    for Detail in Details:
        Detail = Detail.split('\n')
        Detail = Detail[0].split('\t')
        data = (Detail[0], Detail[1][0], Detail[2], int(Detail[3]), Detail[4])
        sql_command = """INSERT INTO Patient_Detail VALUES (?, ?, ?, ?, ?);"""
        crsr.execute(sql_command, data)
        
    #read from Patient_Details_DataBase.db
    '''connection.commit()
    crsr.execute("SELECT * FROM Patient_Detail")  
    ans = crsr.fetchall()  
    print(ans)'''
    connection.close()

    mainWindow.destroy()


def clearScreen():
    global receptionWindow
    receptionWindow.destroy()
    ReceptionWindow()


def PatientDetail():
    global PatientNameEntry, ContactNumberEntry, AgeEntry, AddressEntry, genderEntry
    global Name, Number, age, address, receptionWindow, gender
    
    Name = PatientNameEntry.get()
    Number = ContactNumberEntry.get()
    age = AgeEntry.get()
    address = AddressEntry.get()
    gender = genderEntry.get()

    VerifyDetails()

    
def VerifyDetails():
    global Name, Number, age, address, receptionWindow, gender
    NameEntered = Name 
    ContactNumberEntered = Number
    ageEntered = age
    AddressEntered = address
    genderEntered = gender
    if (ContactNumberEntered.strip().isnumeric()) and (len(ContactNumberEntered.strip()) == 10) and (ageEntered.strip().isnumeric()) and (AddressEntered.replace(' ','').isalnum()) and (NameEntered.replace(' ','').isalpha()) and (int(genderEntered) != 0):
        receptionWindow.destroy()
        SaveInTextFile()
    else:
        text = tk.Text(receptionWindow, height=1, width=30)
        text.grid(row=1, columnspan=2, sticky=tk.E+tk.W)
        text.insert(tk.END,'Invalid Details!!!')


def SaveInTextFile():
    global Name, Number, age, address, receptionWindow, gender
    
    if(gender == '1'):
        gender = 'Male'
    elif(gender == '2'):
        gender = 'Female'
    else:
        gender = 'Other'
    
    info = str(Name) + '\t' + str(gender) + '\t' + str(age) + '\t' + str(Number) + '\t' + str(address) + '\n'
    #print(detail)
    PD = open('Patient_Details_File','a')
    PD.write(info)
    PD.close()
    ReceptionWindow()

    
if __name__ == "__main__":
    #create a GUI
    mainWindow = tk.Tk()
    LoginWindow(1)  
    mainWindow.mainloop()
