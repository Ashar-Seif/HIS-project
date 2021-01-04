from flask import Flask, render_template
app = Flask(__name__,template_folder='template')

@app.route('/')
def hello_name():
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
def viewpatient():
   return render_template('viewpatient.html')

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

   