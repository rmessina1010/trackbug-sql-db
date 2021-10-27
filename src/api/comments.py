from flask import Blueprint, jsonify, abort, request
from sqlalchemy import and_
from ..models import Comment, db

bp = Blueprint('comments', __name__, url_prefix='/comments')


@bp.route('', methods=['GET'])
def index():
    args = [('by', 'comm_author'), ('id', 'comment_id'),
            ('abt', 'refers_to'), ('on', 'comm_date')]

    # comprehesion filters query string
    filters = [getattr(Comment, arg[1]) == (None if request.args.get(arg[0]) == '' else request.args.get(
        arg[0])) for arg in args if request.args.get(arg[0]) is not None]

    try:
        comms = Comment.query.where(and_(*filters)).all()
        result = []
        for c in comms:
            result.append(c.serialize())
        return jsonify(result)
    except:
        return "invalid param!!"


@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    c = Comment.query.get_or_404(id)
    return jsonify(c.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    c = Comment.query.get_or_404(id)
    if 'user_id' not in request.json or request.json['user_id'] != c.comm_author:
        return "unauthorized!!!"
    updatable_keys = ['text', 'refers_to']
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    try:
        db.session.query(Comment).where(Comment.comment_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@ bp.route('', methods=['POST'])
def create():
    if 'user_id' not in request.json or 'text' not in request.json or 'refers_to' not in request.json:
        return abort(400)
    try:
        c = Comment(
            text=request.json['text'],
            comm_author=request.json['user_id'],
            refers_to=request.json['refers_to'],
        )
        db.session.add(c)
        db.session.commit()
        return jsonify(c.serialize())
    except:
        return "bad data!!!"


@ bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    c = Comment.query.get_or_404(id)
    try:
        db.session.delete(c)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
