import os
import json
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from models import db, Annot
from config import Config, DBLogin
from datetime import datetime
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
load_dotenv() 

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DBLogin.USER}:{DBLogin.PSWD}@annotation_db:3306/labels'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Flask is running"

@app.route('/add_annot', methods=['POST'])
def add_annot():
    from models import User
    data = request.json
    if not User.query.filter_by(username=data["user"]).first():
        return jsonify({"error": "User not found"}), 403
    
    cmd = insert(Annot).values(
        sign=data['sign'],
        user=data["user"],
        label=data["label"],
        comments=data.get('comments', ""),
        time=datetime.fromtimestamp(data["time"] / 1000),
        video_path=os.path.basename(data["video_path"])
    ).on_duplicate_key_update(
        sign=data['sign'],
        label=data["label"],
        comments=data.get('comments', ""),
        time=datetime.fromtimestamp(data["time"] / 1000)
    )

    try:
        db.session.execute(cmd)
        db.session.commit()
        return jsonify({"message": "Added annotation"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to add annotation"}), 500
    
@app.route('/check_user', methods=['POST'])
def check_user():
    from models import db, User
    data = request.json
    username = data.get("username")
    print(username)
    user = db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar()

    if user:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})

@app.route('/batches/<string:username>', methods=["GET"])
def get_batches(username):
    from models import db, User
    user = db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar()
    user_dict = {k: v for k, v in vars(user).items() if k != "_sa_instance_state"}

    batches = {}

    with open("./batches/batches.json", 'r') as file:
        batches = json.load(file)

    user_batches = []

    for batch_num in user_dict["batches"]:
        batch_data = batches[f"batch_{batch_num}"]  # dict of {word: [clips]}
        words = list(batch_data.keys())  # collect all words
        
        user_batches.append({
            "batch": batch_num,
            "words": words
        })

    return jsonify(user_batches)


#Get list of clip titles from json batches file
#REQUIRES {batch_numer: INT, word: STRING}
@app.route('/batches/word/videos', methods=["POST"])
def get_word_videos():
    data = request.json
    batch = f"batch_{data.get("batch_number")}"
    word = data.get("word")

    batches = {}
    with open("./batches/batches.json", 'r') as file:
        batches = json.load(file)
    video_list = batches[batch][word]
    return jsonify({"videos": video_list})

@app.route('/batches/word/video', methods=["POST"])
def load_video():
    data = request.json
    video_title = data.get('video_title')
    participant = video_title.split("_")[0]
    video_path = os.path.join(os.getenv("VIDEO_DIRECTORY"), participant, video_title)
    print(video_path)

    try:
        return send_file(video_path, mimetype="video/mp4")
    except FileNotFoundError:
        return "Video not found", 404


if __name__ == '__main__':
    app.run(debug=True)
