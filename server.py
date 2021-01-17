from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from google.oauth2 import service_account
import googleapiclient.discovery
#from pprint import pprint
import mysql.connector
from flask import Flask, redirect, url_for, render_template, request, session,send_file
from io import BytesIO
import re

mydb = mysql.connector.connect(

  host="localhost",
  user="root",
  passwd="mysql",
   database="Hemodialysis"
  
)
#Calendar 
'''
SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
SERVICE_ACCOUNT_FILE = 'service.json'
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#delegated_credentials = credentials.with_subject('ashar.zanqour99@eng-st.cu.edu.eg')
sqlAdmin= googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
GCAL = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
#Calendar '''

mycursor = mydb.cursor(buffered=True)
mycursor.execute("CREATE TABLE IF NOT EXISTS Doctors(Dcode VARCHAR (255)  NOT NULL PRIMARY KEY,password VARCHAR(255) UNIQUE NOT NULL , Dname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),phone INT(50),mail VARCHAR(255) UNIQUE,Birth_date Date,Doctor_ID INT(150) UNIQUE,syndicate_number INT (100) UNIQUE,salary INT(50),gender VARCHAR(255),address text,job_rank VARCHAR(255),access_level int DEFAULT 2,image LONGBLOB,calendarid VARCHAR (600) UNIQUE )")
mycursor.execute("CREATE TABLE IF NOT EXISTS nurses (Ncode VARCHAR (255) NOT NULL PRIMARY KEY,password VARCHAR(255) UNIQUE NOT NULL ,Nname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),phone INT(50),mail VARCHAR(255)UNIQUE,Birth_date Date,Nurse_ID INT(150)UNIQUE,syndicate_number INT (100) UNIQUE,salary INT(50),gender VARCHAR(255),address text,access_level int DEFAULT 3 )")
mycursor.execute("CREATE TABLE IF NOT EXISTS patients(Pcode VARCHAR (255) NOT NULL PRIMARY KEY,password VARCHAR(255) UNIQUE NOT NULL ,Pname VARCHAR(255),Mname VARCHAR(255),Lname VARCHAR(255),Numofsessions int(11),Daysofsessions text,Patient_ID INT(100)UNIQUE,phone INT(14),mail VARCHAR(255)UNIQUE,age INT(11),gender VARCHAR(255),address text,Dry_weight INT (11),Described_drugs text,scan LONGBLOB,scan_name VARCHAR (255),access_level int DEFAULT 4,SupD VARCHAR (255),FOREIGN KEY (SupD) REFERENCES doctors(Dcode))")
mycursor.execute("CREATE TABLE IF NOT EXISTS sessions (Scode VARCHAR (255) NOT NULL PRIMARY KEY,Date Date,used_device VARCHAR(255),price INT(11),record_by VARCHAR(255),after_weight INT (11),duration INT(11),taken_drugs text,complications text, dealing_with_complications text,comments text,P_code VARCHAR (255),D_code VARCHAR (255),N_code VARCHAR (255) ,FOREIGN KEY(P_code) REFERENCES patients(Pcode),FOREIGN KEY(D_code) REFERENCES doctors(Dcode),FOREIGN KEY(N_code) REFERENCES nurses(Ncode))")
mycursor.execute("CREATE TABLE IF NOT EXISTS contact (name VARCHAR(255),email VARCHAR(255),subject VARCHAR(255),message text)")
mycursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,fullname VARCHAR(255) NOT NULL,username VARCHAR(255) NOT NULL,password VARCHAR(255) UNIQUE NOT NULL ,email VARCHAR(255) UNIQUE NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS admins (admin_name VARCHAR(255) UNIQUE NOT NULL,password VARCHAR(255) DEFAULT 'team13')")
mycursor.execute('INSERT IGNORE INTO admins (admin_name) VALUES ("aya"), ("ashar") ,("alaa"), ("radwa"), ("walaa");')
mydb.commit()
app = Flask(__name__,template_folder='template')
app.secret_key = 'team13'

@app.route('/',methods =  ['POST', 'GET'])
def hello_name():
  mycursor = mydb.cursor()
  if request.method == "POST": 
    name = request.form['name']
    email = request.form['email']
    subject= request.form['subject']
    message= request.form['message']
    sql = "INSERT INTO contact (name,email,subject, message) VALUES (%s, %s, %s, %s)"
    val = (name,email,subject, message)
    mycursor.execute(sql, val)
    mydb.commit()  
    mycursor.close()
    return render_template("index.html")
  else:
    return render_template("index.html")   
