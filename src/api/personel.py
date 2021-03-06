from flask import Blueprint, jsonify, abort, request
import sqlalchemy
from sqlalchemy.sql.expression import true
from ..models import Personel, db, dev_skills, Skill
import sqlalchemy
from sqlalchemy import text

import hashlib
import secrets


def scramble(password: str, salt):
    """Hash and salt the given password"""
    if salt == True:
        salt = secrets.token_hex(16)
    return (hashlib.sha512((password + salt).encode('utf-8')).hexdigest(), salt)


def pass_check(upass: str, bdpass: str, salt: str):
    passdata = scramble(upass, salt)
    if bdpass == passdata[0]:
        return True
    return False


and_ = sqlalchemy.and_

bp = Blueprint('personel', __name__, url_prefix='/personel')

loadSELECTtxt = 'WITH loadsTable AS (SELECT COUNT(*) as tasks, CAST(AVG(bug_weight) AS DECIMAL(4, 3)), SUM(bug_weight) as load, assigned_to as dev FROM bugs'
loadGROUPtxt = ' group by assigned_to) SELECT tasks, avg, load, dev, first_name, last_name, reports_to, p_role, work_stat, email FROM loadsTable LEFT JOIN personel ON personel.person_id=loadsTable.dev'


@bp.route('', methods=['GET'])
def index():
    args = [('fn', 'first_name'), ('id', 'person_id'),
            ('ln', 'last_name'), ('mng', 'reports_to'),
            ('stat', 'work_stat'), ('role', 'p_role'),
            ('age', 'age'), ('sex', 'sex'), ('email', 'email')]

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
    updatable_keys = ['first_name', 'last_name', 'email',
                      'reports_to', 'p_role', 'work_stat', 'age', 'sex']
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    if 'password' in request.json:
        updates['password'], updates['nacl'] = scramble(
            request.json['password'], True)
    try:
        db.session.query(Personel).where(Personel.person_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@ bp.route('', methods=['POST'])
def create():
    if 'first_name' not in request.json or 'last_name' not in request.json or 'email' not in request.json or 'password' not in request.json:
        return abort(400)
    try:
        hashed, salt = scramble(request.json['password'], True)
        p = Personel(
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            p_role=request.json['p_role'],
            work_stat=request.json['work_stat'],
            reports_to=request.json['reports_to'],
            age=request.json['age'],
            sex=request.json['sex'],
            email=request.json['email'],
            password=hashed,
            nacl=salt
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


@bp.route('/<int:id>/skills', methods=['POST'])
def add_skill(id: int):
    if 'skill_id' not in request.json:
        return abort(400)
    # if skill is already present,  return
    s = sqlalchemy.select(dev_skills).where(dev_skills.c.person_id == id).where(
        dev_skills.c.skill_id == request.json['skill_id'])
    chk = db.session.query(s.exists()).scalar()
    if chk:
        return jsonify(True)
    # check person exists
    Personel.query.get_or_404(id)
    # check skill exists
    Skill.query.get_or_404(request.json['skill_id'])
    try:
        stmt = sqlalchemy.insert(dev_skills).values(
            person_id=id, skill_id=request.json['skill_id'])
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>/skills', methods=['DELETE'])
def del_skill(id: int):
    if 'skill_id' not in request.json:
        return abort(400)
    # check person exists
    Personel.query.get_or_404(id)
    # check bug exists
    Skill.query.get_or_404(request.json['skill_id'])
    try:
        stmt = sqlalchemy.delete(dev_skills).where(
            sqlalchemy.and_(
                dev_skills.c.person_id == id,
                dev_skills.c.skill_id == request.json['skill_id']
            )
        )
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(None)


@bp.route('/<int:id>/skills', methods=['GET'])
def view_skills(id: int):
    p = Personel.query.get_or_404(id)
    skills = []
    for s in p.skilled_in:
        skills.append(s.serialize())
    return jsonify(skills)


def load_query(where: str):
    sql = text(loadSELECTtxt+loadGROUPtxt+where)
    result = db.engine.execute(sql)
    load = [{'load': row['load'],
             'tasks':row['tasks'],
             'dev_id':row['dev'],
             'first_name':row['first_name'],
             'last_name':row['last_name'],
             'reports_to':row['reports_to'],
             'p_role':row['p_role'],
             'work_stat':row['work_stat'],
             'email':row['email']
             }for row in result]
    return load


def operator_for(qry_arg: str):
    if qry_arg.endswith('_lt'):
        return ' < '
    if qry_arg.endswith('_gt'):
        return ' > '
    return ' = '


@ bp.route('/load/<int:id>', methods=['GET'])
def load_id(id):
    where = ' WHERE dev ' + (' = '+str(id)+' ' if id else ' IS NULL ')
    load = load_query(where)
    return jsonify(load)


@ bp.route('/load', methods=['GET'])
def load():
    where = ''
    if request.args:
        args = [('id', 'dev'), ('mng', 'reports_to'), ('stat', 'work_stat', 1), ('role', 'p_role', 1), ('email', 'email', 1), ('load', 'load'),
                ('tasks', 'tasks'), ('load_lt', 'load'), ('tasks_lt', 'tasks'), ('load_gt', 'load'), ('tasks_gt', 'tasks')]
        where = ' WHERE TRUE ' + \
            ' '.join([' AND ' + arg[1] + (operator_for(arg[0]) + (request.args.get(arg[0]) if len(arg) < 3 else "'" + request.args.get(arg[0]) + "'") if request.args.get(arg[0]) != '' else ' IS NULL ')
                     for arg in args if (request.args.get(arg[0]) is not None)])
    load = load_query(where)
    return jsonify(load)


@ bp.route('/sim/login', methods=['POST'])
def login():
    if 'password' not in request.json or 'email' not in request.json:
        return jsonify(None)
    p = Personel.query.filter(
        getattr(Personel, 'email') == request.json['email']).one()
    if p:
        if jsonify(pass_check(request.json['password'], p.password, p.nacl)):
            return jsonify(p.serialize())
    return jsonify(False)
