import os
import django
from faker import Faker


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banksystem.settings')  
django.setup()

# Correct lowercase import
from Users.models import User

fake = Faker()

def create_fake_users(n=500):
    users = []
    print('Entering loop')
    print(n)
    for i in range(n):
        username = f'user{i+1}'
        print(username)
        email = f'{username}@example.com'
        password = "password123"
        phone = fake.phone_number()

        user = User(
            username=username,
            email=email,
            phone=phone
        )
        user.set_password(password)
        users.append(user)
    print('Exit loop')
    User.objects.bulk_create(users)
    print(f"{n} fake users created successfully using bulk_create().")

if __name__ == "__main__":
    create_fake_users()
