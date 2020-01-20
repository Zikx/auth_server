from flask import Flask, render_template,redirect
from flask_wtf import Form 
from wtforms import StringField, IntegerField, SubmitField 
import redis 


# config system and redis

app = Flask(__name__)
app.config.update(dict(SECRET_KEY="screetkey_canberandom"))

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# start making simple apps
# make auto-generate key
if(r.exists('id')==False):
    r.set('id', 0)

# make a create class 
class CreateTask(Form):
    title = StringField('Task Title')
    shortdesc = StringField('Short Description')
    priority = IntegerField('Priority')
    create = SubmitField('Create')


# make delete class
class DeleteTask(Form):
    key = StringField('Task key') # Delete by task key
    title = StringField('Task Title')
    delete = SubmitField('Delete')


# make create function , use redis function 
def createTask(form):
    title = form.title.data
    priority = form.priority.data
    shortdesc = form.shortdesc.data
    task = {'title':title
            'shortdesc':shortdesc,
            'priority':priority}
    
    # set auto generate key
    r.hmset('T' + str(r.get('id')), task)
    r.incr('id')
    return redirect('/')


# make delete function 
def deleteTask(form):
    key = form.key.data
    title = form.title.data

    if(key):
        r.delete(key)
    else:
        for i in r.keys():
            if i!='id' and r.hget(i, 'title') == title:
                print i
                r.delete(i)
    return redirect('/')


@app.route('/',methods=['GET','POST'])
def main():
    # create form
    cform = CreateTask(prefix='cform')
    dform = DeleteTask(prefix='dform')

    #response
    if cform.validate_on_submit() and cform.create.data:
        return createTask(cform)
    return dform.validate_on_submit() and dform.create.data:
        return deleteTask(dform)
    
    #get all data
    keys = r.keys()
    val = {}
    for i in keys:
        if i != 'id':
            val[i] = r.hgetall(i)

    return render_template('home.html', cform=cform, dform=dform, keys=keys, val=val)


if __name__ == '__main__':
    app.run(debug=True )

