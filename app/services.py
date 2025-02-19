from typing import Optional, Union

from app import database
from app.models import Users


class UserService: 
    def create(self, username: str, email: str) -> Optional[Users]: 
        user = self.get_user_from_email(email=email)
        if not user: 
            new_user = Users(username=username, email=email)
            database.session.add(new_user) 
            database.session.commit()
            return new_user
    
    def get_user_from_email(self, email: str) -> Optional[Users]:
        user = database.session.query(Users).filter(email=email).first()
        return user

    def get_user_from_id(self, id: int) -> Optional[Users]: 
        user = database.session.query(Users).get(id)
        return user
        
    def update(self, user: Users, updated_data: dict): 
        user.update(updated_data)
        database.session.commit()

    def delete(self, user: Users) -> None: 
        database.session.delete(user)
        database.session.commit()

    def get_users_on_page(self, page: int) -> list[Users]: 
        per_page = 5
        users_on_page = database.session.query(Users).paginate(page=page, per_page=per_page)
        return users_on_page
    
    def get_users_from_last_week(self) -> Union[list[Users]]:
        pass 

    def get_users_with_longer_names(self) -> Union[list[Users]]:
        pass

    def get_email_domains_users_share(self) -> float: 
        pass 