# Start of view contact 
@app.route('/viewcontact')
def viewcontact():
   mycursor.execute("SELECT * FROM contact")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   return render_template('viewcontact.html',contactData = myresult)
#End of view contact 

def hello_name():
    # Check if user is loggedin
  
  if 'adminloggedin' in session:
 # User is loggedin show them the home page
    return render_template('index.html', admin=session['admin'])
  elif 'loggedin' in session:  
    return render_template('index.html', username=session['username'])
  elif 'dloggedin' in session:  
     return render_template('index.html', doctor=session['Dname'])        
  elif 'nloggedin' in session:  
     return render_template('index.html', nurse=session['Nname'])
  elif 'ploggedin' in session:  
    return render_template('index.html', patient=session['Pname'])                
  else:
    session['notloggedin']= True
    return render_template('index.html', notloggedin=session['notloggedin'])

# Start of delete contact 
@app.route('/deletecontact/<string:id>',methods=['GET','POST'])
def deletecontact(id):
   mycursor = mydb.cursor()
   mycursor.execute("DELETE FROM contact WHERE name= %s", [id])
   mydb.commit()
   mycursor.execute("SELECT * FROM contact")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   return render_template('viewcontact.html' ,contactData = myresult)
#End of delete contact 

#START OF ADD DOCTOR **** http://127.0.0.1:5000/adddoctor
#START OF Dashboard
@app.route('/dashboard')
def dashboard():
#Numberofdoctors
     mycursor.execute("SELECT * FROM doctors")
     myresult = mycursor.fetchall()
     Numberofdoctors=len(myresult)
#Numberofpatients
     mycursor.execute("SELECT * FROM patients")
     myresult = mycursor.fetchall()
     Numberofpatients=len(myresult)
#NumberofNurses
     mycursor.execute("SELECT * FROM nurses")
     myresult = mycursor.fetchall()
     Numberofnurses=len(myresult)
#Numberofvisitors
     mycursor.execute("SELECT * FROM accounts")
     myresult = mycursor.fetchall()
     Numberofvisitors=len(myresult)
#Sumofsalaries
     mycursor.execute("SELECT SUM(salary) FROM doctors")
     myresult = mycursor.fetchall()
     Sum= myresult
     Sumsalaryofdoctors=Sum[0][0]
     mycursor.execute("SELECT SUM(salary) FROM nurses")
     myresult = mycursor.fetchall()
     Sum= myresult
     Sumsalaryofnurses=Sum[0][0]
#Avgofsalaries
     mycursor.execute("SELECT AVG(salary) FROM doctors") 
     myresult = mycursor.fetchall()
     Sum= myresult
     AVGsalaryofdoctors=Sum[0][0]
     mycursor.execute("SELECT  AVG(salary) FROM nurses")
     row_headers=[x[0] for x in mycursor.description] 
     myresult = mycursor.fetchall()
     Sum= myresult
     AVGsalaryofnurses=Sum[0][0]
#Sumofprices
     mycursor.execute("SELECT SUM(price) FROM sessions")
     myresult = mycursor.fetchall()
     Sum= myresult
     Sumofprices=Sum[0][0]
#sessions
     mycursor.execute("SELECT Scode FROM sessions ")
     myresult = mycursor.fetchall()
     Numberofsessions=len(myresult)
     L1=[]
     L2=[]
     for x in myresult:
         L1.append(x[0])
     for i in L1 :
         L2.append(i[3])
     January=L2.count('1')
     February=L2.count('2')
     March=L2.count('3')
     April=L2.count('4')
     May=L2.count('5')
     return render_template('dashboard.html', Numberofdoctors= Numberofdoctors, Numberofpatients= Numberofpatients, Numberofnurses= Numberofnurses,Sumsalaryofnurses=Sumsalaryofnurses,Sumsalaryofdoctors=Sumsalaryofdoctors, AVGsalaryofdoctors=AVGsalaryofdoctors,AVGsalaryofnurses=AVGsalaryofnurses,Sumofprices=Sumofprices,Numberofvisitors=Numberofvisitors,January=January,February=February,March=March,April=April,May=May)
#End of Dashboard


