from http import HTTPStatus
from flask import jsonify
from sqlalchemy.orm.session import Session
from app.configs.database import db
from app.models.eisenhower_model import Eisenhower
from app.models.tasks_model import Task
from app.models.tasks_categories_model import Task_Category
from app.models.category_model import Category


def tasks_categories_get():

    session: Session = db.session()

    json_list = []

    categories = Task_Category.query.all()

    for tasks_category in categories:
        category = session.query(Category).get(tasks_category.category_id).__dict__
        category.pop("_sa_instance_state")
        category["tasks"] = []
        task = session.query(Task).get(tasks_category.task_id).__dict__
        task.pop("_sa_instance_state")
        task.pop("urgency")
        task.pop("importance")
        eisenhower = task.pop("eisenhower_id")

        classification = session.query(Eisenhower).get(eisenhower).__dict__["type"]

        task["classification"] = classification

        name_check = True

        for item_category in json_list:
            if item_category["name"] == category["name"]:
                name_check = False
                item_category["tasks"].append(task)

        if name_check:
            category["tasks"].append(task)
            json_list.append(category)


    return jsonify(json_list), HTTPStatus.OK