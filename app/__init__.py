import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
import datetime
from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField
from playhouse.shortcuts import model_to_dict
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

              
@app.route('/')
def index():
    json_path_edu = os.path.join(app.root_path,"data", "education.json")
    json_path_exp = os.path.join(app.root_path,"data", "experience.json")
    with open(json_path_exp) as f:
        experience = json.load(f)
    with open(json_path_edu) as f:
        education = json.load(f)
    return render_template('index.html', title="Juan Pablo Morales", url=os.getenv("URL"), education=education, experience=experience)

@app.route('/hobbies')
def hobbies():
    json_path = os.path.join(app.root_path, "data", "hobbies.json")
    with open(json_path) as f:
        hobbies_data = json.load(f)
    return render_template('hobbies.html', title="My Hobbies", url=os.getenv("URL"), hobbies=hobbies_data["hobbies"])

@app.route('/map')
def map():
    return render_template('map.html', title="Places I've been to", url=os.getenv("URL"))


@app.route('/api/timeline_post', methods=['POST'])
def post_timelinePost():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_timelinePost():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in 
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

if __name__ == "__main__":
    print(f"Server up. \n MySQL running:{mydb}")