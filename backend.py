# all the imports
import sqlite3
from flask import Flask, request, g, render_template, jsonify
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


@app.route('/profile')
def render_profile_page():
    return render_template('profile_bq.html')


@app.route('/addNewEvent')
def render_add_new_event_page():
    return render_template('addNewEvent.html')


@app.route('/all-events')
def load_all_events():
    # cur1 = g.db.execute('select name, artist, album, tags from tb_song')
    # all_songs = [dict(name=row[0], artist=row[1], album=row[2], tags=row[3]) for row in cur1.fetchall()]
    # for song in all_songs:
    #     song.tags = song.tags.split(",")
    all_events = [{
        'name': "DC wine hangout",
        'thumbnail': "static/img/1.jpg",
        'caption': "The wine Caption"
    }, {
        'name': "DC game hangout",
        'thumbnail': "static/img/2.jpg",
        'caption': "The game strings"
    }, {
        'name': "Maryland football meetup",
        'thumbnail': "static/img/3.jpg",
        'caption': "football YESSSS!"
    }, {
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
    return 'a'


@app.route('/currentUserInfo')
def get_current_user_info():
    currentUserInfo = {
        'userid': "100001userid",
        'password': "test password",
        'displayname': "test user displayname",
        'email_address': "huangbq.01@gmail.com",
        'location': "college park, MD",
        'age': "25",
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
        'facebook_url': "www.facebook.com/test-user-facebook",
        'twitter_url': "www.twitter.com/test-user-twitter"
    }
    return jsonify(currentUserInfo)


@app.route('/createNewEvent', methods=["POST"])
def create_new_event():
    item = json.loads(request.data)
    return 'a'


if __name__ == '__main__':
    app.run()
