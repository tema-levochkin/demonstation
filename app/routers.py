from flask import Response, jsonify, request

from app import app
from app.services import UserService


user_service = UserService()


@app.route("/user/create", methods=["POST"])
def create_user(username: str, email: str) -> Response: 
    user_service.create(username, email)
    return Response("success", status=200)


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Response: 
    user = user_service.get_user_from_id(id=user_id)
    if not user:
        return Response("user not found", status=404) 
    return jsonify({
        "username": user.username, 
        "email": user.email, 
        "registraion_date": user.registration_date
    })


@app.route("/user/update/<int:user_id>", methods=["PATCH"])
def update_user(user_id: int, **updated_data) -> Response:
    user = user_service.get_user_from_id(id=user_id)
    if not user:
        return Response("user not found", status=404) 
    update_status = user_service.update(user, updated_data)
    if not update_status: 
        return Response("not valid data for update", status=400)
    return Response("user data successfully updated", status=200)    
    

@app.route("/user/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> Response: 
    user = user_service.get_user_from_id(id=user_id)
    if not user:
        return Response("user not found", status=404) 
    user_service.delete(user)
    return Response("user was delete", status=200) 


from marshmallow import Schema, fields
class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    registration_date = fields.DateTime()


@app.route("/user/list", methods=["GET"])
def get_list_users(): 
    page = request.args.get("page", 0)
    users_on_page = user_service.get_users_on_page(page=page)
    if users_on_page: 
        schema = UserSchema()
        users = schema.dump(users_on_page, many=True)
        return jsonify(users)
    return Response("users not found", status=404)


@app.route("/user/analytics", methods=["GET"])
def get_analytics(): 
    return jsonify(
        
    )