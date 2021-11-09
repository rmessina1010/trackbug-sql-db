from flask import Blueprint, jsonify, abort, request
from sqlalchemy import and_, sql
from ..models import Project, Bug, Personel, db

bp = Blueprint('projects', __name__, url_prefix='/projects')


@bp.route('', methods=['GET'])
def index():
    args = [('name', 'proj_title'), ('id', 'project_id'),
            ('stat', 'proj_status'), ('mng', 'managed_by')]

    # comprehesion filters query string
    filters = [getattr(Project, arg[1]) == (None if request.args.get(arg[0]) == '' else request.args.get(
        arg[0])) for arg in args if request.args.get(arg[0]) is not None]

    try:
        proj = Project.query.where(and_(*filters)).all()
        result = []
        for p in proj:
            result.append(p.serialize())
        return jsonify(result)
    except:
        return "invalid param!!"


@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    p = Project.query.get_or_404(id)
    return jsonify(p.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    p = Project.query.get_or_404(id)
    if 'user_id' not in request.json or request.json['user_id'] != p.managed_by:
        return "unauthorized!!!"
    updatable_keys = ['proj_title', 'proj_status',
                      'managed_by', 'proj_excerpt']
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    try:
        db.session.query(Project).where(Project.proj_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('', methods=['POST'])
def create():
    if 'proj_title' not in request.json:
        return abort(400)
    try:
        p = Project(
            proj_title=request.json['proj_title'],
            proj_status=request.json['proj_status'],
            proj_excerpt=request.json['proj_excerpt'],
            managed_by=request.json['managed_by']
        )
        db.session.add(p)
        db.session.commit()
        return jsonify(p.serialize())
    except:
        return "bad data!!!"


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Project.query.get_or_404(id)
    if 'user_id' not in request.json or request.json['user_id'] != p.managed_by:
        return "unauthorized!!!"
    try:
        db.session.delete(p)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>/staff', methods=['GET'])
def staff(id: int):
    prj = Project.query.get_or_404(id)

    staff_qry = sql.select(Bug.assigned_to).where(
        Bug.in_proj == id)
    s = db.session.query(Personel).filter(
        Personel.person_id.in_(staff_qry))
    m = Personel.query.get(prj.managed_by)

    manager = m.serialize() if m else None
    staff = []
    for p in s:
        staff.append({'dev_id': p.person_id,
                     'first_name': p.first_name,
                      'last_name': p.last_name,
                      'sex': p.sex,
                      'work_stat': p.work_stat,
                      'p_role': p.p_role
                      })

    return jsonify({'manager': manager,  'staff': staff})
