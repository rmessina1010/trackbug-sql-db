from flask import Blueprint, jsonify, abort, request
from sqlalchemy import and_
from ..models import Skill, db

bp = Blueprint('skills', __name__, url_prefix='/skills')


@bp.route('', methods=['GET'])
def index():
    args = [('lev', 'lev'), ('name', 'skill_name'),
            ('id', 'skill_id'), ('tech', 'tech')]

    # comprehesion filters query string
    filters = [getattr(Skill, arg[1]) == request.args.get(
        arg[0]) for arg in args if request.args.get(arg[0]) is not None]

    try:
        skills = Skill.query.where(and_(*filters)).all()
        result = []
        for s in skills:
            result.append(s.serialize())
        return jsonify(result)
    except:
        return "invalid param!!"


@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    s = Skill.query.get_or_404(id)
    return jsonify(s.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    updatable_keys = ['skill_name', 'tech', 'lev']
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    try:
        db.session.query(Skill).where(Skill.skill_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/add', methods=['POST'])
def create():
    if 'skill_name' not in request.json:
        return abort(400)
    s = Skill(
        skill_name=request.json['skill_name'],
        tech=request.json['tech'],
        lev=request.json['lev']
    )
    db.session.add(s)
    db.session.commit()
    return jsonify(s.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    s = Skill.query.get_or_404(id)
    try:
        db.session.delete(s)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
