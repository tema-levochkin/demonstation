from flask import Response, jsonify, request

from app import app
from app.services import UserService
from app.schemas import UserSchema, UserCreateSchema


user_service = UserService()


@app.route("/user/create", methods=["POST"])
def create_user() -> Response: 
    new_user_data = request.get_json()
    username = new_user_data.get("username")
    email = new_user_data.get("email")
    user = user_service.get_user_from_email(email=email)
    if user: 
        return Response("user with this email has already been registered", status=409)
    
    user_schema = UserCreateSchema()
    errors = user_schema.validate(new_user_data)
    if errors: 
        return jsonify(errors), 400
    
    new_user = user_service.create(username, email)
    if new_user: 
        return jsonify({
            "id": new_user.id,
            "username": new_user.username, 
            "email": new_user.email, 
            "registraion_date": new_user.registration_date
        })
    return Response("not valid user data", status=400)


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Response: 
    user = user_service.get_user_from_id(user_id=user_id)
    if not user:
        return Response("user not found", status=404) 
    
    return jsonify({
        "id": user.id,
        "username": user.username, 
        "email": user.email, 
        "registraion_date": user.registration_date
    })


@app.route("/user/update", methods=["PATCH"])
def update_user() -> Response:
    user_data = request.get_json()
    user = user_service.get_user_from_id(user_id=user_data.get("user_id"))
    if not user:
        return Response("user not found", status=404) 
    
    update_data = user_service.update(user, user_data.get("update_data"))
    if not update_data: 
        return Response("not valid data for update", status=400)
    
    return jsonify(update_data)    
    

@app.route("/user/delete", methods=["DELETE"])
def delete_user() -> Response: 
    user_data = request.get_json()
    user = user_service.get_user_from_id(user_id=user_data.get("user_id"))
    if not user:
        return Response("user not found", status=404) 
    
    user_service.delete(user)
    return Response("user was delete", status=200) 


@app.route("/user/list", methods=["GET"])
def get_list_users() -> Response: 
    page = int(request.args.get("page", 1))
    users_on_page = user_service.get_users_on_page(page=page)
    if users_on_page: 
        schema = UserSchema()
        users = schema.dump(users_on_page, many=True)
        return jsonify(users)
    return Response("users not found", status=404)


@app.route("/user/analytics", methods=["GET"])
def get_analytics(): 
    schema = UserSchema()
    users_from_last_week = user_service.get_users_from_last_week()
    users_from_last_week_validate = schema.dump(users_from_last_week, many=True)

    users_with_loger_names = user_service.get_users_with_longer_names()
    users_with_loger_names_validate = schema.dump(users_with_loger_names, many=True)

    return jsonify(
        {
            "user_from_last_week": users_from_last_week_validate, 
            "users_with_longer_names": users_with_loger_names_validate, 
            "email_domains_users_share": {

            } 
        }
    )


@app.route("/static/swagger.json")
def serve_swagger_json():
    return app.send_static_file("swagger.json")