import os 
import pandas as pd
import openpyxl
import random as rd
import string
import time
import traceback
#ทดลองทุกอย่างที่มี def หากไม่รู้วิธีใช้ถามคนเขียนโค้ด



#Declare variables
cur_path = os.getcwd()
def delay(second):
   time.sleep(second)


#main function of UserSystem. Create for all of user system.

class Fund_User:

  #Declare variables
  def __init__(self,Data):
    self.Data = Data

  #Load data expect errors
  def load_file(self):
    try:
      data =  pd.read_excel(self.Data, engine="openpyxl")
      return data
    except FileNotFoundError:
      print("File Not Found. Please Create/Check your file.")




#Shop User System
class shop_User_system:
  #Declare variables
  def __init__(self,data):
    self.data = data
    self.user = Fund_User(self.data)
    self.load = self.user.load_file()
    self.using = None
  #register by recive input and save to file.  
  def register(self,username,password):
      data = self.load.to_dict(orient="list")
      #if username has been used warning if not contain all data and member 0 meaning False 
      while True:
        if username in self.load["username"].tolist():
          print("\nUsername has been used. Please Enter again!\n")
          username = input("Enter Your Username:")
        else:
          data["username"].append(username)
          data["password"].append(str(password))
          data["member"].append(0)
          data = pd.DataFrame(data)
          data.to_excel(self.data,index=False,engine="openpyxl")
          break

  #login function      
  def login(self,username,password):
    load = self.load
    #check if username is exist 
    if username not in load["username"].tolist():
      return "register"
    else:
      #checking password 
      passwordCheck = load.loc[load["username"] == username,"password"]
      if password  == str(passwordCheck.item()):
        print("Connecting")
        time.sleep(3)
        self.using = username
        print("Enjoy! :)")
        return "pass"
      else:
        #check password if password was a space
        if password in "                     ":
          pwc = input("Enter your password separated by (oldpass/newpass):")
          pwin = pwc.split(" ")
          #loop until oldpassword has been enter right password
          while True:
              #if it's be as i mentioned password save to excel
            if pwin[0] == str(passwordCheck.item()):
              load.loc[(load["username"] == username), "password"] = pwin[1]
              load.to_excel(self.data,index=False,engine="openpyxl")
              self.using = username
              return "pass"
              break
            else:
              print("Wrong Password!")
              pwc = input("Enter your password separated by (oldpass/newpass) back to login by a space:")
              pwin = pwc.split(" ") 
              #if it's a space back to login
              if pwc == " ":
                return "login"
        else:
          print("Wrong Password!")
          return "fail"
  #logout in order to not using others person account
  def logout(self):
    self.using = None
        
class ATM_User_system:

  #declare variables
  def __init__(self,data):
    self.data = data
    self.User = Fund_User(self.data)
    self.load = self.User.load_file()
    self.using = None
    
  #register function
  def register(self,realname,id,password,pin):
    Data = self.load
    while True:
      #check if name is been used
      if ((realname[0].lower() + realname[1].lower()) not in (Data["FirstName"] + Data["LastName"]).tolist() ):
        #check if ID have been used
        if (id not in Data["ID"].tolist()):
          #check if pin is number
          try:
            int(pin)
            #Last terms/check if pin is 4 numbers
            if len(str(pin)) == 4:
              new_user ={"FirstName":realname[0].lower(),"LastName":realname[1].lower(),"ID":id,"Password":str(password),"Pin":(pin),"Balance":0,"Locked":0,"Cash":0}
              user_dataframe = pd.DataFrame([new_user])
              Data = pd.concat([Data, user_dataframe],ignore_index=False)
              Data.to_excel(self.data,index=False,engine="openpyxl")
              break
            else:
                print("Please enter only 4 numbers.")
                pin = (input("Please Enter your pin(4 numbers):"))
          except ValueError:
            print("Pin Is allow only number. Please set number as pin.")
            pin = (input("Please Enter your pin(4 numbers):"))
        else:
          print("This ID have been used. Please enter ID again.")
          time.sleep(1)
          id = input("Please Enter your ID:")
      else:
        print("This Name have been used. Please change your Name.")
        time.sleep(1)
        inName = input("Please Enter your (Firstname/Lastname):")
        realname = inName.split(" ")
  def login(self,id,password):
    Data = self.load
    #check if id is exist
    if (id in Data["ID"].tolist()) :
      if (Data.loc[Data["ID"] == id , "Locked"].item() == 0):
      #check if password = pin or password
        if ((password == str(Data.loc[Data["ID"] == id,"Password"].item())) or (password == str(Data.loc[Data["ID"] == id,"Pin"].item()))) :
          print("Logging")
          time.sleep(3)
          self.using = id
          print("Pass!")
          return ("Pass")
        else:
          return ("Failpass")
      else:
        return("Faillocked")
    else:
        
        return ("Failid")
      
  #logout in order to not using others person account
  def logout(self):
    self.using = None
  #notice Blance in account
  def CheckBalance(self,load,username): 
    try:
      Check = Fund_User(load)
      self.load = Check.load_file() 
      self.balance = self.load.loc[self.load["ID"] == username,"Balance"].item()
      print(f"\nYou have {self.balance } Dollar in the bank.")
    except ValueError:
      print("Please Login before checking balance.")

