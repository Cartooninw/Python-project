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
items_list = list(items.keys())
items_price = list(items.values())
shipping_charge = 0 
basket = {}
items_amount = []
# SHOPUSER = User_system.shop_User_system(User_system.cur_path + "/users.xlsx")
# ATMUSER = User_system.ATM_User_system(User_system.cur_path + "/atmdata.xlsx") 
# ATMDATA = pd.read_excel(User_system.cur_path + "/atmdata.xlsx",engine="openpyxl")
SHOPDATA = pd.read_excel(User_system.cur_path + "/users.xlsx",engine="openpyxl")

balance = 15000
def register_membership(User,Balance):
  while True:
      ASKFORMEMBER = input("Do you want to apply membership? (y/n):")
      if ASKFORMEMBER == "y":
          print("work")
          SHOPDATA.loc[SHOPDATA["username"]==User  ,  "member"] = 1
          SHOPDATA.to_excel(User_system.cur_path + "/users.xlsx",index=False,engine="openpyxl")
          print(Balance)
          Balance -= 2000
          print(Balance)

          break
      elif ASKFORMEMBER == "n":
          return "no"
      else:
          print("Please Enter only y or n")
register_membership("E",balance)
print(balance)
balance -= 200
print(balance)