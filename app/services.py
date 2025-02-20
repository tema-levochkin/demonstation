from datetime import datetime, timedelta
from typing import Optional, Union

from flask_sqlalchemy.query import Query

from app import database
from app.models import User


class UserService: 
    def create(self, username: str, email: str) -> User: 
        """
        Creates a new user in the database.

        Args:
            username: The username of the new user.
            email: The email address of the new user.

        Returns:
            The newly created User object.
        """
        new_user = User(username=username, email=email)
        database.session.add(new_user) 
        database.session.commit()
        return new_user
    
    def get_user_from_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user from the database by their email address.

        Args:
            email: The email address of the user to retrieve.

        Returns:
            The User object if found, otherwise None.
        """
        user = database.session.query(User).filter(User.email==email).first()
        return user

    def get_user_from_id(self, user_id: int) -> Optional[User]: 
        """
        Retrieves a user from the database by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The User object if found, otherwise None.
        """
        user = database.session.query(User).get(user_id)
        return user
        
    def update(self, user: User, update_data: dict) -> Optional[dict[str, str]]: 
        """
        Updates the email or username of a user in the database.
        If the user doesn't exist, email will be changed, also commits changes to the database.

        Args:
            user: The User object to update.
            update_data: A dictionary containing the fields to update (e.g., {"email": "new_email@example.com", "username": "NewUsername"}).

        Returns:
            The updated user data dictionary if the update was successful, None otherwise.
        """
        user = self.get_user_from_email(email=update_data.get("email"))
        if not user: 
            user.email = update_data.get("email")
            user.username = update_data.get("username")
            database.session.commit()
            return update_data

    def delete(self, user: User) -> None: 
        """
        Deletes a user from the database.

        Args:
            user: The User object to delete.
        """
        database.session.delete(user)
        database.session.commit()

    def get_users_on_page(self, page: int) -> Query[User]: 
        """
        Retrieves a paginated list of users from the database.

        Args:
            page: The page number to retrieve (starting from 1).

        Returns:
            A Query object containing the users for the specified page.
        """
        per_page = 5
        User_on_page = database.session.query(User).paginate(page=page, per_page=per_page)
        return User_on_page
    
    def get_users_last_week(self) -> Union[Query[User]]:
        """
        Retrieves a list of users who registered within the last week.

        Returns:
            A list of User objects who registered within the last week.
        """
        current_datetime = datetime.now()
        seven_days_ago = current_datetime - timedelta(days=7)
        users = database.session.query(User).filter(User.registration_date >= seven_days_ago).all()
        return users

    def get_users_longer_names(self) -> Union[Query[User]]:
        """
        Retrieves a list of the 5 users with the longest usernames.

        Returns:
            A list of User objects with the longest usernames, limited to 5.
        """
        users_with_longer_names = database.session.query(User).order_by(database.func.length(User.username)).limit(5)
        return users_with_longer_names

    def get_email_domains_users_share(self) -> float: 
        """
        Calculates the percentage of users sharing each email domain.

        Returns:
            A dictionary where keys are email domains and values are the percentage of users sharing that domain (e.g., {"example.com": "50.0%"}).
        """
        query = database.session.query(
            database.func.substring(User.email, database.func.instr(User.email, '@') + 1).label('domain')
        ).distinct()
        all_users_count = database.session.query(User).count()
        domains = [row.domain for row in query.all()]
        users_share = {}
        for domain in domains: 
            users_with_domain = database.session.query(User).filter(User.email.ilike(f"%@{domain}")).count()
            share_percent = round((users_with_domain / all_users_count) * 100, 2)
            users_share[domain] = f"{share_percent}%"
        return users_share
