import random
import User_system
import pandas as pd
import openpyxl
from time import sleep
note = pd.read_excel(User_system.cur_path + "/cash_note.xlsx" , engine="openpyxl")
account_balance = None
option_note = note["option note"].tolist()
bank_note = note["bank note"].tolist()
Username = None
def Deposit():
    global account_balance
    Loop = True
    while Loop:
        result =input("Are you win or lose ?? w/l:")
        if result == "w":
            print("you are so good bro. There your money \n +2000 in the bank. \n")
            account_balance += 2000
        else:
            print("Bye~ 1000 Dollar. \n -1000 in the bank. \n")
            account_balance -= 1000
        while True:
            play = input("play again? y/n:")
            if play == "y":
                break
            elif play == "n":
                Loop = False
                break
            else:
                print("Enter only y or n please.")
                pass


def Bank_List():
    for A,B in zip(bank_note,option_note):
        print(f"remaining {A} lefts of {B} banknote")

 #withdraw       
def Withdraw_system(amount):
    global account_balance,bank_note,Cash
    amount_keeper = 0
    nonote_count = 0
    cannot_draw_count = 0 
    for i in range(len(option_note)):
        if sum(bank_note) != 0:
            if amount <= account_balance :
                if amount >= option_note[i]:
                    if bank_note[i] > 0:
                        for i in range(len(bank_note)):
                            while amount >= option_note[i] and bank_note[i] > 0 :  
                                amount -= option_note[i]  
                                bank_note[i] -= 1
                                amount_keeper += option_note[i]
                        account_balance -= amount_keeper
                        Cash += amount_keeper
                        amount_keeper = 0
                        note["bank note"] = bank_note
                        note.to_excel(User_system.cur_path + "/cash_note.xlsx" , index=False, engine="openpyxl")
                        return "Successful"
                    else:
                        nonote_count +=1
                else:
                    cannot_draw_count += 1
                    pass
            else:
                return "not enough"
        else:
            return "no note in atm"        
    if nonote_count == 5:
        return "out of scale of banknote"
    elif nonote_count + cannot_draw_count == 5:  
        return "no note for withdraw"

def withdraw(IDUSER):
  global Cash,account_balance,ChangeTrue
  data = pd.read_excel(User_system.cur_path + "/atmdata.xlsx" , engine="openpyxl")
  user = User_system.ATM_User_system(User_system.cur_path + "/atmdata.xlsx")
  account_balance = data.loc[data["ID"] == IDUSER ,"Balance"].item()
  Cash = data.loc[data["ID"] == IDUSER ,"Cash"].item()
  while True:
      while True:
          try:
              ChangeTrue = True
              user.CheckBalance(User_system.cur_path + "/atmdata.xlsx",IDUSER)
              amountEnter = input("\nPlease Enter your amount to withdraw \n(Enter 'deposit' for deposit)\n(Enter 'leave' for leave)\n(Enter 'Change' for Change your Password/Pin)\n:")
              if amountEnter.lower() == "deposit":
                  withdraw = "deposit"
                  break
              elif amountEnter.lower() == "leave":
                  withdraw = "leave"
                  break
              elif amountEnter.lower() == "change":
                  withdraw = "change"
                  break
              else:
                  withdraw = Withdraw_system(int(amountEnter))
                  if withdraw == "not enough":
                      print("\nYou Enter Over price your account balance. Please Enter again or deposit!")
                      pass
                  else:
                      break
          except ValueError:
              print("please Enter number.")
      if withdraw == "Successful":
          print((f"Successful Withdraw !. Your account balance is:{account_balance}\n"))
          print(f"Your cash is {Cash}")
          Bank_List()
          again = input("Do you want to withdraw again? y/n:").lower()
          if again == "y":
              data.loc[data["ID"] == IDUSER ,"Balance"] = account_balance
              data.loc[data["ID"] == IDUSER ,"Cash"] = Cash
              data.to_excel(User_system.cur_path + "/atmdata.xlsx" ,index=False, engine="openpyxl") 
              pass   
          else:
              print("saving." ,end="\r")
              sleep(1)
              print("saving. . " ,end="\r")
              sleep(1)
              print("saving. . ." ,end="\r")
              sleep(1)
              data.loc[data["ID"] == IDUSER ,"Balance"] = account_balance
              data.loc[data["ID"] == IDUSER ,"Cash"] = Cash
              data.to_excel(User_system.cur_path + "/atmdata.xlsx" ,index=False, engine="openpyxl") 
              # user.logout()
              break
      else:
          if withdraw == "out of scale of banknote":
              print("\nThe amount is not relevant with banknotes. \n Please Enter again")
              pass
          elif withdraw == "not enough":
              Game_time = (input("Play game with coder and gain 2000 if you win and if you lose loss 1000 ok|no:"))
              if Game_time in ["ok","k","yes","y"]:
                  Deposit()
                  data.loc[data["ID"] == IDUSER ,"Balance"] = account_balance
                  data.to_excel(User_system.cur_path + "/atmdata.xlsx" ,index=False, engine="openpyxl") 
                  pass
              
              else:
                  print("bye dude.")
                  # user.logout()
                  break
          elif withdraw == "deposit":
              print("\nSeem You want to against the god. ok! come on!")
              Game_time = (input("Play game with coder and gain 2000 if you win and if you lose loss 1000 ok|no:"))
              if Game_time in ["ok","k","yes","y"]:
                  Deposit()
                  data.loc[data["ID"] == IDUSER ,"Balance"] = account_balance
                  data.to_excel(User_system.cur_path + "/atmdata.xlsx" ,index=False, engine="openpyxl") 
                  pass
              else:
                  print("bye dude.")
                  # user.logout()
                  break
          elif withdraw == "no note in atm":
              print("\nThere's no more note in ATM")
              break
          elif withdraw == "no note for withdraw":
              print("\nDon't have note for your amount. \nPlease try again later.\n")
              pass
          elif withdraw == "leave":
              print("Have a nice day :)")
              break
          elif withdraw == "change":
              while ChangeTrue:
                  passpinask = input("Change Pass or Pin? \n(Pass/Pin):")
                  if passpinask.lower() == "pass":
                      newpass = input("Please Enter your new password:")
                      data.loc[data["ID"] == IDUSER,"Password"] = newpass
                      data["Password"] = data["Password"].astype(str)
                      data.to_excel(User_system.cur_path + "/atmdata.xlsx" ,index=False, engine="openpyxl")
                      break
                  elif passpinask.lower() == "pin":
                      newpin = input("Please Enter your new pin(4 numbers):")
                      while True:
                          try:
                              int(newpin)
                              if len(str(newpin)) == 4:
                                  data.loc[data["ID"] == IDUSER,"Pin"] = newpin
                                  data["Pin"] = data["Pin"].astype(str)
                                  data.to_excel(User_system.cur_path + "/atmdata.xlsx" ,index=False, engine="openpyxl")
                                  ChangeTrue = False
                                  break
                              else:
                                  print("Please enter only 4 numbers.")
                                  newpin = (input("Please Enter your new pin(4 numbers):"))
                          except ValueError:
                              print("Pin Is allow only number. Please set number as pin.")
                              newpin = (input("Please Enter your new pin(4 numbers):"))
                  else:
                      print("Please Enter Pin or Pass")
          else:
              print("\nwhat the heck bro. How can you be able to be here??")
              break