#START OF ADD DOCTOR 
@app.route('/adddoctor',methods =  ['POST', 'GET'])
def adddoctor():
 if 'admin' in session:
    if request.method == 'POST': ##check if there is post data
      Dcode = request.form['Dcode']
      password = request.form['password']
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
      '''calendar = {
      'summary': 'MY SESSIONS',
      'timeZone': 'Africa/Cairo'
      }
      created_calendar = GCAL.calendars().insert(body=calendar).execute()
      Calendar_ID = created_calendar['id']
      rule = {
        'scope': {
            'type' : 'user',
            'value': mail,
        },
        'role': 'reader'
      }
      created_rule = GCAL.acl().insert(calendarId=Calendar_ID, body=rule).execute()'''
      sql = "INSERT INTO doctors ( Dcode,password,Dname,Mname,Lname,phone,mail,Birth_date,Doctor_ID,Syndicate_number,salary,gender,address,Job_rank,calendarid ) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s, %s,%s,%s,%s)"
      val = (Dcode, password ,Fname,Mname,Lname,phone,mail,BD,Doctor_ID,Syndicate_number,Salary,gender,address,Job_rank,Calendar_ID)
      mycursor.execute(sql, val)
      mydb.commit() 
      return render_template('index.html')
    else:
      return render_template('adddoctor.html')
 else:
     return redirect(url_for('hello_name'))    

#END OF ADD DOCTOR 

#START OF VIEW DOCTOR **** http://127.0.0.1:5000/viewdoctor
@app.route('/viewdoctor')
def viewdoctor():
 if 'admin' in session: 
   mycursor.execute("SELECT * FROM Doctors")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   return render_template('viewdoctor.html',DoctorsData = myresult)
 else:
     return redirect(url_for('hello_name')) 
#END OF VIEW DOCTOR 


#START OF DELETE DOCTOR 
@app.route('/deletedoctor/<string:id>',methods=['GET','POST'])
def deletedoctor(id):
 if 'admin' in session:
   mycursor = mydb.cursor()
   mycursor.execute("DELETE FROM doctors WHERE Dcode = %s", [id])
   mydb.commit()
   mycursor.execute("SELECT * FROM Doctors")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   return render_template('viewdoctor.html',DoctorsData = myresult)
 else:
     return redirect(url_for('hello_name'))        
#END OF DELETE DOCTOR

