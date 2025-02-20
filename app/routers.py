from flask import Response, jsonify, request

from app import app
from app.services import UserService
from app.schemas import UserSchema


user_service = UserService()


@app.route("/user/create", methods=["POST"])
def create_user() -> Response:
    """
    Creates a new user.

    Receives a JSON payload with the new user's username and email.
    Validates the input and creates the user in the database.

    Returns:
        A JSON response with the new user's data if successful, or an error message with a 400 or 409 status code.
    """ 
    user_schema = UserSchema()
    errors = user_schema.validate(new_user_data)
    if errors: 
        return jsonify(errors), 400
    
    new_user_data = request.get_json()
    username = new_user_data.get("username")
    email = new_user_data.get("email")
    user = user_service.get_user_from_email(email=email)
    if user: 
        return Response("user with this email has already been registered", status=409)
    
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
    """
    Retrieves a user by ID.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        A JSON response with the user's data if found, or a 404 error if the user is not found.
    """
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
    """
    Updates an existing user.

    Receives a JSON payload with the user's ID and the data to update.
    Validates the input and updates the user in the database.

    Returns:
        A JSON response with the updated user data if successful, or an error message with a 400 or 404 status code.
    """
    user_schema = UserSchema()
    errors = user_schema.validate(user_data.get("update_data"))
    if errors: 
        return jsonify(errors), 400
    
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
    """
    Deletes a user.

    Receives a JSON payload with the user's ID.
    Deletes the user from the database.

    Returns:
        A 200 status code if successful, or a 404 error if the user is not found.
    """
    user_data = request.get_json()
    user = user_service.get_user_from_id(user_id=user_data.get("user_id"))
    if not user:
        return Response("user not found", status=404) 
    
    user_service.delete(user)
    return Response("user was delete", status=200) 


@app.route("/user/list", methods=["GET"])
def get_list_users() -> Response: 
    """
    Retrieves a paginated list of users.

    Args:
        page (optional): The page number to retrieve (default: 1).

    Returns:
        A JSON response with the list of users on the specified page, or a 404 error if no users are found.
    """
    page = int(request.args.get("page", 1))
    users_on_page = user_service.get_users_on_page(page=page)
    if users_on_page: 
        schema = UserSchema()
        users = schema.dump(users_on_page, many=True)
        return jsonify(users)
    return Response("users not found", status=404)


@app.route("/user/analytics", methods=["GET"])
def get_analytics():
    """
    Retrieves user analytics data.

    Returns:
        A JSON response with user data from the last week, users with longer names, and email domain sharing information.
    """
    users_last_week = user_service.get_users_last_week()
    users_longer_names = user_service.get_users_longer_names()
    email_domains_users_share = user_service.get_email_domains_users_share()

    users_last_week_data = [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "registration_date": user.registration_date
    } for user in users_last_week]

    users_longer_names_data = [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "registration_date": user.registration_date
    } for user in users_longer_names]

    return jsonify(
        {
            "users_last_week": users_last_week_data,
            "users_longer_names": users_longer_names_data,
            "email_domains_users_share": email_domains_users_share
        }
    )


@app.route("/static/swagger.json")
def serve_swagger_json():
    return app.send_static_file("swagger.json")