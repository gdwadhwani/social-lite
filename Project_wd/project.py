import sqlite3
from flask import *
from contextlib import closing
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField,FileField, RadioField,validators
import os

DATABASE = 'flaskr.db'
DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

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
        '''
        g.db.execute('insert into userinfo(username,u_gender,u_email) values (?,?)',
                     (session['username'],form.gender.data,))
        g.db.commit()
        print "profile"
        '''
        file = request.files['photo']
        filename = session['username']+ "."+file.filename.split(".")[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print filename
        return redirect(url_for('index'))
    return render_template('profile.html', form=form)





# events(need a link to direct to this page, need first login)
@app.route('/create', methods=['GET', 'POST'])
def createevent():
    e_title = request.args.get('title')
    e_time = request.args.get('time')
    e_address = request.args.get('address')
    e_detail = request.args.get('detail')
    if e_title!=None:
        g.db.execute("insert into event(e_title,e_time,e_address,e_detail) values (?,?,?,?)",
                     (e_title,e_time,e_address,e_detail))
        g.db.commit()
        eid = g.db.execute("select eventid from event where e_title=?",[e_title]).fetchone()[0]
        print "Create event"
        print "eventid"+str(eid)
        g.db.execute("insert into event_user(eventid,creator) values (?,?)",(eid,session['username']))
        g.db.commit()
        print "Create event_user"
        return redirect(url_for('index'))

    return render_template('create.html')


# the temporary event search
@app.route('/show', methods=['GET', 'POST'])
def show():
    cur = g.db.execute("select e_title,e_time, e_address, e_detail from event")
    output={}
    for row in cur.fetchall():
        output["e_title"] = row[0]
        output["e_address"] = row[1]
        output["e_detail"] = row[2]
    print output
    return jsonify(output)


#recommendation
@app.route('/search',methods=['GET', 'POST'])
def search():
    # get the useraddress
    u_address = "None"
    u_interests = "None"
    cur = g.db.execute("select u_city,u_interests from userinfo where username=?",[session['username']])
    for row in cur.fetchall():
        u_address = row[0]
        u_interests = row[1].split(",")
    print "u_address: " + u_address
    print u_interests

    #TODO: maybe use the distance between two place
    eventid=[]
    cur = g.db.execute("select event.eventid, event.category, event_user.member, event_user.creator from "
                       "event,event_user where event.e_address=? and event.eventid=event_user.eventid order by event_user.membercount DESC",
                        [u_address])
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
        # TODO: do above again with parent
        cur2 = g.db.execute("select parent from parenlist where child=?")
        pass

    for i in eventid:
        cur3 = g.db.execute("select * from event where eventid=?",[i])
        print cur3.fetchall()

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


if __name__ == '__main__':
    app.run()
