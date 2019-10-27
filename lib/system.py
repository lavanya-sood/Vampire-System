#comments are examples of what we should put in this file
#from lib.products import Products

import json
import os
import ast
import operator
import datetime
from operator import itemgetter
from collections import Counter

currDir = os.getcwd()
#productsDir = currDir + "/lib/textfiles/products.json"

now = datetime.datetime.now()

class System:
    #product_data = {}
    #request_data = {}
    #user_data = {}

    def __init__(self):
        pass


    #def get_user(self, name):
      #  with open(user_dataDir, 'r') as f:
      #      datastore = json.load(f)
      #  for element in datastore["user"]:
      #      if element["username"] == name:
      #          return element



    #def create_user(self,username,email, password,city):
     #   data = {
     #       "username":username,
     #       "email": email,
     #       "password": password,
     #       "login": "True",
     #       "city":city,
     #       "aveRating": "0",
     #       "review": [],
     #       "trip": []

      #  }
      #  with open(user_dataDir, 'r') as f:
      #      datastore = json.load(f)
      #  datastore["user"].append(data)
      #  with open(user_dataDir, "w") as file:
      #      json.dump(datastore, file,indent= 4)
      #  return ""
