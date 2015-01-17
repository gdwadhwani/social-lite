import sqlite3
from flask import *
from contextlib import closing
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField,FileField, RadioField,validators
import os
import nltk
from nltk.tokenize import *
import re

DATABASE = 'flaskr.db'
DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'



# utils
def handletag(s):
    output = []
    s = word_tokenize(s)
    corpus = nltk.pos_tag(s)
    for item in corpus:
        if item[1] in ["NNPS","NNP"]:
            output.append( item[0] )
    if len(output) > 5:
        output=output[:5]
    return output


@app.route('/')
def render_index_page():
    session["username"]="admin"
    return render_template('index.html')


@app.route('/profile')
def render_profile_page():
    return render_template('profile_bq.html')


@app.route('/addNewEvent')
def render_add_new_event_page():
    return render_template('addNewEvent.html')


@app.route('/eventDetail',methods=['GET','POST'])
def gotoEventDetail():
    item = request.data
    if len(item) > 0:
        session['detaileventid'] = item
    return render_template('eventDetail.html')


@app.route('/account_index')
def render_account_index():
    return render_template('account_index.html')

'''
# login and signup
class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired("Username is required!")])
    password = PasswordField('Password', [validators.DataRequired("Password is required!")])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm1(Form):
    username = StringField('Username', [validators.DataRequired("Username is required!")])
    password = PasswordField('Password', [
        validators.DataRequired("Password is required!"),validators.length(min=6),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password',[validators.DataRequired("Password Confirm is required!")])


@app.route('/')
def index():
    return render_template("layout.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        cur = g.db.execute('select username,password from userdata where username=? and password=?',
                           (form.username.data,form.password.data))
        if len(cur.fetchall()) != 0:
            print "Log in"
            session['username'] = form.username.data
            if form.remember_me.data==True:
                session.permanent = True
            return render_template("layout.html")
        else:
            form.errors["invalid"] = ["Invalid Username or Password!"]
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    print "log out"
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm1(request.form)
    if form.validate_on_submit():
        cur = g.db.execute('select username,password from userdata where username=?',([form.username.data]))
        if len(cur.fetchall()) != 0:
            form.errors["repeat"] = ["Username has been used!"]
        else:
            g.db.execute('insert into userdata values (?,?)',(form.username.data,form.password.data))
            g.db.commit()
            session['username']=form.username.data
            return redirect(url_for('profile'))
    return render_template('signup.html', form=form)


# profile
class RegisterForm2(Form):
    email = StringField('Email Address', [validators.DataRequired(), validators.Email()])
    gender= RadioField('Gender',[validators.DataRequired()],choices=[("male","male"),("female","female")])
    photo = FileField('Your photo')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = RegisterForm2(request.form)
    if form.validate_on_submit():

        g.db.execute('insert into userinfo(username,u_gender,u_email) values (?,?)',
                     (session['username'],form.gender.data,))
        g.db.commit()
        print "profile"

        file = request.files['photo']
        filename = session['username']+ "."+file.filename.split(".")[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print filename
        return redirect(url_for('index'))
    return render_template('profile.html', form=form)

'''

@app.route('/currentUserInfo')
def get_current_user_info():
    '''
    currentUserInfo = {
        'username': "100001userid",
        'password': "test password",
        'displayname': "test user displayname",
        'email': "huangbq.01@gmail.com",
        'address': "college park, MD",
        'city': 'test city',
        'state': 'test state',
        'birth': '1989-12-12',
        'gender': "male",
        'bio': "I'm interested in everything! I'm a test user!",
        'interests': [{
            'name': "Social Media",
            'parent': "Internet & Technology"
        },
        {
            'name': "Interaction Design",
            'parent': "Internet & Technology"
        },
        {
            'name': "Cloud Computing",
            'parent': "Internet & Technology"
        }],

    }
    '''

    username = session["username"]
    currentUserInfo= {}
    cur = g.db.execute("select * from userinfo where username= ?", [username])
    for row in cur:
        currentUserInfo["displayname"] = row[1]
        currentUserInfo["gender"] = row[2]
        currentUserInfo["birth"] = row[3]
        currentUserInfo["email"] = row[4]
        currentUserInfo["address"] = row[6]
        currentUserInfo["state"] = row[7]
        currentUserInfo["city"] = row[8]
        currentUserInfo["interests"] = row[9].split(",")
        currentUserInfo["bio"] =row[10]
    return json.dumps(currentUserInfo)

