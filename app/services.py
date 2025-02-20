from datetime import datetime, timedelta
from typing import Optional, Union

from flask_sqlalchemy.query import Query

from app import database
from app.models import User


class UserService: 
    def create(self, username: str, email: str) -> User: 
        new_user = User(username=username, email=email)
        database.session.add(new_user) 
        database.session.commit()
        return new_user
    
    def get_user_from_email(self, email: str) -> Optional[User]:
        user = database.session.query(User).filter(User.email==email).first()
        return user

    def get_user_from_id(self, user_id: int) -> Optional[User]: 
        user = database.session.query(User).get(user_id)
        return user
        
    def update(self, user: User, update_data: dict) -> dict[str, str]: 
        user.email = update_data.get("email")
        user.username = update_data.get("username")
        database.session.commit()
        return update_data

    def delete(self, user: User) -> None: 
        database.session.delete(user)
        database.session.commit()

    def get_users_on_page(self, page: int) -> Query[User]: 
        per_page = 5
        User_on_page = database.session.query(User).paginate(page=page, per_page=per_page)
        return User_on_page
    
    def get_users_from_last_week(self) -> Union[Query[User]]:
        current_datetime = datetime.now()
        seven_days_ago = current_datetime - timedelta(days=7)
        users = database.session.query(User).filter(User.registration_date >= seven_days_ago).all()
        return users

    def get_users_with_longer_names(self) -> Union[Query[User]]:
        users_with_longer_names = database.session.query(User).order_by(database.func.length(User.username)).limit(5)
        return users_with_longer_names

    def get_email_domains_users_share(self, domain) -> float: 
        users_share = database.session.query(
            User.email, database.func.count(User.email)
            ).group_by(
                User.email
            ).order_by(
                database.func.count(User.name).desc()
            ).all()
        # users_with_email_domain = database.session.query(User).filter(User.email.ilike(f"%@{domain}")).count()
        # all_users = database.session.query(User).all().count()
        # users_share = (users_with_email_domain / all_users) * 100
        return users_share
