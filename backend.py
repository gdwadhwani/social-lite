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
def load_index():
    return render_template('index.html')


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

# @app.route('/UpdateSongs', methods=["POST"])
# def update_songs():
#     answer_str = str(request.json)
#     content = request.json["fridge"]
#     g.db.execute('delete * from tb_song')
#     g.db.execute('insert into fridges (answer) values (?)', [answer_str])
#     g.db.commit()
#     f_id = query_db('select id from fridges order by id desc')[0][0]
#     for con in content:
#         g.db.execute('insert into contents (fridge_id, fruit_name, fruit_amount) values (?,?,?)', [f_id, con, content[con]])
#     g.db.commit()
#     return "success"


if __name__ == '__main__':
    app.run()
