# all the imports
import sqlite3
from flask import *
from contextlib import closing
import json

# configuration
DATABASE = 'a4.db'
DEBUG = True
SECRET_KEY = 'development key'


app = Flask(__name__)
app.config.from_object(__name__)


# db methods
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()
    # init_db()
    # remember to do init_db() when first time running

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def render_index_page():
    return render_template('index.html')
    # return redirect('/profile')


@app.route('/profile')
def render_profile_page():
    return render_template('profile_bq.html')


@app.route('/addNewEvent')
def render_add_new_event_page():
    return render_template('addNewEvent.html')


@app.route('/eventDetail', methods=["GET", "POST"])
def gotoEventDetail():
    item = request.data
    if len(item) > 0:
        session['detaileventid'] = item
    return render_template('eventDetail.html')


@app.route('/account_index')
def render_account_index():
    return render_template('account_index.html')


@app.route('/getEventDetail', methods=["GET"])
def getEventDetail():
    item = {
        'eventid': 'abc',
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
    }
    return json.dumps(item)


@app.route('/all-events')
def load_all_events():
    # cur1 = g.db.execute('select name, artist, album, tags from tb_song')
    # all_songs = [dict(name=row[0], artist=row[1], album=row[2], tags=row[3]) for row in cur1.fetchall()]
    # for song in all_songs:
    #     song.tags = song.tags.split(",")
    all_events = [{
        'eventid': 123,
        'title': "DC wine hangout",
        'thumbnail': "static/img/1.jpg",
        'caption': "The wine Caption"
    }, {
        'eventid': 124,
        'name': "DC game hangout",
        'thumbnail': "static/img/2.jpg",
        'caption': "The game strings"
    }, {
        'eventid': 125,
        'name': "Maryland football meetup",
        'thumbnail': "static/img/3.jpg",
        'caption': "football YESSSS!"
    }, {
        'eventid': 126,
        'name': "Maryland basketball meetup",
        'thumbnail': "static/img/4.jpg",
        'caption': "GET A DUNK!"
    }]
    return json.dumps(all_events)


@app.route('/all-interests')
def load_all_interests():
    all_interests = [{
        'name': "Art",
        'parent': "Arts & Entertainment"
    }, {
        'name': "Fiction",
        'parent': "Arts & Entertainment"
    }, {
        'name': "Film",
        'parent': "Arts & Entertainment"
    }, {
        'name': "Lean Startup",
        'parent': "Business & Career"
    }, {
        'name': "Marketing",
        'parent': "Business & Career"
    }, {
        'name': "Investing",
        'parent': "Business & Career"
    }, {
        'name': "Social Media",
        'parent': "Internet & Technology"
    }, {
        'name': "Interaction Design",
        'parent': "Internet & Technology"
    }, {
        'name': "Cloud Computing",
        'parent': "Internet & Technology"
    }]
    return json.dumps(all_interests)


@app.route('/updateCurrentUser', methods=["POST"])
def update_current_user():
    item = json.loads(request.data)
    return 'Success'


@app.route('/currentUserInfo')
def get_current_user_info():
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
        'interests': ["Evolution"],
        'facebook_url': "www.facebook.com/test-user-facebook",
        'twitter_url': "www.twitter.com/test-user-twitter"
    }
    # currentUserInfo = {}

    # item = session['username']
    return json.dumps(currentUserInfo)


@app.route('/createNewEvent', methods=["POST"])
def create_new_event():
    item = json.loads(request.data)
    return 'Success!'


@app.route('/rsvpEvent', methods=["POST"])
def rsvpEvent():
    item = request.data
    return 'Success!'


@app.route('/getReco')
def get_reco():
    item = [{
        'title': 'test event name',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': ['test cate 1', 'test cate 2', 'test cate 3'],
        'tag': ['tag a', 'tag b'],
        'creator': 'username of creator',
        'member': ['attender 1 username', 'attender 2 username'],
        'member_count': '2'
    }, {
        'title': 'test event name',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': ['test cate 1', 'test cate 2', 'test cate 3'],
        'tag': ['tag a', 'tag b'],
        'creator': 'username of creator',
        'member': ['attender 1 username', 'attender 2 username'],
        'member_count': '2'
    }]
    return json.dumps(item)


@app.route('/getRsvpedEvent')
def get_rsvped_event():
    item = [{
        'title': 'test event name',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': ['test cate 1', 'test cate 2', 'test cate 3'],
        'tag': ['tag a', 'tag b'],
        'creator': 'username of creator',
        'member': ['attender 1 username', 'attender 2 username'],
        'member_count': '2'
    }, {
        'title': 'test event name',
        'detail': 'detail description',
        'address': 'test location',
        'city': 'test city',
        'state': 'test state',
        'date': 'test date',
        'thumbnail': 'username.png',
        'category': ['test cate 1', 'test cate 2', 'test cate 3'],
        'tag': ['tag a', 'tag b'],
        'creator': 'username of creator',
        'member': ['attender 1 username', 'attender 2 username'],
        'member_count': '2'
    }]
    return json.dumps(item)


@app.route('/checkUser')
def check_user():
    # session['username'] ='adf'
    if len(str(session['username'])) > 0:
        return str(session['username'])
    else:
        return ''


@app.route('/login', methods=["GET", "POST"])
def login():
    item = request.data
    session['username'] = item.username
    return "success"


@app.route('/logout', methods=["GET", "POST"])
def logout():
    return "success"


@app.route('/signup', methods=["GET", "POST"])
def signup():
    item = request.data
    return "success"


@app.route('/getDiscussion', methods=["GET", "POST"])
def get_discussion():
    item = [{'title': 'This is the title',
             'creator': 'The creator',
             'content': 'the content of the post'}]
    return json.dumps(item)


@app.route('/newPost', methods=["GET", "POST"])
def post_new():
    item = request.data
    return 'success'


if __name__ == '__main__':
    app.run()
