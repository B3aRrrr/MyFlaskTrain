from app import create_app, db
from app.models import User, Role
from faker import Faker
import os

# Создаем экземпляр приложения
app = create_app(os.getenv("FLASK_CONFIG") or 'default')

fake = Faker()

def add_random_users(num_users=10):
    with app.app_context():  # Создаем контекст приложения
        for _ in range(num_users):
            email = fake.email()
            username = fake.user_name()
            password = fake.password()
            role = Role.query.order_by(db.func.random()).first()  # Случайная роль

            if role is None:
                print('Нет доступных ролей для назначения пользователям')
                return
            user = User(email=email, username=username, password=password, role=role)
            db.session.add(user)

        db.session.commit()
        print(f"{num_users} случайных пользователей добавлены в базу данных.")

if __name__ == "__main__":
    add_random_users(10)  # Измените количество пользователей по необходимости
