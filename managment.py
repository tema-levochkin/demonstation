import sys
import random

from datetime import datetime, timedelta

from faker import Faker

from app import database, app
from app.models import User
from app.services import UserService


def generate_random_date() -> datetime: 
    """
    Generates a random date between 2010-01-01 and 2025-01-01.

    Returns:
        datetime: A random date within the specified range.
    """
    start_date = datetime(
        year=2010, 
        month=1, 
        day=1, 
        hour=random.randint(0, 23), 
        minute=random.randint(0, 59)
        )
    end_date = datetime(
        year=2025, 
        month=1, 
        day=1, 
        hour=random.randint(0, 23), 
        minute=random.randint(0, 59)
        )
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date


def generate_random_users() -> None:
    """
    Generates and adds 1000 random users to the database if they don't already exist.

    Returns:
        None
    """
    faker = Faker()
    for _ in range(1000):
        user_servise = UserService()
        with app.app_context():
            email = faker.free_email()
            user = user_servise.get_user_from_email(email=email)
            if not user: 
                username = faker.name()
                registration_date = generate_random_date()
                new_user = User(
                    username=username, 
                    email=email, 
                    registration_date=registration_date
                    )
                database.session.add(new_user)
                database.session.commit()


command = sys.argv[1]
if command == "generate_random_users":
    generate_random_users()