#START OF EDIT DOCTOR
@app.route('/editdoctor/<id>', methods = ['POST', 'GET'])
def editdoctor(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM doctors WHERE Dcode = %s", [id])
    myresult= mycursor.fetchall()
    return render_template('editdoctor.html',Dcode=myresult[0][0], password = myresult[0][1],Fname= myresult[0][2],Mname=myresult[0][3],Lname= myresult[0][4],phone=myresult[0][5],mail=myresult[0][6],Birth_date=myresult[0][7],Doctor_ID= myresult[0][8],Syndicate_number= myresult[0][9],Salary= myresult[0][10],gender = myresult[0][11],address= myresult[0][12],Job_rank= myresult[0][13])
@app.route('/updatedoctor', methods=['POST'])
def updatedoctor():
    if request.method == 'POST':
      Dcode = request.form['Dcode']
      password = request.form['password']
      Fname = request.form['Fname']
      Mname = request.form['Mname']
      Lname = request.form['Lname']
      phone = request.form['Phone']
      mail = request.form['mail']
      Birth_date = request.form['Birth_date']
      Doctor_ID= request.form['Doctor_ID']
      Salary= request.form['Salary']
      gender= request.form['gender']
      Syndicate_number= request.form['Syndicate_number']
      address= request.form['address']
      Job_rank= request.form['Job_rank']
      print(Salary)
      print(Lname)
      print(Fname)
      mycursor.execute(f"UPDATE `doctors` SET  password = {password},salary={Salary}, Doctor_ID = {Doctor_ID},phone = {phone},Syndicate_number = {Syndicate_number} WHERE Dcode = {Dcode}")
      mydb.commit()
      mycursor.execute("SELECT * FROM Doctors")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      return render_template('viewdoctor.html',DoctorsData = myresult)
#END OF EDIT DOCTOR

#START OF ADD PATIENT ***** http://127.0.0.1:5000/addpatient
@app.route('/addpatient',methods=["GET","POST"])
def addpatient():
 if 'admin' in session:  
   if request.method == 'POST': 
    Pcode=request.form ["Pcode"]
    password = request.form["password"]
    Fname = request.form["Fname"]
    Mname = request.form["Mname"]
    Lname = request.form["Lname"]
    Numofsessions=request.form["Num of sessions"]
    Daysofsessions=request.form["Days of sessions"]
    Patient_ID = request.form["Patient_ID"]
    phone = request.form["Phone"]
    mail = request.form["mail"]
    age= request.form["age"]
    gender=request.form["gender"]
    address = request.form["address"]
    Dry_weight= request.form["Dry_weight"]
    Described_drugs=request.form["Described_drugs"]
    scan=request.files["scan"]
    img=scan.read()
    img_name=scan.filename 
    SupD=request.form["SupD"]
    sql = 'INSERT INTO patients (Pcode, password,SupD,Pname,Mname,Lname,Numofsessions,Daysofsessions,Patient_ID,phone,mail,age,gender,address,Dry_weight,Described_drugs,scan,scan_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    val = (Pcode, password,SupD,Fname,Mname,Lname,Numofsessions,Daysofsessions,Patient_ID,phone,mail,age,gender,address,Dry_weight,Described_drugs,img,img_name)
    mycursor.execute(sql, val)
    mydb.commit()  
    return render_template('index.html')
   else:
    return render_template('addpatient.html')
 else:
     return redirect(url_for('hello_name')) 
#END OF ADD PATIENT 

#START OF VIEW PATIENT ***** http://127.0.0.1:5000/viewpatient
@app.route('/viewpatient')
def viewpatient():
   mycursor.execute("SELECT * FROM patients")
   row_headers =[x[0] for x in mycursor.description] #this will extract row headers
   myresult = mycursor.fetchall()
   return render_template('viewpatient.html',patientsData = myresult)
#END OF VIEW PATIENT 


#START OF DELETE patient
@app.route('/deletepatient/<string:id>',methods=['GET','POST'])
def deletepatient(id):
   mycursor = mydb.cursor()
   mycursor.execute("DELETE FROM patients WHERE Pcode = %s", [id])
   mydb.commit()
   mycursor.execute("SELECT * FROM patients")
   row_headers =[x[0] for x in mycursor.description] #this will extract row headers
   myresult = mycursor.fetchall()
   return render_template('viewpatient.html',patientsData = myresult)
#END OF DELETE patient

#START OF edit patient
@app.route('/editpatient/<id>', methods = ['POST', 'GET'])
def editpatient(id):
      mycursor = mydb.cursor()
      mycursor.execute("SELECT * FROM patients WHERE Pcode = %s", [id])
      myresult= mycursor.fetchall()
      return render_template('editpatient.html',Pcode=myresult[0][0], password = myresult[0][1],Fname= myresult[0][2],Mname=myresult[0][3],Lname= myresult[0][4],Numofsessions=myresult[0][5],Daysofsessions=myresult[0][6],Patient_ID=myresult[0][7],Phone= myresult[0][8],mail= myresult[0][9],age= myresult[0][10],gender = myresult[0][11],address= myresult[0][12],Dry_weight= myresult[0][13],Described_drugs = myresult[0][14],SupD= myresult[0][15])
@app.route('/updatepatient', methods=['POST'])
def updatepatient():
    if request.method == 'POST': 
     Pcode=request.form ["Pcode"]
     password = request.form["password"]
     Fname = request.form["Fname"]
     Mname = request.form["Mname"]
     Lname = request.form["Lname"]
     Numofsessions=request.form["Num of sessions"]
     Daysofsessions=request.form["Days of sessions"]
     Patient_ID = request.form["Patient_ID"]
     phone = request.form["Phone"]
     mail = request.form["mail"]
     age= request.form["age"]
     gender=request.form["gender"]
     address = request.form["address"]
     Dry_weight= request.form["Dry_weight"]
     Described_drugs=request.form["Described_drugs"]
     SupD=request.form["SupD"]
     mycursor.execute(f"UPDATE `patients` SET Pcode ={Pcode}, password = {password},Numofsessions={Numofsessions}, Patient_ID = {Patient_ID},phone = {phone},age = {age},Dry_weight = {Dry_weight} WHERE Pcode = {Pcode}")
     mydb.commit()
     mycursor.execute("SELECT * FROM patients")
     row_headers=[x[0] for x in mycursor.description] 
     myresult = mycursor.fetchall()
     return render_template('viewpatient.html',patientsData = myresult)
#END OF edit patient

#START OF Download 
@app.route('/download',methods=["POST",'GET'])
def download(): 
  patient_code=request.form["scanimg"]
  mycursor.execute(" SELECT * FROM  patients WHERE pcode=%s",[patient_code])
  for x in mycursor.fetchall():
    nameofscan=x[16]
    dataofscan=x[15]
    mydb.commit()
  return send_file(BytesIO(dataofscan),attachment_filename= str(nameofscan), as_attachment=True)
 #END OF Download 

#START OF ADD NURSE **** http://127.0.0.1:5000/addnurse 
@app.route('/addnurse', methods=["GET","POST"])
def addnurse():
 if 'admin' in session:
   if request.method == 'POST': 
    Ncode = request.form["Ncode"]
    password = request.form["password"]
    Fname = request.form["Fname"]
    Mname = request.form["Mname"]
    Lname = request.form["Lname"]
    phone = request.form["Phone"]
    mail = request.form["mail"]
    Birth_Date = request.form["Birth_Date"]
    Nurse_ID = request.form["Nurse_ID"]
    salary = request.form["salary"]
    gender = request.form["gender"]
    address = request.form["address"]
    syndicate_number=request.form["Syndicate_number"]
    sql = 'INSERT INTO nurses (Ncode, password,Nname,Mname,Lname,phone,mail,Birth_Date,Nurse_ID,salary,address,gender,syndicate_number) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    val = (Ncode, password,Fname,Mname,Lname,phone,mail,Birth_Date,Nurse_ID,salary,address,gender,syndicate_number)
    mycursor.execute(sql,val)
    mydb.commit() 
    return render_template('index.html')
   else:
    return render_template("addnurse.html")
 else:
     return redirect(url_for('hello_name')) 
#END OF ADD NURSE
 

#START OF VIEW NURSE **** http://127.0.0.1:5000/viewnurse
@app.route('/viewnurse')
def viewnurse():
 if 'admin' in session: 
   mycursor.execute("SELECT * FROM nurses")
   row_headers =[x[0] for x in mycursor.description] #this will extract row headers
   myresult = mycursor.fetchall()
   return render_template('viewnurse.html',nursesData=myresult)
 else:
     return redirect(url_for('hello_name'))  
#END OF VIEW NURSE


#START OF DELETE nurse
@app.route('/deletenurse/<string:id>',methods=['GET','POST'])
def deletenurse(id):
 if 'admin' in session:
   mycursor = mydb.cursor()
   mycursor.execute("DELETE FROM nurses WHERE Ncode = %s", [id])
   mydb.commit()
   mycursor.execute("SELECT * FROM nurses")
   row_headers =[x[0] for x in mycursor.description] #this will extract row headers
   myresult = mycursor.fetchall()
   return render_template('viewnurse.html',nursesData=myresult)
 else:
     return redirect(url_for('hello_name'))
#END OF DELETE nurse

#START OF edit nurse
@app.route('/editnurse/<id>', methods = ['POST', 'GET'])
def editnurse(id):
      mycursor = mydb.cursor()
      mycursor.execute("SELECT * FROM nurses WHERE Ncode = %s", [id])
      myresult= mycursor.fetchall()
      return render_template('editnurse.html',Ncode=myresult[0][0], password = myresult[0][1],Fname= myresult[0][2],Mname=myresult[0][3],Lname= myresult[0][4],phone=myresult[0][5],mail=myresult[0][6],Birth_Date=myresult[0][7],Nurse_ID= myresult[0][8],Syndicate_number= myresult[0][9],salary= myresult[0][10],gender = myresult[0][11],address= myresult[0][12])
 
@app.route('/updatenurse', methods=['POST'])
def updatenurse():
       if request.method == 'POST':
        Ncode = request.form["Ncode"]
        password = request.form["password"]
        Fname = request.form["Fname"]
        Mname = request.form["Mname"]
        Lname = request.form["Lname"]
        phone = request.form["Phone"]
        mail = request.form["mail"]
        Birth_Date = request.form["Birth_Date"]
        Nurse_ID = request.form["Nurse_ID"]
        salary = request.form["salary"]
        gender = request.form["gender"]
        address = request.form["address"]
        syndicate_number=request.form["Syndicate_number"]
      
        mycursor.execute(f"UPDATE `nurses` SET Ncode ={Ncode}, password = {password},salary={salary}, Nurse_ID = {Nurse_ID},phone = {phone},Syndicate_number = {syndicate_number} WHERE Ncode = {Ncode}")
        mydb.commit()
        mycursor.execute("SELECT * FROM nurses")
        row_headers=[x[0] for x in mycursor.description] 
        myresult = mycursor.fetchall()
        return render_template('viewnurse.html',nursesData = myresult)
#END OF edit nurse



#START OF ADD sessions ***** http://127.0.0.1:5000/addsession
@app.route('/addsession',methods =  ['POST', 'GET'])
def addsession(): 
 if 'admin' in session:
   if request.method == 'POST': ##check if there is post data
      Scode=request.form['Scode']
      D_code=request.form['D_code']
      N_code=request.form['N_code']
      P_code=request.form['P_code']
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
      sql = "INSERT INTO sessions (Scode,D_code,P_code,N_code,Date,used_device,price,record_by,after_weight,duration,taken_drugs,complications,dealing_with_complications,comments) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s,%s, %s, %s )"
      val = (Scode,D_code,P_code,N_code,Date,used_device,Price,record_by,after_weight,duration,taken_drugs,complications,dealing_with_complications,comments)
      mycursor.execute(sql,val)
      mydb.commit() 
      Time=Scode
      Am=Time[-1]
      AM=int(Am)
      pm=Time[-2]
      PM=int(pm)
      T=PM+AM
      D=int(duration)
      Duration=T+D
      mycursor.execute("SELECT calendarid FROM Doctors WHERE Dcode = %s", [D_code])
      ID= mycursor.fetchone()
      id=ID[0]
      '''calendar = GCAL.calendars().get(calendarId='primary').execute()
      event = {
      'summary': 'New session With patient{}'.format(P_code),
      "description": 'Hemodialysis_Departement',
      "start": {"dateTime": '{}T{:d}:00:00'.format(Date,T), "timeZone": 'Africa/Cairo'}, 
      "end": {"dateTime":'{}T{:d}:00:00'.format(Date,Duration), "timeZone": 'Africa/Cairo'},
     }
     
      e = GCAL.events().insert(calendarId=id,sendNotifications=True, body=event).execute()'''
      return render_template('index.html')
   else:
      return render_template('addsession.html')
 else:
     return redirect(url_for('hello_name')) 
#END OF ADD sessions

#START OF VIEW sessions **** http://127.0.0.1:5000/viewsession
@app.route('/viewsession')
def viewsession():
    if 'admin' in session:
      mycursor.execute("SELECT * FROM sessions")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      return render_template('viewsession.html',sessionsData = myresult)
    else:
     return redirect(url_for('hello_name')) 
#END OF VIEW sessions


#START OF edit session
@app.route('/editsession/<id>', methods = ['POST', 'GET'])
def editsession(id):
      mycursor = mydb.cursor()
      mycursor.execute("SELECT * FROM sessions WHERE Scode = %s", [id])
      myresult= mycursor.fetchall()
      return render_template('editsession.html',Scode=myresult[0][0], Date = myresult[0][1],used_device= myresult[0][2],Price=myresult[0][3],record_by=myresult[0][4],after_weight=myresult[0][5],duration=myresult[0][6],complications= myresult[0][7],dealing_with_complications= myresult[0][8],taken_drugs= myresult[0][9],comments= myresult[0][10],P_code= myresult[0][11],D_code= myresult[0][12],N_code= myresult[0][13])
@app.route('/updatesession', methods=['POST'])
def updatesession():

   if request.method == 'POST': ##check if there is post data
      Scode=request.form['Scode']
      D_code=request.form['D_code']
      N_code=request.form['N_code']
      P_code=request.form['P_code']
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
      mycursor.execute(f"UPDATE `sessions` SET Scode ={Scode},Price={Price}, after_weight = {after_weight},duration = {duration} WHERE Scode = {Scode}")
      mydb.commit()
      mycursor.execute("SELECT * FROM sessions")
      row_headers=[x[0] for x in mycursor.description] 
      myresult = mycursor.fetchall()
      return render_template('viewsession.html',sessionsData = myresult)
 #END OF edit session


#START OF sesssion 
@app.route('/pviewsession')
def pviewsession():      
   if 'pcode' in session:
       mycursor.execute("SELECT pcode,Scode, Date, price, after_weight, duration, taken_drugs,scan,scan_name, complications, dealing_with_complications, comments, Dname, Nname FROM sessions JOIN Doctors ON Dcode = D_code JOIN patients ON Pcode=P_code JOIN nurses ON Ncode = N_code WHERE P_code = %s", [session['pcode']] )
       psession = mycursor.fetchall()
       return render_template('pviewsession.html',psession = psession) 
   else:
     return redirect(url_for('hello_name'))     
@app.route('/pdownload',methods=["POST",'GET'])
def pdownload(): 
        ppatient_code=request.form["pscanimg"]
        mycursor.execute(" SELECT * FROM  patients WHERE pcode=%s",[ppatient_code])
        for x in mycursor.fetchall():
            pnameofscan=x[16]
            pdataofscan=x[15]
            print(pdataofscan)
 
        mydb.commit()
       
        return send_file(BytesIO(pdataofscan),attachment_filename= str(pnameofscan), as_attachment=True)
@app.route('/dviewsession')
def dviewsession():      
   if 'dcode' in session:
       mycursor.execute("SELECT pcode,Dcode,Dname,Nname,Pname,Scode,Date,used_device,record_by,Dry_weight,after_weight,duration,taken_drugs,described_drugs,scan,scan_name,complications,dealing_with_complications,comments FROM doctors JOIN sessions ON Dcode = D_code JOIN patients ON Pcode=P_code JOIN Nurses ON Ncode=N_code WHERE Dcode = %s", [session['dcode']] )
       dsession = mycursor.fetchall()
       return render_template('dviewsession.html',dsession = dsession) 
   else:
     return redirect(url_for('hello_name'))       
@app.route('/ddownload',methods=["POST",'GET'])
def ddownload(): 
  dpatient_code=request.form["dscanimg"]
  mycursor.execute(" SELECT * FROM  patients WHERE pcode=%s",[dpatient_code])
  for x in mycursor.fetchall():
    dnameofscan=x[16]
    ddataofscan=x[15]
    print(ddataofscan)
    mydb.commit()
  return send_file(BytesIO(ddataofscan),attachment_filename= str(dnameofscan), as_attachment=True)
@app.route('/nviewsession')
def nviewsession():      
   if 'ncode' in session:
       mycursor.execute("SELECT pcode,Ncode,Nname,Dname,Pname,Scode,Date,used_device,record_by,Dry_weight,after_weight,duration,taken_drugs,described_drugs,scan,scan_name,complications,dealing_with_complications,comments FROM nurses JOIN sessions ON Ncode = N_code JOIN patients ON Pcode=P_code JOIN Doctors ON Dcode=D_code WHERE Ncode = %s", [session['ncode']] )
       nsession = mycursor.fetchall()
       return render_template('nviewsession.html',nsession = nsession) 
   else:
     return redirect(url_for('hello_name')) 
#END OF sesssion 
@app.route('/ndownload',methods=["POST",'GET'])
def ndownload(): 
  npatient_code=request.form["nscanimg"]
  mycursor.execute(" SELECT * FROM  patients WHERE pcode=%s",[npatient_code])
  for x in mycursor.fetchall():
    nnameofscan=x[16]
    ndataofscan=x[15]
    print(ndataofscan)
    mydb.commit()
  return send_file(BytesIO(ndataofscan),attachment_filename= str(nnameofscan), as_attachment=True)
#START OF DELETE session
@app.route('/deletesession/<string:id>',methods=['GET','POST'])
def deletesession(id):
 if 'admin' in session:  
    mycursor = mydb.cursor()
    mycursor.execute("DELETE FROM sessions WHERE Scode = %s", [id])
    mydb.commit()
    mycursor.execute("SELECT * FROM sessions")
    row_headers=[x[0] for x in mycursor.description] 
    myresult = mycursor.fetchall()
    return render_template('viewsession.html',sessionsData = myresult)
 else:
     return redirect(url_for('hello_name')) 
#END OF DELETE session





#**********log in page http://127.0.0.1:5000/login 
@app.route('/login', methods=['GET', 'POST'])
def login():
 # connect
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        mycursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = mycursor.fetchone()
   
    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('hello_name'))
        elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
          # Create variables for easy access
          username = request.form['username']
          password = request.form['password']
          # Check if account exists using MySQL
          mycursor.execute('SELECT * FROM admins WHERE admin_name = %s AND password = %s', (username, password))
          # Fetch one record and return result
          adminaccount = mycursor.fetchone()
          if adminaccount:
            # Create session data, we can access this data in other routes
              session['adminloggedin'] = True
            
              session['admin'] = adminaccount[0]
              session['adminpass'] = adminaccount[1]
              #session['acess_level'] = adminaccount[2]
            # Redirect to home page
            #return 'Logged in successfully!'
              return redirect(url_for('hello_name'))    
          else:
            # Account doesnt exist or username/password incorrect
              msg = 'Incorrect username/password!'
            
    
    
    return render_template('login.html', msg=msg)