def Login():
    global Cash,account_balance,Username
    BreakLoopanywhereyouwant = True
    attemps = 4
    
    while BreakLoopanywhereyouwant:# While ทณู
        while True:
            try:
                data = pd.read_excel(User_system.cur_path + "/atmdata.xlsx" , engine="openpyxl")
                user = User_system.ATM_User_system(User_system.cur_path + "/atmdata.xlsx")
                Login_input = input("\nLogin Page\nEnter your (leave space and Enter for register/leave)(username/password or pin):")
                if Login_input in "                                 ":
                    Speicific = input("\nEnter leave to leave\nEnter Register to register\n:")
                    if Speicific.lower() == "register":
                        Login =  "Failid"
                        break
                    elif Speicific.lower() == "leave":
                        Login = None
                        break
                else:
                    split_login = Login_input.split(" ",1)
                    Login = user.login(split_login[0],split_login[1])
                    if Login == "Failid":
                        print("ID not found. Please register.")
                        pass
                    else:
                        break
            except IndexError:
                print("please enter username and password both and split with a space")
        while attemps != 0:
            if Login == "Pass":
                Username = split_login[0]
                return "pass"
                BreakLoopanywhereyouwant = False
                break
            else:
                if Login == "Failpass":
                    print(f"Password was wrong. Please check carefully before enter. \n you have {attemps} times left. please Enter again")
                    attemps -=1
                    password_input = input("Enter your password / Pin:")
                    Login = user.login(split_login[0],password_input)
                    if attemps == 0:
                        data.loc[data["ID"] == split_login[0],"Locked"] = 1
                        data.to_excel("atmdata.xlsx",index=False,engine="openpyxl")
                        print("Your account has been locked. please notify directly to the bank.")
                        return "Faillogin"
                        BreakLoopanywhereyouwant = False
                        break
                else:
                    if Login ==  "Failid":
                        print("Connecting to register." ,end="\r")
                        sleep(1)
                        print("Connecting to register. . " ,end="\r")
                        sleep(1)
                        print("Connecting to register. . ." ,end="\r")
                        sleep(1)
                        User_signin_NAME = input("\nSignin Page\nPlease Enter your (Firstname/Lastname):") 
                        User_signin_NAME_spilt = User_signin_NAME.split (" ",1)
                        User_signin_ID = input("Please enter your Username:") 
                        User_signin_PASSWORD = input("Please enter your Password:") 
                        User_signin_PIN = input("Please Enter your pin(4 numbers):") 
                        while True:
                            try:
                                user.register(User_signin_NAME_spilt,User_signin_ID,User_signin_PASSWORD,User_signin_PIN)   
                                break
                            except IndexError:
                                print("please enter Firstname/Lastname both and split with a space")
                                User_signin_NAME2 = input("Please Enter your (Firstname/Lastname):") 
                                User_signin_NAME_spilt = User_signin_NAME2.split (" ",1)
                        break
                    elif Login ==  "Faillocked":
                        print("Your account has been locked. please notify directly to the bank.")
                        return "Faillogin"
                        BreakLoopanywhereyouwant = False
                        break
                    else:
                        return "Faillogin"
                        BreakLoopanywhereyouwant = False
                        break

                   
def main():
  global Username
  isLogin = Login()                   
  if isLogin == "pass":
    withdraw(Username)
    Username = None
if __name__ == "__main__":
    main()

