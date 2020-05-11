from flask import Flask, request, make_response 
from flask_mysqldb import MySQL 
from functools import wraps
import hashlib

app = Flask(__name__)
    

def auth_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if auth and auth.username == 'username' and auth.password == 'password':
               return f(*args, **kwargs)
               
            return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            
        return decorated

   

app.config['MYSQL_USER'] = 'E6jelsj7BW'
app.config['MYSQL_PASSWORD'] = 'ou4J1Od4oM'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_DB'] = 'E6jelsj7BW'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
print("In the program")
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('''select * from example''')
    if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
        return '<h1> Thank you for successful login</h1>'
        
    return make_response('Unsuccessful credentials', 401, {'www-Authenticate' : 'Basic realm="Login Required"'})
    
    
@app.route('/page')
def page():
    return '<h1>Authentication failed</h1>'

if __name__ == '__main__':
    app.run(debug=True)
    
    #print("before cursor; In index funtion of the program")
    #cur = mysql.connection.cursor()
    #print("In index funtion of the program")
    #cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')
    #cur.execute('''select * from example''')
    #print("After the select")
    #return 'Done!'

    #cur.execute('''INSERT INTO example VALUES (1, 'NK')''')
    #cur.execute('''INSERT INTO example VALUES (2, 'NK1')''')
    #mysql.connection.commit()

    #cur.execute('''SELECT * FROM example''')
    #results = cur.fetchall()
    #print(results)
    #return str(results[1]['id'])