#********** roles log in page http://127.0.0.1:5000/roleslogin
@app.route('/roleslogin/', methods=['GET', 'POST'])
def roleslogin():

    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'dcode' in request.form and 'dpassword' in request.form:
        # Create variables for easy access
        dcode = request.form['dcode']
        dpassword = request.form['dpassword']
        mycursor.execute('SELECT * FROM doctors WHERE Dcode = %s AND password = %s', (dcode, dpassword))
        daccount = mycursor.fetchone()
        if daccount:
            # Create session data, we can access this data in other routes
            session['dloggedin'] = True
            session['dcode'] = daccount[0]
            session['dpassword'] = daccount[1]
            session['Dname'] = daccount[2]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('hello_name'))  
        elif request.method == 'POST' and 'ncode' in request.form and 'npassword' in request.form:
        # Create variables for easy access
          ncode = request.form['ncode']
          npassword = request.form['npassword']
          mycursor.execute('SELECT * FROM nurses WHERE Ncode = %s AND password = %s', (ncode, npassword))
          naccount = mycursor.fetchone()  
          if naccount:
            # Create session data, we can access this data in other routes
            session['nloggedin'] = True
            session['ncode'] = naccount[0]
            session['npassword'] = naccount[1]
            session['Nname'] = naccount[2]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('hello_name'))             
          elif request.method == 'POST' and 'pcode' in request.form and 'ppassword' in request.form:
        # Create variables for easy access
           pcode = request.form['pcode']
           ppassword = request.form['ppassword']    
           mycursor.execute('SELECT * FROM patients WHERE Pcode = %s AND password = %s', (pcode, ppassword))
           paccount = mycursor.fetchone()
           if paccount:
            # Create session data, we can access this data in other routes
            session['ploggedin'] = True
            session['pcode'] = paccount[0]
            session['ppassword'] = paccount[1]
            session['Pname'] = paccount[2]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('hello_name')) 
           else:
            # Account doesnt exist or username/password incorrect
            
              msg = 'Incorrect code/password!'


    
    return render_template('roleslogin.html', msg=msg)

