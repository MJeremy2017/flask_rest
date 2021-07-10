from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    likes = db.Column(db.Integer, unique=False, nullable=False)
    views = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"id={self.id} | name={self.name} | likes={self.likes} | views={self.views}"


db.create_all()

"""
video struct
{
    vid_id: {
        name: str
        likes: int
        views: int
    }
}
"""
vid_parser = reqparse.RequestParser()
vid_parser.add_argument("name", type=str, help="name of the video")
vid_parser.add_argument("likes", type=int, help="likes of the video")
vid_parser.add_argument("views", type=int, help="views of the video")

vid_fields = {
    "id": fields.String,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    @marshal_with(vid_fields, envelope="data")
    def get(self, vid_id):
        result = VideoModel.query.filter_by(id=vid_id).first_or_404(description="video id not exists")
        return result, 200

    @marshal_with(vid_fields, envelope="data")
    def put(self, vid_id):
        result = VideoModel.query.filter_by(id=vid_id).first()
        if result:
            abort(401, error="video id already exists!")
        args = vid_parser.parse_args()
        video = VideoModel(id=vid_id, name=args['name'], likes=args['likes'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    def delete(self, vid_id):
        result = VideoModel.query.filter_by(id=vid_id).first()
        if not result:
            abort(404, error="video id not found!")

        db.session.delete(result)
        db.session.commit()
        return {"data": f"{vid_id} deleted"}, 204


api.add_resource(Video, "/video/<string:vid_id>")

if __name__ == '__main__':
    app.run(debug=True)
