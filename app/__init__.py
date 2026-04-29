import os
import json
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
load_dotenv()

# ── Database ────────────────────────────────────────────────────────────────
if os.getenv("TESTING") == "true":
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimelinePost(Model):
    name       = CharField()
    email      = CharField()
    content    = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

# ── App factory ─────────────────────────────────────────────────────────────
def create_app():
    app = Flask(__name__)

    mydb.connect()
    mydb.create_tables([TimelinePost])

    def load_json(*path_parts):
        full_path = os.path.join(app.root_path, "data", *path_parts)
        with open(full_path) as f:
            return json.load(f)

    # ── Routes ───────────────────────────────────────────────────────────────

    @app.route('/')
    def index():
        return render_template('index.html', title="Juan Pablo Morales",
                               url=os.getenv("URL"))

    @app.route('/hobbies')
    def hobbies():
        data = load_json("hobbies.json")
        return render_template('hobbies.html', title="My Hobbies",
                               url=os.getenv("URL"), hobbies=data["hobbies"])

    @app.route('/map')
    def map():
        return render_template('map.html', title="Places I've been to",
                               url=os.getenv("URL"))

    @app.route('/timeline')
    def timeline():
        return render_template('timeline.html', title="Timeline",
                               url=os.getenv("URL"))

    @app.route('/dev')
    def dev():
        return render_template(
            'dev/index.html',
            title="JP · Dev",
            url=os.getenv("URL"),
            projects=load_json("dev", "projects.json"),
            stack=load_json("dev", "stack.json")
        )

    @app.route('/sec')
    def sec():
        return render_template(
            'sec/index.html',
            title="JP · Sec",
            url=os.getenv("URL"),
            projects=load_json("sec", "projects.json"),
            certs=load_json("sec", "certs.json"),
            tools=load_json("sec", "tools.json"),
            writeups=load_json("sec", "writeups.json"),
            blog_posts=load_json("sec", "blog_posts.json")
        )

    # ── Timeline API ─────────────────────────────────────────────────────────

    @app.route('/api/timeline_post', methods=['POST'])
    def post_timelinePost():
        name    = request.form['name']
        email   = request.form['email']
        content = request.form['content']
        if not name:
            return "Invalid name", 400
        if '@' not in email:
            return "Invalid email", 400
        if not content:
            return "Invalid content", 400
        post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(post)

    @app.route('/api/timeline_post', methods=['GET'])
    def get_timelinePost():
        return {
            'timeline_posts': [
                model_to_dict(p)
                for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }

    @app.route('/api/timeline_post/<int:id>', methods=['DELETE'])
    def delete_timelinePost(id):
        try:
            post = TimelinePost.get(TimelinePost.id == id)
            post.delete_instance()
            return {'status': 'success', 'message': 'Post deleted successfully'}
        except TimelinePost.DoesNotExist:
            return {'status': 'error', 'message': 'Post not found'}, 404

    return app

# ── Module-level app instance (used by Flask CLI and tests) ──────────────────
app = create_app()
