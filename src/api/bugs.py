from flask import Blueprint, jsonify, abort, request
from sqlalchemy import and_
from ..models import Bug, Project, db, bug_skills, Skill
import sqlalchemy

and_ = sqlalchemy.and_

bp = Blueprint('bugs', __name__, url_prefix='/bugs')


@bp.route('', methods=['GET'])
def index():
    args = [('stat', 'bug_status'), ('id', 'bug_id'), ('on', 'defined_on'),
            ('dev', 'assigned_to'), ('in', 'in_proj')]

    # comprehesion filters query string
    filters = [getattr(Bug, arg[1]) == request.args.get(
        arg[0]) for arg in args if request.args.get(arg[0]) is not None]

    try:
        bugs = Bug.query.where(and_(*filters)).all()
        result = []
        for b in bugs:
            result.append(b.serialize())
        return jsonify(result)
    except:
        return "invalid param!!"


@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    b = Bug.query.get_or_404(id)
    return jsonify(b.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    b = Bug.query.get_or_404(id)
    p = Project.query.get_or_404(b.in_proj)

    # only manager and dev can update bug
    allowed_users = [p.managed_by]
    if Bug.assigned_to is not None:
        allowed_users.append(b.assigned_to)
    if 'user_id' not in request.json or (request.json['user_id'] not in allowed_users):
        return "unauthorized!!!"
    updatable_keys = ['bug_title', 'bug_status', 'in_proj']
    # only manager can change who it's assigned to
    if request.json['user_id'] == p.managed_by:
        updatable_keys.append('assigned_to')
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    try:
        db.session.query(Bug).where(Bug.bug_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>/assign', methods=['PUT'])
def assign(id: int):
    b = Bug.query.get_or_404(id)
    p = Project.query.get_or_404(b.in_proj)
    if 'assigned_to' not in request.json or 'user_id' not in request.json or request.json['user_id'] != p.managed_by:
        return "unauthorized!!!"
    try:
        db.session.query(Bug).where(Bug.bug_id == id).update(
            {"assigned_to": request.json['assigned_to']}, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@ bp.route('', methods=['POST'])
def create():
    if 'user_id' not in request.json or 'bug_title' not in request.json or 'in_proj' not in request.json or 'bug_summary' not in request.json:
        return abort(400)
    p = Project.query.get_or_404(request.json['in_proj'])
    if p.managed_by != request.json['user_id']:
        return "Unauthorized!"
    try:
        b = Bug(
            bug_title=request.json['bug_title'],
            bug_status=request.json['bug_status'],
            bug_summary=request.json['bug_summary'],
            in_proj=request.json['in_proj'],
            assigned_to=request.json['assigned_to']
        )
        db.session.add(b)
        db.session.commit()
        return jsonify(b.serialize())
    except:
        return "bad data!!!"


@ bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    b = Bug.query.get_or_404(id)
    try:
        db.session.delete(b)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>/skills', methods=['POST'])
def add_skill(id: int):
    if 'skill_id' not in request.json:
        return abort(400)
    # if skill is already present,  return
    s = sqlalchemy.select(bug_skills).where(bug_skills.c.bug_id == id).where(
        bug_skills.c.skill_id == request.json['skill_id'])
    chk = db.session.query(s.exists()).scalar()
    if chk:
        return jsonify(True)
    # check user exists
    Bug.query.get_or_404(id)
    # check skill exists
    Skill.query.get_or_404(id)
    try:
        stmt = sqlalchemy.insert(bug_skills).values(
            bug_id=id, skill_id=request.json['skill_id'])
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>/skills', methods=['DELETE'])
def del_skill(id: int):
    if 'skill_id' not in request.json:
        return abort(400)
    # check bug exists
    Bug.query.get_or_404(id)
    # check skill exists
    Skill.query.get_or_404(id)
    try:
        stmt = sqlalchemy.delete(bug_skills).where(
            sqlalchemy.and_(
                bug_skills.c.bug_id == id,
                bug_skills.c.skill_id == request.json['skill_id']
            )
        )
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(None)


@bp.route('/<int:id>/skills', methods=['GET'])
def view_skills(id: int):
    b = Bug.query.get_or_404(id)
    skills = []
    for s in b.req_skill:
        skills.append(s.serialize())
    return jsonify(skills)
