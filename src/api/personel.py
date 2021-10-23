from flask import Blueprint, jsonify, abort, request
from sqlalchemy import and_
from ..models import Personel, db

bp = Blueprint('personel', __name__, url_prefix='/personel')


@bp.route('', methods=['GET'])
def index():
    args = [('fn', 'first_name'), ('id', 'person_id'),
            ('ln', 'last_name'), ('mng', 'reports_to'),
            ('stat', 'work_stat'), ('role', 'p_role'),
            ('age', 'age'), ('sex', 'sex')]

    # comprehesion filters query string
    filters = [getattr(Personel, arg[1]) == (None if request.args.get(arg[0]) == '' else request.args.get(
        arg[0])) for arg in args if request.args.get(arg[0]) is not None]

    try:
        pers = Personel.query.where(and_(*filters)).all()
        result = []
        for p in pers:
            result.append(p.serialize())
        return jsonify(result)
    except:
        return "invalid param!!"


@ bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    p = Personel.query.get_or_404(id)
    return jsonify(p.serialize())


@ bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    updatable_keys = ['first_name', 'last_name',
                      'reports_to', 'p_role', 'work_stat', 'age', 'sex']
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    try:
        db.session.query(Personel).where(Personel.person_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@ bp.route('', methods=['POST'])
def create():
    if 'first_name' not in request.json or 'last_name' not in request.json:
        return abort(400)
    try:
        p = Personel(
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            p_role=request.json['p_role'],
            work_stat=request.json['work_stat'],
            reports_to=request.json['reports_to'],
            age=request.json['age'],
            sex=request.json['sex']
        )
        db.session.add(p)
        db.session.commit()
        return jsonify(p.serialize())
    except:
        return "bad data!!!"


@ bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Personel.query.get_or_404(id)
    try:
        db.session.delete(p)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
