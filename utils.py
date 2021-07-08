from flask_restful import abort


def video_non_exist_call_back(videos, vid_id):
    if vid_id not in videos:
        abort(404, error="video id not exists!")


def video_exist_call_back(videos, vid_id):
    if vid_id in videos:
        abort(401, error="video already exists!")