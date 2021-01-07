import mysql.connector
from flask import Flask, render_template,request

mydb = mysql.connector.connect(

  host="localhost",
  user="root",
  passwd="mysql",
  database="Hemodialysis"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS Doctors(Dcode VARCHAR (255) NOT NULL PRIMARY KEY,Fname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),phone INT(14),mail VARCHAR(255) UNIQUE,Birth_date INT(14),Doctor_ID INT(28) UNIQUE,syndicate_number INT (28) UNIQUE,salary INT(11),gender VARCHAR(255),address text,jop_rank VARCHAR(255),image LONGBLOB)")
mycursor.execute("CREATE TABLE IF NOT EXISTS nurses (Ncode VARCHAR (255) NOT NULL PRIMARY KEY,Fname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),phone INT(14),mail VARCHAR(255)UNIQUE,Birth_Date INT(11),Nurse_ID INT(28)UNIQUE,syndicate_number INT (28) UNIQUE,salary INT(11),gender VARCHAR(255),address text,image LONGBLOB )")
mycursor.execute("CREATE TABLE IF NOT EXISTS patients(Pcode VARCHAR (255) NOT NULL PRIMARY KEY,Fname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),Numofsessions int(11),Daysofsessions text,Patient_ID INT(28)UNIQUE,phone INT(14),mail VARCHAR(255)UNIQUE,age INT(11),gender VARCHAR(255),adress text,Dry_weight INT (11),Described_drugs text,SupD VARCHAR (255),FOREIGN KEY (SupD) REFERENCES doctors(Dcode))")
mycursor.execute("CREATE TABLE IF NOT EXISTS sessions (Scode VARCHAR (255) NOT NULL PRIMARY KEY,Date INT (11),used_device VARCHAR(255),price INT(11),record_by VARCHAR(255),after_weight INT (11),duration INT(11),taken_drugs text,complications text, dealing_with_complications text,comments text,P_code VARCHAR (255),D_code VARCHAR (255),N_code VARCHAR (255) ,FOREIGN KEY(P_code) REFERENCES patients(Pcode),FOREIGN KEY(D_code) REFERENCES doctors(Dcode),FOREIGN KEY(N_code) REFERENCES nurses(Ncode))")
mycursor.execute("CREATE TABLE IF NOT EXISTS contact (name VARCHAR(255),email VARCHAR(255),subject VARCHAR(255),message text)")

app = Flask(__name__,template_folder='template')

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/adddoctor')
def adddoctor():
   return render_template('adddoctor.html')

@app.route('/viewdoctor')
def viewdoctor():
   return render_template('viewdoctor.html')

@app.route('/addpatient')
def addpatient():
   return render_template('addpatient.html')

@app.route('/viewpatient')
@app.route("/upload",methods=["post"])
def viewpatient():
   return render_template('viewpatient.html')
def upload():
    file=request.files["inputfile"]
    return file.filename

@app.route('/addnurse')
def addnurse():
   return render_template('addnurse.html')

@app.route('/viewnurse')
def viewnurse():
   return render_template('viewnurse.html')

@app.route('/addsession')
def addsession():
   return render_template('addsession.html')

@app.route('/viewsession')
def viewsession():
   return render_template('viewsession.html')

if __name__ == '__main__':
   app.run()

   