# fixme date
@app.route('/createNewEvent', methods=['GET', 'POST'])
def create_new_event():
    item = json.loads(request.data)
    e_title = item['title']
    e_time = item['date']
    e_address = item['address']
    e_city = item['city']
    e_state = item['state']
    e_detail = item['detail']
    e_tag = ",".join(handletag(e_detail))
    category = ",".join(item['category'])
    g.db.execute("insert into event(e_title,e_time,e_address,e_detail,e_city,e_state,e_tag, category) values (?,?,?,?,?,?,?,?)",
                 (e_title,e_time,e_address,e_detail,e_city,e_state,e_tag,category))
    g.db.commit()
    eid = g.db.execute("select eventid from event where e_title=? order by eventid DESC",[e_title]).fetchone()[0]
    print "Create event"
    print "eventid"+str(eid)
    g.db.execute("insert into event_user(eventid,creator) values (?,?)",(eid,session['username']))
    g.db.commit()
    print "Create event_user"
    session["detaileventid"] = eid
    return "Success!"


# return one event
@app.route('/getEventDetail', methods=['GET', 'POST'])
def getEventDetail():
    '''
        item = {
        'name': 'test event name',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'category': [
            'test cate 1',
            'test cate 2',
            'test cate 3'
        ]
    }
    '''

    eventid = session["detaileventid"]
    output={}
    cur3 = g.db.execute("select * from event,event_user where event.eventid=? and event.eventid=event_user.eventid",[eventid])
    for row in cur3:
        output["eventid"] = row[0]
        output["title"] = row[1]
        output["detail"] = row[2]
        output["date"] = row[3]
        output["address"] = row[4]
        output["city"] = row[5]
        output["state"] = row[6]
        if row[7] is not None:
            output["tag"] = row[7].split(",")
        else:
            output["tag"] = row[7]
        if row[8] is not None:
            output["category"] = row[8].split(",")
        else:
            output["category"] = row[8]
        output["creator"] = row[10]
        if row[11] is not None:
            output["member"] = row[11].split(",")
        else:
            output["member"] = row[11]
        output["member_count"] = row[12]
        output["thumbnail"] = session["username"] + ".png"
    print output
    item = output
    return json.dumps(item)


#recommendation
@app.route('/getReco',methods=['GET', 'POST'])
def get_reco():
    # get the useraddress
    u_city = "None"
    u_interests = "None"
    cur = g.db.execute("select u_city,u_interests from userinfo where username=?",[session['username']])
    for row in cur.fetchall():
        u_city = row[0]
        u_interests = row[1].split(",")
    print "u_city: " + u_city
    print u_interests

    eventid=[]
    cur = g.db.execute("select event.eventid, event.category, event_user.member, event_user.creator from "
                       "event,event_user where event.e_city=? and event.eventid=event_user.eventid order by event_user.membercount DESC",
                        [u_city])
    result=cur.fetchall()
    print "result#: "+ str(len(result))

    # judge whether have 10 more events near user
    # FIXME: change to 10 or other
    if len(result) < 1:
        for row in result:
            eventid.append(row[0])
        print eventid

    for row in result:
        for i in row[1].split(","):
            if i in u_interests:
                eventid.append(row[0])

    # over 10 have 10
    if len(eventid) > 10:
        eventid = eventid[:10]


    if len(eventid) < 10:

        for child in u_interests:
            cur2 = g.db.execute("select parent from parenlist where child=?",[child])
            for row in cur2.fetchall():
                 u_interests.append(row[0])

        print "Have Parent, current u_interests:"
        print u_interests
        eventid=[]
        for row in result:
            for i in row[1].split(","):
                if i in u_interests:
                    eventid.append(row[0])

    entry = []
    for i in eventid:
        cur3 = g.db.execute("select * from event,event_user where event.eventid=? and event.eventid=event_user.eventid",[i])
        for row in cur3:
            output={}
            output["eventid"] = row[0]
            output["title"] = row[1]
            output["detail"] = row[2]
            output["date"] = row[3]
            output["address"] = row[4]
            output["city"] = row[5]
            output["state"] = row[6]
            if row[7] is not None:
                output["tag"] = row[7].split(",")
            else:
                output["tag"] = row[7]
            if row[8] is not None:
                output["category"] = row[8].split(",")
            else:
                output["category"] = row[8]
            output["creator"] = row[10]
            if row[11] is not None:
                output["member"] = row[11].split(",")
            else:
                output["member"] = row[11]

            output["member_count"] = row[12]
            output["thumbnail"] = session["username"] + ".png"
            print output
            entry.append(output)
    print entry
    return json.dumps(entry)



@app.route('/all-interests')
def load_all_interests():
    '''
    all_interests = [{
        'name': "Art",
        'parent': "Arts & Entertainment"
    }, {
        'name': "Fiction",
        'parent': "Arts & Entertainment"
    }]
    '''
    all_interests=[]
    cur_parent = g.db.execute("select * from parenlist")
    result = cur_parent.fetchall()
    print result
    for row in result:
        interest={}
        interest["name"] = row[0]
        interest["parent"] = row[1]
        all_interests.append(interest)
    return json.dumps(all_interests)


