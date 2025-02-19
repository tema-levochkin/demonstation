from app import database
from app.models import User 


class UserService: 
    def create(self, username: str, email: str): 
        print(database.func.current_timestamp)
        # new_user = User(username=username, email=email)
        # database.session.add(new_user) 
        # database.session.commit()
    
    def read(id: int):
        pass

    def update(id: int): 
        pass 

    def delete(id:int ): 
        pass 

