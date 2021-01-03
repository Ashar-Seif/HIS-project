# Import MySQL Module
import mysql.connector
from flask import Flask, redirect, url_for, request,render_template

# Create Database And Connect
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="Hemodialysis_Department"
)
mycursor = mydb.cursor()
app = Flask(__name__)
# Checking that database is readable
"""
 mycursor.execute("SHOW DATABASES")
 for x in mycursor:
  print(x)
  """
# Showing tables 
"""
 mycursor.execute("SHOW TABLES")
for x in mycursor:
  print(x) 
  """
#Selecting From table Doctor 
"""
mycursor.execute("SELECT * FROM Doctor")
myresult = mycursor.fetchone()
print(myresult)
"""

#Selecting From table nurses
mycursor.execute("SELECT * FROM nurses")
myresult = mycursor.fetchone()
print(myresult)


#Selecting From table patient
"""
mycursor.execute("SELECT * FROM patient")
myresult = mycursor.fetchone()
print(myresult)
"""

#Selecting From table Sessions
"""
mycursor.execute("SELECT * FROM Sessions")
myresult = mycursor.fetchone()
print(myresult)
"""