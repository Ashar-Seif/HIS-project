import mysql.connector
from flask import Flask, redirect, url_for, request,render_template

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="MyPythonDatabase"
)
mycursor = mydb.cursor()
app = Flask(__name__)

@app.route('/')
def hello_name():
   return render_template('index.html')

@app.route('/adddoctor',methods = ['POST', 'GET'])
def adddoctor():
   if request.method == 'POST': ##check if there is post data
      name = request.form['name']
      department = request.form['department']
      id = request.form['id']
      print(name,department,id)
      sql = "INSERT INTO Doctors (name,department, id) VALUES (%s, %s, %s)"
      val = (name,department,id)
      mycursor.execute(sql, val)
      mydb.commit() 
      return render_template('index.html')
   else:
      return render_template('adddoctor.html')

@app.route('/viewdoctor',methods = ['POST', 'GET'])
def viewdoctor():
   if request.method == 'POST':
      return render_template('index.html')
   else:
      mycursor.execute("SELECT * FROM Doctors")
      row_headers=[x[0] for x in mycursor.description] #this will extract row headers
      myresult = mycursor.fetchall()
      data={
         'message':"data retrieved",
         'rec':myresult,
         'header':row_headers
      }
      return render_template('viewdoctor.html',data=data)

if __name__ == '__main__':
   app.run()
  