from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """returns all pictures """
    if data:
        return jsonify(data), 200
    
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """returns a picture by its id"""
    if data:
        elements = list(filter(lambda item: item['id'] == id, data))
        if not elements:
            return {"Message": "picture not found"}, 404

        return jsonify(elements[0]), 200

    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Adds a new picture"""
    payload = request.get_json()
    if not payload or 'pic_url' not in payload:
        return {"Message": "Missing 'pic_url' in the request"}, 400
    
    if data:
        exists = list(filter(lambda item: item['id'] == payload['id'], data))
        if exists:
            return {"Message": f"picture with id {payload['id']} already present"}, 302

        data.append(payload)
        return jsonify(payload), 201
    
    return {"message": "Internal server error"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates a new picture"""
    payload = request.get_json()
    if not payload or 'pic_url' not in payload:
        return {"Message": "Missing 'pic_url' in the request"}, 400

    if data:
        exists = None
        for i, picture in enumerate(data):
            if picture['id'] == id:
                exists = i

        if not exists:
            return {"message": "picture not found"}, 404

        data[exists] = payload
        return jsonify(data[exists]), 200

    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """deletes a picture by its id"""
    if data:
        exists = None
        for i, picture in enumerate(data):
            if picture['id'] == id:
                print(f"Just one {i}")
                exists = i
                break

        if exists == None:
            return {"message": "picture not found"}, 404
        
        data.pop(exists)
        return "", 204

    return {"message": "Internal server error"}, 500    
