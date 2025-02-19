from flask import Response

from app import app
from app.services import UserService


@app.route("/user/create")
def create_user(): 
    user_service = UserService()
    user_service.create("Polina", "example@mail.ru")
    response = Response("success", status=200)
    return response