@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        fullname = request.form['fullname']
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email']
   
        mycursor.execute('SELECT * FROM accounts WHERE username = %s', (username, )) 
        account = mycursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            #mycursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s)', (fullname, username, password, email))
            sql = 'INSERT INTO accounts (id, fullname, username, password, email) VALUES (NULL, %s, %s, %s, %s)'
            val = (fullname, username, password, email)
            mycursor.execute(sql, val)
            mydb.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)    

# **************** http://localhost:5000/logout - this will be the logout page 
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('adminloggedin', None)
   session.pop('admin', None)
   session.pop('adminpass', None)
   session.pop('dloggedin', None)
   session.pop('nloggedin', None)
   session.pop('ploggedin', None)
   session.pop('dcode', None)
   session.pop('ncode', None)
   session.pop('pcode', None)  
   session.pop('dpassword', None)
   session.pop('npassword', None)
   session.pop('ppassword', None)   
   # Redirect to login page
   return render_template('index.html')
 

# *************** http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile(): 
 # Check if account exists using MySQL
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        mycursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = mycursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    elif 'ploggedin' in session: 
        mycursor.execute('SELECT * FROM patients WHERE pcode = %s', [session['pcode']])
        paccount = mycursor.fetchone()
        return render_template('patientprofile.html', paccount=paccount)
    elif 'dloggedin' in session: 
        mycursor.execute('SELECT * FROM Doctors WHERE dcode = %s', [session['dcode']])
        daccount = mycursor.fetchone()
        return render_template('doctorprofile.html', daccount=daccount)
    elif 'nloggedin' in session: 
        mycursor.execute('SELECT * FROM nurses WHERE ncode = %s', [session['ncode']])
        naccount = mycursor.fetchone()
        return render_template('nurseprofile.html', naccount=naccount)                   
    # User is not loggedin redirect to login page
    return redirect(url_for('hello_name'))

if __name__ == '__main__':
   #app.run()
   app.run(debug=True)
   