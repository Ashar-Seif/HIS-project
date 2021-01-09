from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector
import re

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="hemodialysis"
)

mycursor = mydb.cursor()
app = Flask(__name__)

app.secret_key = 'team13'

@app.route('/roleslogin/', methods=['GET', 'POST'])
def rolelogin():

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
            session['loggedin'] = True
            session['dcode'] = daccount[0]
            session['dpassword'] = daccount[1]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home')) 
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect code/password!'                   
    elif request.method == 'POST' and 'ncode' in request.form and 'npassword' in request.form:
        # Create variables for easy access
        ncode = request.form['ncode']
        npassword = request.form['npassword']
        mycursor.execute('SELECT * FROM nurses WHERE Ncode = %s AND password = %s', (ncode, npassword))
        naccount = mycursor.fetchone()  
        if naccount:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ncode'] = naccount[0]
            session['npassword'] = naccount[1]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home')) 
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect code/password!'              
    elif request.method == 'POST' and 'pcode' in request.form and 'ppassword' in request.form:
        # Create variables for easy access
        pcode = request.form['pcode']
        ppassword = request.form['ppassword']    
        mycursor.execute('SELECT * FROM patients WHERE Pcode = %s AND password = %s', (pcode, ppassword))
        paccount = mycursor.fetchone()
        if paccount:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['pcode'] = paccount[0]
            session['ppassword'] = paccount[1]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home')) 
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect code/password!'                                       


    
    return render_template('index.html', msg=msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('home.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()