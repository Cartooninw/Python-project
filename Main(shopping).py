import ATM
import random
import User_system
import openpyxl
import pandas as pd
import string
import os
#Variable Declaration
member = ["yes","no"]
yes_options = "yes"
items = {"shirt":5,"shoes":30,"foods":2,"monkey paw":100,"crucifix":20,"curse items":340,"Music Box":10,"Another monkey paw":100,"And monkey paw":100,"water":1,"fruits":1}
items_list = list(key.lower() for key in items.keys())
items_price = list(items.values())
shipping_charge = 0 
basket = {}
items_amount = []
# SHOPUSER = User_system.shop_User_system(User_system.cur_path + "/users.xlsx")
# ATMUSER = User_system.ATM_User_system(User_system.cur_path + "/atmdata.xlsx") 
# ATMDATA = pd.read_excel(User_system.cur_path + "/atmdata.xlsx",engine="openpyxl")
SHOPDATA = pd.read_excel(User_system.cur_path + "/users.xlsx",engine="openpyxl")
def printLists():
    Name1,Name2 = "Items","Price"
    print("="*45)
    print(f"{Name1:<30} {Name2:>10}")
    print("="*45)
    for item,price in list(items.items()):
        print(f"{item:<30} {price:>10}")
    print("="*45+"\n"+"="*45)
    
def register_membership(User,Balance):
    while True:
        ASKFORMEMBER = input("Do you want to apply membership? (y/n):")
        if ASKFORMEMBER == "y":
            SHOPDATA.loc[SHOPDATA["username"]==User  ,  "member"] = 1
            SHOPDATA.to_excel(User_system.cur_path + "/users.xlsx",index=False,engine="openpyxl")
            Balance -= 2000
            return Balance
            break
        elif ASKFORMEMBER == "n":
            return "no"
        else:
            print("Please Enter only y or n")
#Check membershihp

#distance calculator
def distance_calculator_system(distance):
    global shipping_charge
    if distance <= 20.00:
        if 0.01 <=distance<=5.00 :
            shipping_charge = 20
        elif 5.01 <=distance<=10.00 :
            shipping_charge = 40
        elif 10.01 <=distance<=15.00 :
            shipping_charge = 70
        elif 15.01 <=distance<=20.00 :
            shipping_charge = 100
    else:
        return "cancel"

#add to basket
def shopping_system(select,count):
    global basket,items_amount
    if select.lower() in items_list:
        if select.lower() in basket:
            basket[select.lower()] += count
        else:
            basket[select.lower()] = count


#put all items in basket compare with prices in item_price and add on item_amount prepare for price all together
def shopping_calculator(amount,price):
    global items_list
    for lists_sequence in range(len(items_list)):
        itemName = items_list[lists_sequence]
        if itemName in basket:
            amount.append(price[lists_sequence] * basket[itemName])



