from faker import Faker

from app import User
from app import db


if __name__ == '__main__':
    fake = Faker()
    my_fingerprint = 'cd24492a03e4506247a89108f61ec151'
    for i in range(10):
        fingerprint = my_fingerprint if i == 0 else fake.md5()
        user = User(
            fingerprint=fingerprint,
            first_name=fake.first_name(),
            second_name=fake.last_name(),
            email=fake.email()
        )
        db.session.add(user)
        db.session.commit()

