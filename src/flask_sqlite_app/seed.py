from . import db
from .models import Account


def seed_default_accounts():
    nb_accounts = db.session.query(Account.id).count()
    if nb_accounts == 0:
        print("No accounts. We create two default accounts.")
        acc = Account(
            name="Elaine",
            password="abc",
            settings="lang:US ; theme:black"
        )
        db.session.add(acc)
        db.session.commit()
        acc = Account(
            name="Herman",
            password="123",
            settings="lang:FR"
        )
        db.session.add(acc)
        db.session.commit()
