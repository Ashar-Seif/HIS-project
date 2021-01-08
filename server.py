import mysql.connector
from flask import Flask, render_template,request

mydb = mysql.connector.connect(

  host="localhost",
  user="root",
  passwd="mysql",
  database="Hemodialysis"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS Doctors(Dcode VARCHAR (255) PRIMARY KEY,Fname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),phone INT(14),mail VARCHAR(255) UNIQUE,Birth_date INT(14),Doctor_ID INT(28) UNIQUE,syndicate_number INT (28) UNIQUE,salary INT(11),gender VARCHAR(255),address text,jop_rank VARCHAR(255),image LONGBLOB)")
mycursor.execute("CREATE TABLE IF NOT EXISTS nurses (Ncode VARCHAR (255) NOT NULL PRIMARY KEY,Fname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),phone INT(14),mail VARCHAR(255)UNIQUE,Birth_Date INT(11),Nurse_ID INT(28)UNIQUE,syndicate_number INT (28) UNIQUE,salary INT(11),gender VARCHAR(255),address text,image LONGBLOB )")
mycursor.execute("CREATE TABLE IF NOT EXISTS patients(Pcode VARCHAR (255) NOT NULL PRIMARY KEY,Fname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),Numofsessions int(11),Daysofsessions text,Patient_ID INT(28)UNIQUE,phone INT(14),mail VARCHAR(255)UNIQUE,age INT(11),gender VARCHAR(255),adress text,Dry_weight INT (11),Described_drugs text,SupD VARCHAR (255),FOREIGN KEY (SupD) REFERENCES doctors(Dcode))")
mycursor.execute("CREATE TABLE IF NOT EXISTS sessions (Scode VARCHAR (255) NOT NULL PRIMARY KEY,Date INT (11),used_device VARCHAR(255),price INT(11),record_by VARCHAR(255),after_weight INT (11),duration INT(11),taken_drugs text,complications text, dealing_with_complications text,comments text,P_code VARCHAR (255),D_code VARCHAR (255),N_code VARCHAR (255) ,FOREIGN KEY(P_code) REFERENCES patients(Pcode),FOREIGN KEY(D_code) REFERENCES doctors(Dcode),FOREIGN KEY(N_code) REFERENCES nurses(Ncode))")
mycursor.execute("CREATE TABLE IF NOT EXISTS contact (name VARCHAR(255),email VARCHAR(255),subject VARCHAR(255),message text)")

app = Flask(__name__,template_folder='template')

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/adddoctor',methods =  ['POST', 'GET'])
def adddoctor():
    if request.method == 'POST': ##check if there is post data
      Dcode = request.form['Dcode']
      Fname = request.form['Fname']
      Mname = request.form['Mname']
      Lname = request.form['Lname']
      phone = request.form['Phone']
      mail = request.form['mail']
      BD = request.form['Birth_date']
      Doctor_ID= request.form['Doctor_ID']
      Salary= request.form['Salary']
      gender= request.form['gender']
      Syndicate_number= request.form['Syndicate_number']
      address= request.form['address']
      Job_rank= request.form['Job_rank']
      sql = "INSERT INTO doctors ( Dcode,Fname,Mname,Lname,phone,mail,Birth_date,Doctor_ID,Syndicate_number,salary,gender,address,jop_rank) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s, %s,%s)"
      val = (Dcode,Fname,Mname,Lname,phone,mail,BD,Doctor_ID,Syndicate_number,Salary,gender,address,Job_rank)
      mycursor.execute(sql, val)
      mydb.commit() 
      return render_template('index.html')
    else:
      return render_template('adddoctor.html')

@app.route('/viewdoctor')
def viewdoctor():
   mycursor.execute("SELECT * FROM Doctors")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   return render_template('viewdoctor.html',DoctorsData = myresult)

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

@app.route('/addsession',methods =  ['POST', 'GET'])
def addsession(): 
   if request.method == 'POST': ##check if there is post data
      Scode=request.form['Scode']
      Date= request.form['Date']
      used_device = request.form['used_device']
      Price = request.form['Price']
      record_by = request.form['record_by']
      after_weight = request.form['after_weight']
      duration= request.form['duration']
      taken_drugs= request.form['taken_drugs']
      complications= request.form['complications']
      dealing_with_complications= request.form['dealing_with_complications']
      comments= request.form['comments']
      sql = "INSERT INTO sessions (Scode,Date,used_device,price,record_by,after_weight,duration,taken_drugs,complications,dealing_with_complications,comments) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)"
      val = (Scode,Date,used_device,Price,record_by,after_weight,duration,taken_drugs,complications,dealing_with_complications,comments)
      mycursor.execute(sql, val)
      mydb.commit() 
      return render_template('index.html')
   else:
     return render_template('addsession.html')

@app.route('/viewsession')
def viewsession():
   return render_template('viewsession.html')

if __name__ == '__main__':
   #app.run()
   app.run(debug=True)
   