#main        
def main():
    
    Main1,Main2,Logined = True,True,True
    while Main1:
        while True:
            try:
                Main2,Logined = True,True
                SHOPUSER = User_system.shop_User_system(User_system.cur_path + "/users.xlsx")
                SHOPDATA = pd.read_excel(User_system.cur_path + "/users.xlsx",engine="openpyxl")
                #random distance because it's tester
                distance = random.uniform(0.00 , 20.00)
                Login_input = input("Enter Your Username/Password (Leave a space for register/leave):")
                
                if Login_input in "                                 ":
                    Speicific = input("\nEnter leave to leave\nEnter Register to register\n:")
                    if Speicific.lower() == "register":
                        Login_Detector =  "register"
                        break
                    elif Speicific.lower() == "leave":
                        Login_Detector = None
                        break
                else:
                    login = Login_input.split(" ")
                    Login_Detector = SHOPUSER.login(login[0],login[1])
                    if Login_Detector == "register":
                        print("username not found. Please register.")
                        pass
                    else:
                        break
            except IndexError:
                print("please enter username and password both and split with a space")
        while Main2: 
            #main input
            if Login_Detector == "pass":
                
                select_recive = input("pick your items(Enter 'list' for see the menu):")
                if select_recive.lower() == "list":
                    printLists()
                elif select_recive.lower() in items_list:
                    while True:
                        try:
                            item_count = int(input("How many you want?:"))
                            break
                        except ValueError:
                            print("Please Enter number.") 
                    #add on basket system
                    shopping_system(select_recive,item_count)
                    print(basket)
                    #ask if want to stop
                    stop_shopping = input("Need More? y/n:").lower()

                    #early analyse 
                    #declare shipfee for check if can delevery
                    shipfee = distance_calculator_system(distance)

                    if stop_shopping not in yes_options :
                        shopping_calculator(items_amount,items_price)
                        print(items_amount)
                        if shipfee != "cancel":
                            # summary and calculate all price 
                            while Logined:
                                membership = SHOPDATA.loc[SHOPDATA["username"]==login[0],"member"].item()
                                ATM.Login()
                                ATMDATA = pd.read_excel(User_system.cur_path + "/atmdata.xlsx",engine="openpyxl")
                                ATM_USER = ATM.Username
                                balance = ATMDATA.loc[ATMDATA["ID"]==ATM_USER,"Balance"].item()
                                
                                if membership == True:
                                    print("working")
                                    items_amount.append(-(0.2*sum(items_amount)))
                                    print(items_amount)
                                else:
                                    if balance >= 2000 :
                                        balance = register_membership(login[0],balance)
                                        ATMDATA.loc[ATMDATA["ID"]==ATM_USER,"Balance"] = balance
                                        ATMDATA.to_excel(User_system.cur_path + "/atmdata.xlsx",index=False,engine="openpyxl")
                                        items_amount.append(0)
                                    else:
                                        print("You're broke shit")
                                        items_amount.append(0)
                                        pass
                                while True:
                                    ATMDATA = pd.read_excel(User_system.cur_path + "/atmdata.xlsx",engine="openpyxl")
                                    Cash = ATMDATA.loc[ATMDATA["ID"] == ATM_USER,"Cash"].item()
                                    Total = sum(items_amount) 
                                    print(f"Your items price is {Total - items_amount[-1]}\nYour discount is {-items_amount[-1]}\ndistance is {distance:.2f}\nYour shipping rate is {shipping_charge}\nTotal is:{Total + shipping_charge}")
                                    if Cash >= (Total+shipping_charge):
                                        print(f"ordered successful")
                                        Cash -= Total
                                        ATMDATA.loc[ATMDATA["ID"] == ATM_USER ,"Cash"] = Cash
                                        ATMDATA.to_excel(User_system.cur_path + "/atmdata.xlsx" ,index=False, engine="openpyxl")
                                        ATM.Username = None
                                        items_amount.clear()
                                        basket.clear()
                                        Main2 = False
                                        Logined = False
                                        break
                                    else:
                                        print(f"Your cash isn't enough.\nYou have {Cash} available \nPlease add your cash.")
                                        #Active ATM increase crash
                                        ADDCASH = input("Do want to add your cash? y/n:")
                                        if ADDCASH == "y":

                                            ATM.withdraw(ATM_USER)
                                        else:
                                            Main2 = False
                                            Logined = False
                                            break
                        else:
                            print("Distance is so far, ordered cancelled")
                            break
                else:
                    print("Please Enter an item which in the menu.")
            elif Login_Detector == "fail":
                Password = input("Enter your password correctly:")
                Login_Detector = SHOPUSER.login(login[0],Password)
            elif Login_Detector == "login":
                break
            elif Login_Detector == "register":
                Register_username = input("Enter your Username:")
                Register_password = input("Enter your password:")
                SHOPUSER.register(Register_username,Register_password)
                break
if __name__ == "__main__":
    main()

