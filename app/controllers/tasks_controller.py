from flask import request, jsonify, session
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from app.configs.database import db
from app.models.tasks_model import Task
from app.models.tasks_categories_model import Task_Category
from app.models.category_model import Category

eisenhower_list = [None, [None, ["Do It First", 1], ["Schedule It", 3]], [None, ["Delegate It", 2], ["Delete It", 4]]]

def post_task():
    data = request.get_json()

    session: Session = db.session()

    categories = data.pop("categories")

    classification = ""

    if "name" not in data.keys():
        return {'error': 'name key missing'}, HTTPStatus.BAD_REQUEST

    for category in categories:
        record = session.query(Category).filter(Category.name  == category).first()
        if record == None:
            return {'error': f'category {category} does not exist'}, HTTPStatus.BAD_REQUEST

    if data["importance"] > 2 or data["urgency"] > 2:
        return {'error': {'valid_options': {'importance': [1, 2], 'urgency': [1, 2]}, 'recieved_options': {'importance': data["importance"], 'urgency': data["urgency"]}}}, HTTPStatus.BAD_REQUEST

    data["eisenhower_id"] = eisenhower_list[data["importance"]][data["urgency"]][1]
    classification = eisenhower_list[data["importance"]][data["urgency"]][0]

    task_info = Task(**data)

    session.add(task_info)

    try:
        session.commit()
    except IntegrityError:
        return {'error': 'name already exists'}, HTTPStatus.CONFLICT


    for category in categories:
        info = {"task_id": task_info.task_id}
        record = session.query(Category).filter(Category.name  == category).first()
        info["category_id"] = record.category_id

        task_category_info = Task_Category(**info)

        session.add(task_category_info)

        session.commit()

    data["categories"] = categories

    data["task_id"] = task_info.task_id

    data["classification"] = classification

    data.pop("importance")
    data.pop("urgency")
    data.pop("eisenhower_id")

    return data, HTTPStatus.OK

def patch_task(task_id):
    
    session: Session = db.session()

    record = session.query(Task).get(task_id)

    data = request.get_json()

    if record:

        dict_record = record.__dict__

        name = dict_record["name"]
        description = dict_record["description"]
        duration = dict_record["duration"]
        record_task_id = dict_record["task_id"]

        classification = ""
        data_categories = []
        record_categories = []

        if "categories" in data.keys():
            data_categories = data.pop("categories")

        if "importance" in data.keys() and "urgency" in data.keys():
            if data["importance"] > 2 or data["urgency"] > 2 or data["importance"] < 1 or data["urgency"] < 1:
                return {'error': {'valid_options': {'importance': [1, 2], 'urgency': [1, 2]}, 'recieved_options': {'importance': data["importance"], 'urgency': data["urgency"]}}}, HTTPStatus.BAD_REQUEST

            data["eisenhower_id"] = eisenhower_list[data["importance"]][data["urgency"]][1]
            classification = eisenhower_list[data["importance"]][data["urgency"]][0]
        
        if "importance" in data.keys() and "urgency" not in data.keys():
            if data["importance"] > 2 or data["importance"] < 1:
                return {'error': {'valid_options': {'importance': [1, 2]}, 'recieved_options': {'importance': data["importance"]}}}, HTTPStatus.BAD_REQUEST
            
            data["eisenhower_id"] = eisenhower_list[data["importance"]][dict_record["urgency"]][1]
            classification = eisenhower_list[data["importance"]][dict_record["urgency"]][0]
            data["urgency"] = dict_record["urgency"]

        if "urgency" in data.keys() and "importance" not in data.keys():
            if data["urgency"] > 2 or data["urgency"] < 1:
                return {'error': {'valid_options': {'urgency': [1, 2]}, 'recieved_options': {'urgency': data["urgency"]}}}, HTTPStatus.BAD_REQUEST
            
            data["eisenhower_id"] = eisenhower_list[dict_record["importance"]][data["urgency"]][1]
            classification = eisenhower_list[dict_record["importance"]][data["urgency"]][0]
            data["importance"] = dict_record["importance"]

        task_categories_record = session.query(Task_Category).filter(Task_Category.task_id  == task_id).all()

        if task_categories_record:
            for category in task_categories_record:
                category_record = session.query(Category).get(category.category_id)
                record_categories.append(category_record.name)

        if data_categories:
            for category in data_categories:
                if category not in record_categories:
                    info = {"task_id": dict_record["task_id"]}
                    category_record = session.query(Category).filter(Category.name  == category).first()

                    try:
                        info["category_id"] = category_record.category_id
                    except AttributeError:
                        return {'error': f'category {category} does not exist'}, HTTPStatus.NOT_FOUND

                    task_category_info = Task_Category(**info)

                    session.add(task_category_info)

                    session.commit()

        for category in record_categories:
            if category not in data_categories:
                data_categories.append(category)

    
        for item in data.items():
            setattr(record, item[0], item[1])

        session.commit()

        
        if "name" not in data.keys():
            data["name"] = name
        if "description" not in data.keys():
            data["description"] = description
        if "duration" not in data.keys():
            data["duration"] = duration

        if data_categories:
            data["categories"] = data_categories

        data["classification"] = classification
        data["task_id"] = record_task_id

        data.pop("importance")
        data.pop("urgency")
        data.pop("eisenhower_id")

        return data, HTTPStatus.OK
    else:
        return {'error': 'task does not exist'}, HTTPStatus.NOT_FOUND

def delete_task(task_id):
    session: Session = db.session()

    record = session.query(Task).get(task_id)

    task_category_record = session.query(Task_Category).filter(Task_Category.task_id  == task_id).all()

    if record:

        for category in task_category_record:
            session.delete(category)

        session.delete(record)

        session.commit()

        return "", HTTPStatus.NO_CONTENT
    else:
        return {'error': "id doesn't exist"}, HTTPStatus.NOT_FOUND