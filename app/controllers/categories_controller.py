from http import HTTPStatus
from flask import jsonify, request
from app.configs.database import db
from app.exceptions.keys_exceptions import MissingKeys
from app.package.keys_services import validate_keys
from app.models.categories_model import CategoriesModel
from sqlalchemy.exc import IntegrityError, NoResultFound

def create_category():

    expected_keys = CategoriesModel.keys
    category_data = request.get_json()

    try:
        validate_keys(category_data, expected_keys)
        category = CategoriesModel(**category_data)

        db.session.add(category)
        db.session.commit()

        return jsonify(category), HTTPStatus.OK

    except KeyError as e:
        e.args[0], HTTPStatus.BAD_REQUEST

    except MissingKeys as e:
        e.args[0], HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"error": "Category already exists"}, HTTPStatus.CONFLICT


def update_category(id):
    
    category_data = request.get_json()

    try:
        data_to_update = CategoriesModel.query.filter_by(id=id).first()

        for key, value in category_data.items():
            setattr(data_to_update, key, value)

        db.session.commit()

        return jsonify(category_data), HTTPStatus.OK

    except NoResultFound:
        return {"error": "Category not found"}, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {"error": "Category already exists"}, HTTPStatus.CONFLICT

def delete_category(id):
    try: 
        data_to_delete = CategoriesModel.query.filter_by(id=id).first()
        
        db.session.delete(data_to_delete)
        db.session.commit()

        return "", HTTPStatus.OK

    except NoResultFound:
        return {"error": "Id not found"}, HTTPStatus.BAD_REQUEST