from flask import Blueprint, jsonify, abort, request
from sqlalchemy import and_
from ..models import Tech, db

bp = Blueprint('techs', __name__, url_prefix='/tech')


@bp.route('', methods=['GET'])
def index():
    args = [('name', 'tech_name'), ('id', 'tech_id')]

    # comprehesion filters query string
    filters = [getattr(Tech, arg[1]) == request.args.get(
        arg[0]) for arg in args if request.args.get(arg[0]) is not None]

    try:
        tech = Tech.query.where(and_(*filters)).all()
        result = []
        for t in tech:
            result.append(t.serialize())
        return jsonify(result)
    except:
        return "invalid param!!"


@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    t = Tech.query.get_or_404(id)
    return jsonify(t.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    updatable_keys = ['tech_name']
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    try:
        db.session.query(Tech).where(Tech.tech_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/add', methods=['POST'])
def create():
    if 'tech_name' not in request.json:
        return abort(400)
    try:
        t = Tech(
            tech_name=request.json['tech_name'],
        )
        db.session.add(t)
        db.session.commit()
        return jsonify(t.serialize())
    except:
        return "bad data!!!"


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    t = Tech.query.get_or_404(id)
    try:
        db.session.delete(t)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
