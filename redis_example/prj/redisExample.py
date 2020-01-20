# #!/bin/python

# # Dependencies:
# # pip install flask
# # pip install redis

# from flask import Flask
# from flask import request
# import flask
# import redis
# import time
# import json
# from flask import Response, stream_with_context

# app = Flask(__name__)
# app.debug = True
# db = redis.Redis('localhost') #connect to server

# ttl = 31104000 #one year

# def isInt(s):
#     try:
#         int(s)
#         return True
#     except ValueError:
#         return False

# @app.route('/', defaults={'path': ''}, methods = ['PUT', 'GET'])
# @app.route('/<path:path>', methods = ['PUT', 'GET'])
# def home(path):

#     if (request.method == 'PUT'):
#         event = request.json
#         event['last_updated'] = int(time.time())
#         event['ttl'] = ttl
#         db.delete(path) #remove old keys
#         db.hmset(path, event)
#         db.expire(path, ttl)
#         return json.dumps(event), 201

#     if not db.exists(path):
#         return "Error: thing doesn't exist"

#     event = db.hgetall(path)
#     event["ttl"] = db.ttl(path)
#     #cast integers accordingly, nested arrays, dicts not supported for now  :(
#     dict_with_ints = dict((k,int(v) if isInt(v) else v) for k,v in event.iteritems())
#     return json.dumps(dict_with_ints), 200

# import redis

# client = redis.Redis(host = '0.0.0.0', port = 6379)

# if client.keys('somethingIdOrPassword'):
#     print('true!!')

# # client.set('language', 'Python')


# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')

#     user = client.keys(email)
#     # user = User.query.filter_by(email=email).first()
#     if user:
#         flash('Email address already exists.')
#         return redirect(url_for('auth.login'))
#     new_user = User(email=email, name=name, password=generate_password_hash(password, methds='sha256'))    

#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.login'))

# from flask.ext.mysql import MySQL

# MYSQL = MySQL()

@app.route('/login', methods=['post', 'get'])
def login():
    error = None
    if request.method == 'POST':
       
        email = request.form['email']
        pw = request.form['pw']
       
        conn = mysql.connect(host='localhost', user='root', passwd='admin', db='python', charset='utf8')
        cursor = conn.cursor()
        
        query = "SELECT user_name FROM user_table WHERE user_email = %s AND user_pw = %s"
        value = (email, pw)
        cursor.execute("set names utf8")
        cursor.execute(query, value)
        data = (cursor.fetchall())
       
        cursor.close()
        conn.close()
       
        for row in data:
            data = row[0]
       
        if data:
            print 'login success'
            return redirect(url_for('success', name=data))
        else:
            error = 'Invalid input data detected!'
           
        #return redirect(url_for('success', name=user))
   
    return render_template('python_login.html', error=error)

@app.route('/regist', methods=['post', 'get'])
def regist():
    error = None
    if request.method == 'POST':
       
        name = request.form['name']
        email = request.form['email']
        pw = request.form['pw']
       
        print name, email, pw
       
        conn = mysql.connect(host='localhost', user='root', passwd='admin', db='python', charset='utf8')
        cursor = conn.cursor()
       
        query = "SELECT 1 FROM user_table WHERE user_email = '%s' " % (email)
        #value = (email)
        cursor.execute(query)
        data = cursor.fetchall()
       
        if data:
            print 'user other email'
            error = "The email is already used. please use another one"
        else:
            print 'use it okay'
            query = "INSERT INTO user_table (user_name, user_email, user_pw) values (%s, %s, %s)"
            value = (name, email, pw)
            cursor.execute(query, value)
            data = cursor.fetchall()
            print data
            if not data:
                conn.commit()
                print data
                return "Register Success"
            else:
                conn.rollback()
                print data
                return "Register Failed"
       
       
        cursor.close()
        conn.close()

    return render_template('python_regist.html', error=error)