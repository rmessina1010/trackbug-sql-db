from flask import Blueprint, jsonify, abort, request
from sqlalchemy import and_
from ..models import Report, db

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('', methods=['GET'])
def index():
    args = [('sub', 'subject'), ('id', 'report_id'), ('on', 'reported_on'),
            ('bug', 'defined_as'), ('by', 'reported_by'), ('in', 'in_project')]

    # comprehesion filters query string
    filters = [getattr(Report, arg[1]) == (None if request.args.get(arg[0]) == '' else request.args.get(
        arg[0])) for arg in args if request.args.get(arg[0]) is not None]

    try:
        report = Report.query.where(and_(*filters)).all()
        result = []
        for r in report:
            result.append(r.serialize())
        return jsonify(result)
    except:
        return "invalid param!!"


@bp.route('/<int:id>', methods=['GET'])
def read(id: int):
    r = Report.query.get_or_404(id)
    return jsonify(r.serialize())


@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
    r = Report.query.get_or_404(id)
    updatable_keys = ['subject', 'description', 'in_project']
    updates = {key: request.json[key]
               for key in updatable_keys if key in request.json}
    try:
        db.session.query(Report).where(Report.report_id == id).update(
            updates, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('<int:id>/define', methods=['PUT'])
def define(id: int):
    if 'defined_as' not in request.json:
        return abort(400)
    Report.query.get_or_404(id)
    try:
        db.session.query(Report).where(Report.report_id == id).update(
            {"defined_as": request.json["defined_as"]}, synchronize_session=False)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('', methods=['POST'])
def create():
    if 'subject' not in request.json or 'in_project' not in request.json or 'reported_by' not in request.json:
        return abort(400)
    try:
        r = Report(
            reported_by=request.json['reported_by'],
            subject=request.json['subject'],
            description=request.json['description'],
            in_project=request.json['in_project']
        )
        db.session.add(r)
        db.session.commit()
        return jsonify(r.serialize())
    except:
        return "bad data!!!"


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    r = Report.query.get_or_404(id)
    try:
        db.session.delete(r)
        db.session.commit()
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)