@app.route('/all-events')
def load_all_events():
    '''
    all_events = [{
        'eventid': 123,
        'name': "DC wine hangout",
        'thumbnail': "static/img/1.jpg",
        'caption': "The wine Caption"
    }, {
        'eventid': 126,
        'name': "Maryland basketball meetup",
        'thumbnail': "static/img/4.jpg",
        'caption': "GET A DUNK!"
    }]
    '''
    all_events = []
    cur_event = g.db.execute("select * from event,event_user where event.eventid=event_user.eventid")
    for row in cur_event:
        output={}
        output["eventid"] = row[0]
        output["name"] = row[1]
        output["detail"] = row[2]
        output["date"] = row[3]
        output["address"] = row[4]
        output["city"] = row[5]
        output["state"] = row[6]
        if row[7] is not None:
            output["tag"] = row[7].split(",")
        else:
            output["tag"] = row[7]
        if row[8] is not None:
            output["category"] = row[8].split(",")
        else:
            output["category"] = row[8]
        output["creator"] = row[10]
        if row[11] is not None:
            output["member"] = row[11].split(",")
        else:
            output["member"] = row[11]
        output["member_count"] = row[12]
        output["thumbnail"] = session["username"] + ".png"
        all_events.append(output)

    return json.dumps(all_events)

# user
@app.route('/updateCurrentUser', methods=["POST"])
def update_current_user():
    '''
      username text primary key,
      displayname text,
      u_gender text,
      u_birth text,
      u_email text,
      u_image text,
      u_address text,
      u_state text,
      u_city text,
      u_interests text,
      u_bio text,
    :
    '''
    item = json.loads(request.data)
    username= item["username"]
    displayname = item["displayname"]
    gender = item["gender"]
    birth = item["birth"]
    email = item["email"]

    file = request.files['photo']
    filename = username+".png"
    path = "uploads/"+ filename
    if os.path.isfile(path):
        os.remove(path)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    address = item["address"]
    state = item["state"]
    city = item["city"]
    interests = ",".join(item["interests"])
    g.db.execute("update userinfo set displayname=?, gender=?, birth=?, email=?, address=?, state=?, city=?, interests=?",
                 [displayname,gender,birth,email,address,state,city,interests])
    g.db.commit()
    return "Success!"


@app.route('/rsvpEvent', methods=["POST"])
def rsvpEvent():
    username = session["username"]
    eventid = session["detaileventid"]
    cur = g.db.execute("select member,membercount from event_user where eventid=?",[eventid])
    result = cur.fetchone()
    print result
    output={}
    output["member"] = result[0]+","+username
    output["membercount"] = int(result[1]) + 1
    g.db.execute("update event_user set member=?, membercount = ? where eventid = ?",[output["member"],output["membercount"],eventid] )
    g.db.commit()

    return 'Success!'

#database
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('data.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/getRsvpedEvent')
def get_rsvped_event():
    '''
    item = [{
        'title': 'test event name',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': [
            'test cate 1',
            'test cate 2',
            'test cate 3'
        ],
        'tag': [
            'tag a',
            'tag b'
        ],
        'creator': 'username of creator',
        'member': [
            'attender 1 username',
            'attender 2 username'
        ],
        'member_count': 2
    }, {
        'title': 'test event name 2',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': [
            'test cate 1',
            'test cate 2',
            'test cate 3'
        ],
        'tag': [
            'tag a',
            'tag b'
        ],
        'creator': 'username of creator',
        'member': [
            'attender 1 username',
            'attender 2 username'
        ],
        'member_count': 3
    }]
    '''
    username = session["username"]
    cur = g.db.execute("select eventid,member from event_user")
    eventid=[]
    for row in cur.fetchall():
        member = row[1].split(",")
        if username in member:
            eventid.append(row[0])
    print eventid


    entry = []
    for i in eventid:
        cur3 = g.db.execute("select * from event,event_user where event.eventid=? and event.eventid=event_user.eventid",[i])
        for row in cur3:
            output = {}
            output["eventid"] = row[0]
            output["title"] = row[1]
            output["detail"] = row[2]
            output["date"] = row[3]
            output["address"] = row[4]
            output["city"] = row[5]
            output["state"] = row[6]
            if row[7] is not None:
                output["tag"] = row[7].split(",")
            else:
                output["tag"] = row[7]
            if row[8] is not None:
                output["category"] = row[8].split(",")
            else:
                output["category"] = row[8]
            output["creator"] = row[10]
            if row[11] is not None:
                output["member"] = row[11].split(",")
            else:
                output["member"] = row[11]
            output["member_count"] = row[12]
            output["thumbnail"] = session["username"] + ".png"
            entry.append(output)
    print entry
    return json.dumps(entry)


if __name__ == '__main__':
    app.run()
