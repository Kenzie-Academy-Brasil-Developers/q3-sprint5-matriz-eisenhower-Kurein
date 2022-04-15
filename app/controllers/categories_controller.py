from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from app.configs.database import db
from app.models.category_model import Category
from sqlalchemy.exc import IntegrityError

def post_category():

    try:
        data = request.get_json()

        data["name"] = data["name"].title()

        category_info = Category(**data)

        session: Session = db.session()

        session.add(category_info)

        session.commit()

        return jsonify(category_info), HTTPStatus.CREATED
    except IntegrityError:
        return {'error': 'name already exists'}, HTTPStatus.CONFLICT
    except KeyError:
        return {'error': 'name key missing'}, HTTPStatus.BAD_REQUEST

def patch_category(category_id):
    data = request.get_json()

    session: Session = db.session()

    record = session.query(Category).get(category_id)

    if record:
        for item in data.items():
            setattr(record, item[0], item[1])

        session.commit()    

        return jsonify(record), HTTPStatus.OK
    else:
        return {'error': "id doesn't exist"}, HTTPStatus.NOT_FOUND

def delete_category(category_id):
    
    session: Session = db.session()

    record = session.query(Category).get(category_id)

    if record:
        session.delete(record)

        session.commit()    

        return "", HTTPStatus.NO_CONTENT
    else:
        return {'error': "id doesn't exist"}, HTTPStatus.NOT_FOUND